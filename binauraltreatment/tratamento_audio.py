


from scipy.io import loadmat
import numpy as np
from scipy.signal import fftconvolve, resample
import warnings
import os

class Calibration():
    def __init__(self, ui=None):
        super(Calibration, self).__init__()

    def equalizeSignal(self, timeSignal=np.array([1, 0, 0, 0, 0]),
                       samplingRate=44100,
                       hats='HMSIII.2',
                       audioInterface='UCA222',
                       headPhone='HD58X'):
        '''
        Equalize a signal to playback in a headphone. The filter is loaded from a .mat file
        located in the 'hats' directory.
        '''
        filename = f"eq_{hats}_{audioInterface}_{headPhone}.mat"
        filter_dir = os.path.join(os.path.dirname(__file__), "hats")
        filter_path = os.path.join(filter_dir, filename)

        try:
            filterData = loadmat(filter_path)
        except FileNotFoundError:
            warnings.warn(f"Filtro não encontrado: {filter_path}", UserWarning)
            return None

        if samplingRate != filterData['samplingRate']:
            num_samples = int(len(timeSignal) * filterData['samplingRate'] / samplingRate)
            timeSignal = resample(timeSignal, num_samples)

        nChannels = timeSignal.ndim
        if nChannels == 1:
            warnings.warn("Esperado sinal binaural. Verifique seus dados.", UserWarning)
            eqSignal = np.vstack((
                fftconvolve(timeSignal, filterData['hcorrLeftMF'].flatten()),
                fftconvolve(timeSignal, filterData['hcorrRightMF'].flatten())
            )).transpose()
        elif nChannels == 2:
            eqSignal = np.vstack((
                fftconvolve(timeSignal[:, 0], filterData['hcorrLeftMF'].flatten()),
                fftconvolve(timeSignal[:, 1], filterData['hcorrRightMF'].flatten())
            )).transpose()
        else:
            raise ValueError("Formato de sinal não suportado (esperado mono ou estéreo).")

        return eqSignal

    def applyHRIR(self, micSignal=np.array([1, 0, 0, 0, 0]),
                  samplingRate=44100,
                  hats="HMSIII.2"):

        filename = f"hrir{hats}.mat"
        hrir_dir = os.path.join(os.path.dirname(__file__), "hats")
        hrir_path = os.path.join(hrir_dir, filename)

        try:
            hrir = loadmat(hrir_path)
        except FileNotFoundError:
            warnings.warn(f"HRIR não encontrado: {hrir_path}", UserWarning)
            return None

        if samplingRate != hrir['samplingRate']:
            num_samples = int(len(micSignal) * hrir['samplingRate'] / samplingRate)
            micSignal = resample(micSignal, num_samples)

        binauralAudio = np.vstack((
            fftconvolve(micSignal, hrir['hrirLeft'].flatten()),
            fftconvolve(micSignal, hrir['hrirRight'].flatten())
        )).transpose()

        return binauralAudio

if __name__ == "__main__":
    cal = Calibration()
    binauralAudio = cal.applyHRIR(hats='HMSIII.2')
    print("HRIR aplicado com sucesso.")

