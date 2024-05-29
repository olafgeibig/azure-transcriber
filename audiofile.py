import numpy as np
from scipy.io import wavfile
from scipy.signal import resample
from pydub import AudioSegment

def convert_mp3_to_wav(mp3_file_path, output_wav_file_path):
    """
    Converts an mp3 file to a mono wav file with 16bit 16kHz sampling rate.

    Args:
        mp3_file_path (str): Path to the input mp3 file.
        output_wav_file_path (str): Path to the output wav file.
    """
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio = audio.set_channels(1)
    audio.export(output_wav_file_path, format="wav")

    # Resample the wav file to 16kHz
    rate, data = wavfile.read(output_wav_file_path)
    resampled_data = resample(data, int(len(data) * 16000 / rate))
    wavfile.write(output_wav_file_path, 16000, resampled_data.astype(np.int16))

