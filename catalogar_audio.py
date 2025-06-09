
"""
import numpy as np
import librosa

def calcular_loudness(audio):
    loudness = np.mean(audio)
    return loudness


def calcular_sharpness(audio, sr):
    media_espectro = np.mean(np.abs(librosa.stft(audio)), axis=1)
    taxas_amostral = librosa.fft_frequencies(sr=sr)
    media_freq = np.sum(taxas_amostral * media_espectro) / np.sum(media_espectro)
    return media_freq


def calcular_roughness(audio):
    roughness = np.mean(np.abs(np.diff(audio)))
    return roughness



def analisar_audio(audio, sr):
    loudness = calcular_loudness(audio)
    sharpness = calcular_sharpness(audio, sr)
    roughness = calcular_roughness(audio)

    resultados = {
        "loudness": loudness,
        "sharpness": sharpness,
        "roughness": roughness,
    }

    return resultados

def catalogar_audio(caminho_arquivo):
    audio, sr = librosa.load(caminho_arquivo, sr=None)
    resultados = analisar_audio(audio, sr)
    return resultados

"""


import numpy as np
import librosa

from loudness import Loudness
from roughness import Roughness
from sharpness_din import Sharpnes_DIN
from binauraltreatment.tratamento_audio import Calibration

def analisar_audio(audio, sr):
    # Inicializar os objetos de análise
    loudness_calc = Loudness()
    roughness_calc = Roughness()
    sharpness_calc = Sharpnes_DIN()

    # Calcular as métricas
    _, loudness_global, _ = loudness_calc.loudnessZWK(audio, sr)
    _, roughness_global, _ = roughness_calc.roughnessDW(audio, sr)
    _, sharpness_global, _ = sharpness_calc.sharpnessCalculation(audio, sr)

    resultados = {
        "loudness": loudness_global,
        "roughness": roughness_global,
        "sharpness": sharpness_global,
    }

    return resultados

def catalogar_audio(caminho_arquivo):
    # Carregar o áudio (espera-se áudio mono)
    audio, sr = librosa.load(caminho_arquivo, sr=None)

    # Aplicar tratamento binaural com filtro de correção
    cal = Calibration()
    audio_tratado = cal.equalizeSignal(
    timeSignal=audio,
    samplingRate=sr,
    hats='HMSIII.2',
    audioInterface='UCA222',
    headPhone='HD58X'
    )


    if audio_tratado is None:
        raise RuntimeError("Erro no tratamento binaural: filtro de correção não encontrado ou mal formatado.")

    # Analisar o sinal tratado
    resultados = analisar_audio(audio_tratado, sr)
    return resultados

# Exemplo de uso (caso deseje rodar direto para teste):
if __name__ == "__main__":
    caminho = "exemplo.wav"  # Substitua pelo nome real
    print(catalogar_audio(caminho))
