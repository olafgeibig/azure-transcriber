import streamlit as st
from azure_transcription import conversation_transcription

def main():
    st.title("Azure Transcription")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        st.write(file_details)
        transcriptions = conversation_transcription(uploaded_file)
        for transcription in transcriptions:
            st.text(transcription)

if __name__ == "__main__":
    main()
