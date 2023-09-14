import time
import uuid
from dotenv import load_dotenv
import os

from scipy.io import wavfile
from pydub import AudioSegment
from scipy.signal import resample

load_dotenv()
AZURE_AI_KEY = os.environ.get('AZURE_AI_KEY')
AZURE_AI_REGION = os.environ.get('AZURE_AI_REGION')

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)

# This sample demonstrates how to use conversation transcription.
def conversation_transcription(conversationfilename):
    """transcribes a conversation"""
    # Creates speech configuration with subscription information
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_AI_KEY, region=AZURE_AI_REGION)

    channels = 1
    bits_per_sample = 16
    samples_per_second = 16000

    # Create audio configuration using the push stream
    wave_format = speechsdk.audio.AudioStreamFormat(samples_per_second, bits_per_sample, channels)
    stream = speechsdk.audio.PushAudioInputStream(stream_format=wave_format)
    audio_config = speechsdk.audio.AudioConfig(stream=stream)

    transcriber = speechsdk.transcription.ConversationTranscriber(speech_config, audio_config, language="de-DE")

    done = False
    transcriptions = []

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous transcription upon receiving an event `evt`"""
        nonlocal done
        done = True

    # Subscribe to the events fired by the conversation transcriber
    transcriber.transcribed.connect(lambda evt: transcriptions.append(str(evt.result.speaker_id) + ": " + str(evt.result.text)))
    transcriber.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    transcriber.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    transcriber.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous transcription on either session stopped or canceled events
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)

    transcriber.start_transcribing_async()

    # Read the whole wave files at once and stream it to sdk
    _, wav_data = wavfile.read(conversationfilename)
    stream.write(wav_data.tobytes())
    stream.close()
    while not done:
        time.sleep(.5)

    transcriber.stop_transcribing_async()

    return transcriptions


# This sample demonstrates how to use conversation transcription.
def conversation_transcription_from_microphone():
    """transcribes a conversation"""
    # Creates speech configuration with subscription information
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_AI_KEY, region=AZURE_AI_REGION)
    transcriber = speechsdk.transcription.ConversationTranscriber(speech_config)

    done = False

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous transcription upon receiving an event `evt`"""
        print('CLOSING {}'.format(evt))
        nonlocal done
        done = True

    # Subscribe to the events fired by the conversation transcriber
    transcriber.transcribed.connect(lambda evt: print('TRANSCRIBED: {}'.format(evt)))
    transcriber.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    transcriber.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    transcriber.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous transcription on either session stopped or canceled events
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)

    transcriber.start_transcribing_async()

    while not done:
        # No real sample parallel work to do on this thread, so just wait for user to type stop.
        # Can't exit function or transcriber will go out of scope and be destroyed while running.
        print('type "stop" then enter when done')
        stop = input()
        if (stop.lower() == "stop"):
            print('Stopping async recognition.')
            transcriber.stop_transcribing_async()
            break

import streamlit as st

    
from audio_handler import convert_mp3_to_wav
