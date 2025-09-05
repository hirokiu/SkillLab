import os
import pyaudio
import numpy as np
import pandas as pd
from google.cloud import storage
from datetime import datetime
import time

# Parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
CSV_FILE_PATH = "dataset.csv"

# Initialize PyAudio
p = pyaudio.PyAudio()

# Google Cloud Storage configurations
BUCKET_NAME = 'us.artifacts.line-syokudo.appspot.com'

# Initialize the CSV file with headers if not exist
if not os.path.exists(CSV_FILE_PATH):
    df = pd.DataFrame(columns=['timestamp', 'mean_freq'])
    df.to_csv(CSV_FILE_PATH, index=False)

def upload_to_gcs(file_path, blob_name):
    """Uploads a file to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path)

def record_and_process():

global data_list 
while True:

        print("Recording...")

        # Recording audio
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=1)
        frames = [stream.read(CHUNK, exception_on_overflow=False) for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS))]
        # Stop recording
        stream.stop_stream()
        stream.close()

        # Convert audio to numpy array
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

        # Perform FFT and get the mean frequency
        fft_data = np.fft.fft(audio_data)
        frequencies = np.fft.fftfreq(len(fft_data))
        positive_frequencies = frequencies[np.where(frequencies > 0)]
        magnitudes = np.abs(fft_data[np.where(frequencies > 0)])

        mean_freq = np.mean(positive_frequencies[np.where(magnitudes == max(magnitudes))])

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Append data to list instead of reading the CSV file each time
        data_list.append({'timestamp': timestamp, 'mean_freq': mean_freq})

        # Convert the list to a DataFrame and save it as a CSV file
        df = pd.DataFrame(data_list)
        df.to_csv(CSV_FILE_PATH, index=False)

        # Upload the CSV file to Google Cloud Storage
        upload_to_gcs(CSV_FILE_PATH, 'audio-data/dataset.csv')

        print(f"Recording saved with timestamp: {timestamp} and mean frequency: {mean_freq} Hz")

        # Wait for 5 minutes before the next recording
        time.sleep(300)

# Start the recording and processing
record_and_process()

# Close PyAudio
p.terminate()

