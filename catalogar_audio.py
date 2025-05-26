

import numpy as np
import librosa

def calcular_loudness(audio):
    loudness = np.mean(audio)
    return loudness

def classificar_loudness(loudness):
    if 0 < loudness < 0.02:
        return "Muito baixo"
    elif 0.02 <= loudness < 0.05:
        return "Baixo"
    elif 0.05 <= loudness < 0.1:
        return "Moderado"
    elif 0.1 <= loudness < 0.2:
        return "Alto"
    elif 0.2 <= loudness < 0.4:
        return "Muito alto"
    else:
        return "extremamente alto"

def calcular_sharpness(audio, sr):
    media_espectro = np.mean(np.abs(librosa.stft(audio)), axis=1)
    taxas_amostral = librosa.fft_frequencies(sr=sr)
    media_freq = np.sum(taxas_amostral * media_espectro) / np.sum(media_espectro)
    return media_freq

def classificar_sharpness(media_freq):
    if 60 <= media_freq < 250:
        return "Grave."
    elif 250 <= media_freq < 640:
        return "Médio grave."
    elif 640 <= media_freq < 2500:
        return "Médio"
    elif 2500 <= media_freq < 5000:
        return "Médio agudo"
    else:
        return "Som agudo."

def calcular_strength(audio):
    var_lenta = librosa.feature.rms(y=audio, frame_length=2048)[0]
    fluct_strength = np.std(var_lenta)
    return fluct_strength

def classificar_strength(fluct_strength):
    if fluct_strength < 0.005:
        return "Som completamente estável."
    elif 0.005 <= fluct_strength < 0.01:
        return "Som levemente instável."
    elif 00.1 <= fluct_strength < 0.02:
        return "Possui flutuações lentas suaves."
    elif 0.02 <= fluct_strength < 0.04:
        return "Possui flutuações lentas moderadas."
    else:
        return "Possui flutuações lentas intensas."

def calcular_roughness(audio):
    roughness = np.mean(np.abs(np.diff(audio)))
    return roughness

def classificar_roughness(roughness):
    if roughness < 0.005:
        return "Muito suave."
    elif 0.005 <= roughness < 0.015:
        return "Levemente áspero."
    elif 0.015 <= roughness < 0.03:
        return "Aspereza moderada."
    elif 0.03 <= roughness < 0.05:
        return "Áspero."
    else:
        return "Extremamente áspero"

def calcular_tonality(audio, sr):
    media_espec = np.mean(np.abs(librosa.stft(audio)), axis=1)
    frequencias = librosa.fft_frequencies(sr=sr)
    freq_dominante = frequencias[np.argmax(media_espec)]
    return freq_dominante

def classificar_tonality(freq_dominante):
    if freq_dominante < 100:
        return "Tonalidade muito grave"
    elif 100 <= freq_dominante < 300:
        return "Tonalidade grave"
    elif 300 <= freq_dominante < 800:
        return "Tonalidade média grave"
    elif 800 <= freq_dominante < 1500:
        return "Tonalidade média"
    elif 1500<= freq_dominante < 3000:
        return "Tonalidade média aguda"
    elif 3000<= freq_dominante < 5000:
        return "Tonalidade sibilante"
    else:
        return "Tonalidade muito aguda ou assobiante"

def analisar_audio(audio, sr):
    loudness = calcular_loudness(audio)
    sharpness = calcular_sharpness(audio, sr)
    strength = calcular_strength(audio)
    roughness = calcular_roughness(audio)
    tonality = calcular_tonality(audio, sr)

    resultados = {
        "loudness": (f"{calcular_loudness(audio):.8f} {classificar_loudness(loudness)}"), 
        "sharpness": (f"{calcular_sharpness(audio, sr):.4f} {classificar_sharpness(sharpness)}"),
        "strength": (f"{calcular_strength(audio):.4f} {classificar_strength(strength)}"),
        "roughness": (f"{calcular_roughness(audio):.4f} {classificar_roughness(roughness)}"),
        "tonality": (f"{calcular_tonality(audio, sr):.4f} {classificar_tonality(tonality)}"),
    }

    """
    resultados = {
        "loudness": classificar_loudness(loudness),
        "sharpness": classificar_sharpness(sharpness),
        "strength": classificar_strength(strength),
        "roughness": classificar_roughness(roughness),
        "tonality": classificar_tonality(tonality),
    }
    """

    return resultados

def catalogar_audio(caminho_arquivo):
    audio, sr = librosa.load(caminho_arquivo, sr=None)
    resultados = analisar_audio(audio, sr)
    return resultados