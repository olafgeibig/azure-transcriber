import streamlit as st
import time
from audiofile import convert_mp3_to_wav, convert_m4a_to_wav
from threading import Thread
from streamlit.runtime.scriptrunner import add_script_run_ctx
from test_transcriber import ConversationTranscriber
from streamlit.components.v1 import html
import streamlit_scrollable_textbox as stx

# Notify function to update transcriptions
def notify(event):
    # Define transcriptions as a session state variable
    if 'transcriptions' not in st.session_state:
        st.session_state.transcriptions = []
    text = str(event.result.speaker_id) + ": " + str(event.result.text)
    print(text)
    st.session_state.transcriptions.append(text)
    st.text_area("Transcriptions", "\n".join(st.session_state.transcriptions), height=400)

# Main function
def main():
    # Initialize session state for transcriptions if not already present
    if 'transcriptions' not in st.session_state:
        st.session_state.transcriptions = []
    
    add_script_run_ctx(notify)

    st.set_page_config(
        page_title = "Azure Meeting Transcription",
        page_icon = "💬",
        layout = "wide",
    )
    
    uploaded_file = st.file_uploader("Choose a file", type=["m4a", "mp3", "wav"])
    wav_file_path = "./temp.wav"
    
    # Check the file type and convert if necessary
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension == "mp3":
            with st.spinner('Converting mp3 to wav format...'):
                convert_mp3_to_wav(uploaded_file, wav_file_path)
        elif file_extension == "m4a":
            with st.spinner('Converting m4a to wav format...'):
                convert_m4a_to_wav(uploaded_file, wav_file_path)
        elif file_extension == "wav":
            wav_file_path = uploaded_file
    else:
        st.warning("Please upload an audio file.")
        return

    # Transcribe the wav file
    with st.spinner('Transcribing audio file...'):
        transcriber = ConversationTranscriber(notify)
        transcriber.transcribe(wav_file_path)

# Call main function
if __name__ == "__main__":
    main()
