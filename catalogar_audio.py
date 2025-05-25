

import numpy as np
import librosa

def calcular_loudness(audio):
    potencia = np.square(audio)
    loudness = np.mean(potencia)
    return loudness

def classificar_loudness(loudness):
    if loudness > 0.05:
        return "Som barulhento."
    else:
        return "Som baixo."

def calcular_sharpness(audio, sr):
    media_espectro = np.mean(np.abs(librosa.stft(audio)), axis=1)
    taxas_amostral = librosa.fft_frequencies(sr=sr)
    media_freq = np.sum(taxas_amostral * media_espectro) / np.sum(media_espectro)
    return media_freq

def classificar_sharpness(media_freq):
    if media_freq < 250:
        return "Som grave."
    elif 250 <= media_freq < 2500:
        return "Som médio."
    else:
        return "Som agudo."

def calcular_strength(audio):
    var_lenta = librosa.feature.rms(y=audio, frame_length=2048)[0]
    fluct_strength = np.std(var_lenta)
    return fluct_strength

def classificar_strength(fluct_strength):
    if fluct_strength > 0.01:
        return "Possui flutuações lentas."
    else:
        return "O som é estável."

def calcular_roughness(audio):
    roughness = np.mean(np.abs(np.diff(audio)))
    return roughness

def classificar_roughness(roughness):
    if roughness > 0.02:
        return "Possui flutuação rápida."
    else:
        return "O som é suave."

def calcular_tonality(audio, sr):
    media_espec = np.mean(np.abs(librosa.stft(audio)), axis=1)
    frequencias = librosa.fft_frequencies(sr=sr)
    freq_dominante = frequencias[np.argmax(media_espec)]
    return freq_dominante

def classificar_tonality(freq_dominante):
    if freq_dominante < 300:
        return "Tonalidade grave."
    elif freq_dominante < 1500:
        return "Tonalidade média."
    elif freq_dominante < 5000:
        return "Tonalidade sibilante."
    else:
        return "Tonalidade assobiante ou muito aguda."

def analisar_audio(audio, sr):
    loudness = calcular_loudness(audio)
    sharpness = calcular_sharpness(audio, sr)
    strength = calcular_strength(audio)
    roughness = calcular_roughness(audio)
    tonality = calcular_tonality(audio, sr)

    resultados = {
        "loudness": classificar_loudness(loudness),
        "sharpness": classificar_sharpness(sharpness),
        "strength": classificar_strength(strength),
        "roughness": classificar_roughness(roughness),
        "tonality": classificar_tonality(tonality),
    }

    return resultados

def catalogar_audio(caminho_arquivo):
    audio, sr = librosa.load(caminho_arquivo, sr=None)
    resultados = analisar_audio(audio, sr)
    return resultados