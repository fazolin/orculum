# Stack — começando simples, crescendo fácil

> O princípio aqui é: cada módulo funciona sozinho, se comunica por interfaces claras, e pode ser trocado sem derrubar o resto.

---

## Ponto de partida

O sistema mínimo viável precisa de:

1. Imagem e som entrando
2. Um modelo interpretando o que entra
3. Imagem e som saindo

Entrada é imagem e som. Saída é imagem e som. No meio, inteligência.

---

## Camada de percepção (entrada)

A entrada do oráculo é **imagem e som**. Câmera e microfone. O que roda localmente, em tempo real, com baixa latência.

### Imagem

| Função | Tecnologia | Comentário |
|---|---|---|
| Captura de vídeo | [OpenCV](https://opencv.org/) | Biblioteca padrão para captura e manipulação de vídeo. Roda em qualquer plataforma. |
| Entendimento da cena | [Moondream](https://huggingface.co/moondream) via [Ollama](https://ollama.ai/) | Modelo de visão + linguagem leve. Descreve o que vê na imagem em texto natural. Roda localmente via Ollama. |
| Detecção de presença e pose | [MediaPipe](https://developers.google.com/mediapipe) | Framework do Google para percepção corporal em tempo real. Pose, mãos, face. Grátis e bem documentado. |
| Reconhecimento facial | [InsightFace](https://github.com/deepinsight/insightface) | Gera embeddings de rosto para identificar pessoas. Open source, roda em GPU local. |

### Som

| Função | Tecnologia | Comentário |
|---|---|---|
| Captura de áudio | [sounddevice](https://python-sounddevice.readthedocs.io/) | Binding Python para PortAudio. Captura em tempo real com callback. |
| Transcrição de fala | [Whisper](https://github.com/openai/whisper) | Modelo da OpenAI para transcrição de voz. Multilíngue, roda localmente, qualidade alta. |

### Bibliotecas de suporte

| Biblioteca | Link | Uso |
|---|---|---|
| NumPy | [numpy.org](https://numpy.org/) | Operações numéricas sobre arrays de imagem e áudio |
| PyObjC | [pyobjc.readthedocs.io](https://pyobjc.readthedocs.io/) | Acesso nativo ao AVFoundation no macOS (nomes de câmera/microfone) |

### Infraestrutura

| Ferramenta | Link | Uso |
|---|---|---|
| uv | [docs.astral.sh/uv](https://docs.astral.sh/uv/) | Gerenciador de ambiente Python. Resolve versão e dependências automaticamente. |
| Ollama | [ollama.ai](https://ollama.ai/) | Servidor de modelos de IA locais. Gerencia download, otimização e inferência. |

---

## Camada de interpretação (a mente)

Recebe o pacote de percepção, consulta o banco de dados vivo, e produz uma intenção de resposta.

| Função | Tecnologia | Comentário |
|---|---|---|
| Raciocínio e decisão | [Claude API](https://docs.anthropic.com/) | Multimodal, contexto grande, raciocínio forte. Roda na nuvem — camada profunda. |
| Modelo local de apoio | [Ollama](https://ollama.ai/) + Llama/Mistral | Para respostas imediatas simples. Roda localmente — camada rápida. |

A camada de interpretação recebe texto + dados estruturados (e possivelmente imagem), e devolve:
- O que o oráculo entendeu
- O que o oráculo quer dizer/mostrar
- Instruções para a camada de expressão (tom, humor, intensidade)

O banco de dados vivo é consultado aqui: quem é essa pessoa? já esteve aqui antes? o que aconteceu da última vez?

---

## Banco de dados vivo (memória)

| Função | Tecnologia | Comentário |
|---|---|---|
| Banco principal | [PostgreSQL](https://www.postgresql.org/) + [pgvector](https://github.com/pgvector/pgvector) | Robusto, busca por similaridade em embeddings, nuvem para múltiplas instâncias. |
| Cache local | [SQLite](https://www.sqlite.org/) | Cada instância guarda espelho local. Funciona offline. |
| Estado de sessão | [Redis](https://redis.io/) | Quem está na frente agora, há quanto tempo, estado da conversa em tempo real. |

A sincronização entre instâncias acontece via o PostgreSQL central na nuvem.

---

## Camada de expressão (saída)

### Visual

| Função | Tecnologia | Comentário |
|---|---|---|
| Avatar / lipsync | [NVIDIA Audio2Face](https://www.nvidia.com/en-us/ai-data-science/audio2face/) | Anima rosto 3D a partir do áudio em tempo real. Integra com Unreal e outros motores. |
| Renderização do avatar | [Unreal Engine 5](https://www.unrealengine.com/) ou [Three.js](https://threejs.org/) | UE5 para qualidade máxima. Three.js para leveza e portabilidade. |
| Geração de imagem | [ComfyUI](https://github.com/comfyanonymous/ComfyUI) + [ControlNet](https://github.com/lllyasviel/ControlNet) | Geração de imagem modular. Pode ser condicionada pela pose/profundidade da percepção. |

### Sonora

| Função | Tecnologia | Comentário |
|---|---|---|
| Voz do oráculo | [ElevenLabs](https://elevenlabs.io/) | Síntese de voz de alta qualidade via API. Baixa latência, voz personalizada. |
| Voz de apoio local | [Bark](https://github.com/suno-ai/bark) / [XTTS](https://github.com/coqui-ai/TTS) | Roda localmente quando a nuvem cai. Qualidade menor, resposta imediata. |
| Textura sonora | [SuperCollider](https://supercollider.github.io/) ou [Max/MSP](https://cycling74.com/products/max) | Síntese sonora em tempo real, reativa a parâmetros do sistema. |

---

## Camada de integração (cola)

| Conexão | Protocolo | Comentário |
|---|---|---|
| Percepção → Interpretação | Interno (Python) | Mesma máquina, chamadas diretas. |
| Interpretação → Expressão visual | [OSC](https://opensoundcontrol.stanford.edu/) ou WebSocket | Desacopla mente do corpo — podem rodar em máquinas separadas. |
| Interpretação → Expressão sonora | OSC | Padrão universal de áudio ao vivo. |
| Avatar → Renderização | [NDI](https://ndi.video/) ou [Syphon](http://syphon.v002.info/)/[Spout](https://spout.zeal.co/) | Compartilhamento de vídeo entre aplicações. Latência quase zero. |
| Instância ↔ Banco central | HTTPS / API REST | Sincronização com a nuvem. |

---

## Linguagens e ambientes

| Camada | Linguagem / ambiente |
|---|---|
| Percepção | Python |
| Interpretação | Python |
| Banco de dados | PostgreSQL (nuvem) + SQLite (local) + Redis |
| Expressão visual — avatar | Unreal Engine 5 (C++ / Blueprints) ou Three.js (JavaScript) |
| Expressão visual — geração | Python (ComfyUI) |
| Expressão sonora — voz | Python (API) |
| Expressão sonora — ambiência | SuperCollider (sclang) ou Max/MSP |
| Integração | OSC, NDI, WebSocket |

---

## O que vem primeiro

Para um primeiro protótipo que prove o conceito de ponta a ponta:

1. Webcam + Moondream entendendo a cena
2. Whisper transcrevendo fala
3. Claude (API) interpretando e respondendo
4. ElevenLabs gerando a voz do oráculo
5. Um lipsync simples rodando sobre a voz gerada

Sem avatar sofisticado, sem geração de imagem complexa, sem múltiplas instâncias — apenas o ciclo completo: alguém chega, o oráculo percebe, pensa, e fala de volta.

---

*Cada escolha aqui pode mudar. O que importa são as interfaces entre os módulos — não os módulos em si.*
