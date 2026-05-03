"""
Captura de imagem e som — módulo de entrada do Oraculum.

Roda sozinho para testar: python3 capture.py
Ao iniciar, lista dispositivos disponíveis e pede para escolher.
"""

import cv2
import sounddevice as sd
import numpy as np
import queue
import platform


class ImageCapture:
    """Captura frames da câmera em tempo real."""

    def __init__(self, device=0):
        self.device = device
        self.cap = None

    def start(self):
        if platform.system() == "Darwin":
            self.cap = cv2.VideoCapture(self.device, cv2.CAP_AVFOUNDATION)
        else:
            self.cap = cv2.VideoCapture(self.device)
        if not self.cap.isOpened():
            raise RuntimeError(f"Não conseguiu abrir a câmera {self.device}")
        w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"[imagem] câmera {self.device} aberta ({w}x{h})")

    def read(self):
        if self.cap is None:
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def stop(self):
        if self.cap:
            self.cap.release()
            print("[imagem] câmera fechada")


class SoundCapture:
    """Captura áudio do microfone em tempo real."""

    def __init__(self, device=None, samplerate=16000, channels=1, blocksize=1024):
        self.device = device
        self.samplerate = samplerate
        self.channels = channels
        self.blocksize = blocksize
        self.audio_queue = queue.Queue()
        self.stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(f"[som] aviso: {status}")
        self.audio_queue.put(indata.copy())

    def start(self):
        self.stream = sd.InputStream(
            device=self.device,
            samplerate=self.samplerate,
            channels=self.channels,
            blocksize=self.blocksize,
            callback=self._callback,
        )
        self.stream.start()
        print(f"[som] microfone aberto ({self.samplerate / 1000:.0f}kHz)")

    def read(self):
        try:
            return self.audio_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            print("[som] microfone fechado")


def get_camera_names():
    """Pega os nomes das câmeras disponíveis no sistema operacional."""
    system = platform.system()
    try:
        if system == "Darwin":
            from AVFoundation import AVCaptureDevice, AVMediaTypeVideo
            devices = AVCaptureDevice.devicesWithMediaType_(AVMediaTypeVideo)
            return [d.localizedName() for d in devices]

        elif system == "Linux":
            from pathlib import Path
            video_dir = Path("/sys/class/video4linux")
            names = []
            if video_dir.exists():
                for dev in sorted(video_dir.iterdir()):
                    name_file = dev / "name"
                    if name_file.exists():
                        names.append(name_file.read_text().strip())
            return names

        elif system == "Windows":
            result = subprocess.run(
                ["powershell", "-Command",
                 "Get-CimInstance Win32_PnPEntity | Where-Object {$_.PNPClass -eq 'Camera' -or $_.PNPClass -eq 'Image'} | Select-Object -ExpandProperty Name"],
                capture_output=True, text=True
            )
            return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

    except Exception:
        pass
    return []


def choose_camera():
    print("\n=== CÂMERAS ===\n")
    names = get_camera_names()

    if not names:
        # fallback: tenta abrir por índice
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                names.append(f"Câmera {i}")
                cap.release()
            else:
                cap.release()
                break

    if not names:
        raise RuntimeError("Nenhuma câmera encontrada (verifique permissões)")

    for i, name in enumerate(names):
        print(f"  [{i}] {name}")

    if len(names) == 1:
        print(f"\n  → usando {names[0]}")
        return 0

    choice = input(f"\nEscolha a câmera: ")
    return int(choice)


def choose_microphone():
    print("\n=== MICROFONES ===\n")
    devices = sd.query_devices()
    inputs = []
    for i, d in enumerate(devices):
        if d["max_input_channels"] > 0:
            print(f"  [{i}] {d['name']}")
            inputs.append(i)

    if not inputs:
        raise RuntimeError("Nenhum microfone encontrado")

    if len(inputs) == 1:
        print(f"\n  → usando {devices[inputs[0]]['name']}")
        return inputs[0]

    choice = input(f"\nEscolha o microfone: ")
    return int(choice)


def main():
    cam_id = choose_camera()
    mic_id = choose_microphone()

    image = ImageCapture(device=cam_id)
    sound = SoundCapture(device=mic_id)

    image.start()
    sound.start()

    print("\n[entrada] rodando — pressione 'q' na janela de vídeo para sair\n")

    audio_level = 0.0

    try:
        while True:
            frame = image.read()
            if frame is None:
                break

            # atualiza nível de áudio
            audio = sound.read()
            if audio is not None:
                audio_level = np.abs(audio).mean()

            # desenha barra de som na imagem
            h, w = frame.shape[:2]
            bar_width = int(min(audio_level * 800, 1.0) * (w - 40))
            cv2.rectangle(frame, (20, h - 40), (20 + bar_width, h - 20), (0, 255, 0), -1)
            cv2.rectangle(frame, (20, h - 40), (w - 20, h - 20), (80, 80, 80), 1)

            cv2.imshow("Oraculum - entrada", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        pass
    finally:
        print("\n")
        image.stop()
        sound.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
