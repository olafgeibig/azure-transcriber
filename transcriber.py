import time
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
from scipy.io import wavfile

load_dotenv()
AZURE_AI_KEY = os.environ.get('AZURE_AI_KEY')
AZURE_AI_REGION = os.environ.get('AZURE_AI_REGION')

class ConversationTranscriber():
    """
    Class for transcribing conversations using Azure Speech Services.
    """
 
    def __init__(self, callback: callable):
        """
        Initializes a new instance of the ConversationTranscriber class.

        Args:
            callback (callable): The callback function to handle transcribed events.
        """
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_AI_KEY, region=AZURE_AI_REGION)

        # Create audio configuration using the push stream
        wave_format = speechsdk.audio.AudioStreamFormat(16000, 16, 1)
        self.stream = speechsdk.audio.PushAudioInputStream(stream_format=wave_format)
        audio_config = speechsdk.audio.AudioConfig(stream=self.stream)
        self.transcriber = speechsdk.transcription.ConversationTranscriber(speech_config, audio_config, language="de-DE")
        
        # Subscribe to the events fired by the conversation transcriber for debugging
        self.transcriber.transcribed.connect(callback)
        # self.transcriber.transcribed.connect(lambda evt: print(str(evt.result.speaker_id) + ": " + str(evt.result.text)))
        self.transcriber.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        self.transcriber.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        self.transcriber.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        # self.transcriber.session_stopped.connect(stop_cb)
        # self.transcriber.canceled.connect(stop_cb)
        
    def init_transcription(self):
        """
        Starts the transcription process asynchronously.

        Returns:
            An instance of the TranscriptionResult class representing the transcription result.
        """ 
        return self.transcriber.start_transcribing_async()

    def transcribe(self, filename: str):
        """
        Transcribes the audio file specified by the given filename.

        Args:
            filename (str): The path to the audio file to transcribe.
        """
        # Read the whole wave files at once and stream it to sdk
        _, wav_data = wavfile.read(filename)
        self.stream.write(wav_data.tobytes())
        self.stream.close()

    def stop(self):
        """
        Stops the transcription process asynchronously.
        """
        self.transcriber.stop_transcribing_async()