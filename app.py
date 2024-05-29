import streamlit as st
import time
from audiofile import convert_mp3_to_wav
from threading import Thread
from streamlit.runtime.scriptrunner import add_script_run_ctx

from test_transcriber import ConversationTranscriber
from streamlit.components.v1 import html
import streamlit_scrollable_textbox as stx

def main():
    transcriptions = []

    def notify(event):
        main.updated = True
        text = str(event.result.speaker_id) + ": " + str(event.result.text)
        transcriptions.append(text)

    wav_file_path = "./temp.wav"

    st.set_page_config(
        page_title = "Azure Meting Transcription",
        page_icon = "💬",
        layout = "wide",
    )
    
    transcriber = ConversationTranscriber(notify)
    transcriber.init_transcription()
    transcriber.transcribe(wav_file_path)

    # if "messages" not in st.session_state:
    #     st.session_state.messages = []

    display = html('', height=400, scrolling=True)
    # display = st.code()
    last = 0
    while True:
        time.sleep(1)
        now = len(transcriptions)
        if now > last:           
            full=''    
            for i in range(0, now):
                full += transcriptions[i]+"</p>"
            # print(full)
            display.write(full)
            last = now

    # print([k for k in st.session_state])

    # uploaded_file = st.file_uploader("Choose a file", type=["mp3"])
    # if True: # uploaded_file is not None:
    #     file_details = {"FileName":uploaded_file.name, "FileType":uploaded_file.type, "FileSize":uploaded_file.size}
    #     st.write(file_details)
        
    #     # Convert the uploaded mp3 file to a wav file with a spinner to indicate progress
    #     wav_file_path = "temp.wav"
    #     with st.spinner('Converting audio file to wav format...'):
    #         convert_mp3_to_wav(uploaded_file, wav_file_path)
        
    #     with st.spinner('Processing audio file...'):
    #         conversation_transcription(wav_file_path, update_ui)

if __name__ == "__main__":
    main()
