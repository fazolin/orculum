"""
Oraculum — orquestrador principal.

Conecta os módulos e roda o loop de percepção.
"""

import sys

if sys.version_info < (3, 10):
    print(f"\n[erro] Python 3.10+ necessário. Você está usando {sys.version.split()[0]}")
    sys.exit(1)

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import cv2
import numpy as np

from input.capture import ImageCapture, SoundCapture, choose_camera, choose_microphone
from input.perception import ScenePerception


def main():
    cam_id = choose_camera()
    mic_id = choose_microphone()

    image = ImageCapture(device=cam_id)
    sound = SoundCapture(device=mic_id)
    perception = ScenePerception(interval=3.0)

    image.start()
    sound.start()
    perception.start()

    print("\n[oraculum] rodando — 'q' para sair\n")

    audio_level = 0.0

    try:
        while True:
            frame = image.read()
            if frame is None:
                break

            # percepção visual
            description = perception.analyze(frame)

            # nível de áudio
            audio = sound.read()
            if audio is not None:
                audio_level = np.abs(audio).mean()

            # desenha na imagem
            h, w = frame.shape[:2]

            # barra de som
            bar_width = int(min(audio_level * 800, 1.0) * (w - 40))
            cv2.rectangle(frame, (20, h - 40), (20 + bar_width, h - 20), (0, 255, 0), -1)
            cv2.rectangle(frame, (20, h - 40), (w - 20, h - 20), (80, 80, 80), 1)

            # descrição da cena
            if description:
                cv2.putText(frame, description[:80], (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            cv2.imshow("Oraculum", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        pass
    finally:
        print("\n")
        perception.stop()
        image.stop()
        sound.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
