import os
import pyaudio
import wave
import whisper
import array
import dotenv
from config.settings import FORMAT, CHANNELS, RATE, CHUNK, SILENCE_LIMIT, THRESHOLD, AUDIO_FILE

def gravar_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print(f"🎙️ CROMOS está ouvindo... (Pode falar!)")
    frames = []
    num_silence_chunks = int(RATE / RATE * SILENCE_LIMIT)
    silence_counter = 0
    ouvindo_voz = False
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        as_ints = array.array('h', data)
        volume = max(as_ints)
        if volume > THRESHOLD:
            if not ouvindo_voz:
                print("🎙️ CROMOS está ouvindo...")
                ouvindo_voz = True
            silence_counter = 0
        else:
            if ouvindo_voz:
                silence_counter += 1
        if ouvindo_voz and silence_counter >= num_silence_chunks:
            break
    print("🛑 CROMOS processando sua fala...")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(AUDIO_FILE, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b'' .join(frames))
    wf.close()

def transcrever_audio():
    if not os.path.exists(AUDIO_FILE):
        return ""
    model = whisper.load_model("base")
    result = model.transcribe(AUDIO_FILE, language="pt")
    os.remove(AUDIO_FILE)
    return result['text'].strip()
