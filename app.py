import streamlit as st
from transcriber import conversation_transcription
from audiofile import convert_mp3_to_wav

def main():
    st.title("Azure Meting Transcription")
    uploaded_file=True
    # uploaded_file = st.file_uploader("Choose a file", type=["mp3"])
    if uploaded_file is not None:
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        st.write(file_details)
        
        # Convert the uploaded mp3 file to a wav file with a spinner to indicate progress
        wav_file_path = "temp.wav"
        # with st.spinner('Converting audio file to wav format...'):
        #     convert_mp3_to_wav(uploaded_file, wav_file_path)
        
        with st.spinner('Processing audio file...'):
            transcriptions = conversation_transcription(wav_file_path)
        st.text_area("Transcription", "\n".join(transcriptions), height=200)

if __name__ == "__main__":
    main()
