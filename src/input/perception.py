"""
Percepção visual — entende o que a câmera vê.

Usa Moondream via Ollama para descrever a cena.
Roda em thread separada para não travar o vídeo.
"""

import time
import base64
import urllib.request
import urllib.error
import json
import threading
import cv2


class ScenePerception:
    """Analisa frames da câmera e descreve o que vê via Ollama."""

    def __init__(self, model="moondream", interval=3.0, ollama_url="http://localhost:11434"):
        self.model = model
        self.interval = interval
        self.ollama_url = ollama_url
        self.last_description = ""
        self._busy = False
        self._last_request = 0

    def start(self):
        import shutil
        import subprocess

        if not shutil.which("ollama"):
            print("\n[percepção] Ollama não encontrado. Instale com:")
            print("  curl -fsSL https://ollama.com/install.sh | sh")
            print("\n[percepção] rodando sem entendimento de cena\n")
            self.ollama_url = None
            return

        try:
            req = urllib.request.Request(f"{self.ollama_url}/api/tags")
            response = urllib.request.urlopen(req, timeout=3)
            models = json.loads(response.read())
        except urllib.error.URLError:
            print("[percepção] Ollama instalado mas não está rodando. Iniciando...")
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2)
            try:
                req = urllib.request.Request(f"{self.ollama_url}/api/tags")
                response = urllib.request.urlopen(req, timeout=3)
                models = json.loads(response.read())
            except urllib.error.URLError:
                print("[percepção] não conseguiu iniciar o Ollama")
                self.ollama_url = None
                return

        model_names = [m["name"].split(":")[0] for m in models.get("models", [])]
        if self.model not in model_names:
            print(f"[percepção] modelo '{self.model}' não encontrado. Baixando...")
            subprocess.run(["ollama", "pull", self.model], check=True)

        print(f"[percepção] pronto ({self.model})")

    def _analyze_thread(self, frame):
        """Roda em thread separada — não bloqueia o vídeo."""
        _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        image_b64 = base64.b64encode(buffer).decode("utf-8")

        payload = json.dumps({
            "model": self.model,
            "prompt": "Describe what you see briefly.",
            "images": [image_b64],
            "stream": False,
        }).encode("utf-8")

        try:
            req = urllib.request.Request(
                f"{self.ollama_url}/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            response = urllib.request.urlopen(req, timeout=30)
            result = json.loads(response.read())
            self.last_description = result.get("response", "").strip()
        except Exception as e:
            print(f"\r[percepção] erro: {e}")
        finally:
            self._busy = False

    def analyze(self, frame):
        if self.ollama_url is None:
            return self.last_description

        now = time.time()
        if self._busy or now - self._last_request < self.interval:
            return self.last_description

        self._busy = True
        self._last_request = now
        thread = threading.Thread(target=self._analyze_thread, args=(frame.copy(),))
        thread.daemon = True
        thread.start()

        return self.last_description

    def stop(self):
        print("[percepção] parado")
