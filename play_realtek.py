import pyaudio
import io
from pydub import AudioSegment
import os

ruta_autor = "autorisation"

with open(ruta_autor, 'w') as archivo:
    archivo.write("no")

def play_audio_through_speaker(input_file, speaker_name):
    audio = AudioSegment.from_file(input_file)
    audio_data = audio.raw_data
    stream = io.BytesIO(audio_data)

    p = pyaudio.PyAudio()

    # Obtener información sobre los dispositivos de salida
    output_device_info = None
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if speaker_name in device_info['name']:
            output_device_info = device_info
            break

    if output_device_info is None:
        raise ValueError(f"No se encontró el dispositivo de altavoz con el nombre '{speaker_name}'.")

    stream_out = p.open(format=p.get_format_from_width(audio.sample_width),
                        channels=audio.channels,
                        rate=audio.frame_rate,
                        output=True,
                        output_device_index=output_device_info['index'])

    chunk_size = 1024
    data = stream.read(chunk_size)
    while data:
        stream_out.write(data)
        data = stream.read(chunk_size)

    stream_out.stop_stream()
    stream_out.close()
    p.terminate()

audio_file_path = os.path.join('repro.mp3')  # Reemplaza con la ruta de tu archivo de audio MP3
speaker_name = "Altavoces (Realtek(R) Audio)"  # Reemplaza con el nombre correcto de tu dispositivo de altavoz

play_audio_through_speaker(audio_file_path, speaker_name)
with open(ruta_autor, 'w') as archivo:
    archivo.write("yes")
