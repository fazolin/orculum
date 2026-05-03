# Módulos do sistema — visão geral

> Documento de pesquisa aberta. Nada aqui é decisão — é mapeamento de possibilidades.

O Oraculum é um sistema de ponta a ponta: percebe o mundo, interpreta o que percebeu, e responde com som e imagem. Esta página mapeia os módulos que compõem esse fluxo, das entradas até os resultados, e as tecnologias sendo investigadas em cada camada.

---

## Fluxo geral

```
[ ENTRADA ]  →  [ INTERPRETAÇÃO ]  →  [ DECISÃO ]  →  [ SAÍDA ]  →  [ PRESENÇA FÍSICA ]
  percepção       processamento         LLM / lógica     expressão      manifestação
```

---

## 1. Entrada — Percepção

O oráculo precisa perceber o que acontece ao seu redor. Esta camada captura e processa sinais do ambiente.

### 1.1 Visão

Câmeras fornecem o fluxo visual. O que se faz com ele:

- **Detecção de presença** — alguém está na sala? quantas pessoas?
- **Rastreamento de pose corporal** — posição, movimento, gesto
- **Expressão facial** — estado emocional inferido
- **Profundidade espacial** — distância e volumetria do espaço

Tecnologias em investigação:
- **MediaPipe** — detecção de pose, mãos, face; roda localmente, baixa latência
- **YOLO** — detecção de objetos e pessoas em tempo real
- **SAM (Segment Anything, Meta)** — segmentação semântica de qualquer elemento visual
- **Câmeras de profundidade** — Intel RealSense, Microsoft Azure Kinect; adicionam dimensão Z ao espaço

Questão em aberto: quanto o oráculo precisa "ver"? Presença e movimento podem ser suficientes. Ou ele precisa reconhecer rosto, intenção, identidade?

### 1.2 Escuta

O oráculo ouve o ambiente. O que se extrai do som:

- **Fala** — o que foi dito; transcrição e intenção
- **Emoção vocal** — tom, ritmo, intensidade
- **Som ambiente** — ruído, silêncio, textura sonora do espaço

Tecnologias em investigação:
- **Whisper (OpenAI)** — transcrição de fala em tempo real, multilíngue, roda localmente
- **Análise de frequência** — FFT ao vivo para extração de características sonoras
- **Detecção de emoção vocal** — modelos específicos, ainda em avaliação
- **Max/MSP, SuperCollider** — ambientes de processamento de áudio ao vivo com alta expressividade

---

## 2. Interpretação — A mente do oráculo

Esta camada recebe os dados brutos da percepção e produz significado. É aqui que o oráculo decide o que o mundo está dizendo.

### 2.1 Camada de raciocínio — LLM

Um modelo de linguagem grande atua como motor simbólico: recebe inputs multimodais (transcrições, dados de pose, descrições de cena) e produz uma interpretação — e uma intenção de resposta.

Questões em aberto:
- Qual modelo? Modelos locais (Llama, Mistral) vs. API (Claude, GPT-4o) — trade-off entre latência, custo e capacidade
- O LLM é o único ponto de decisão ou há lógicas paralelas (regras, estados, memória)?
- O oráculo tem memória de sessão? De sessões anteriores? Lembra de quem já esteve diante dele?
- Qual é o "personagem" do oráculo — como ele interpreta e qual é sua voz?

### 2.2 Integração multimodal

Como combinar visão + áudio + contexto em um único input para o LLM ou sistema de decisão:
- Modelos multimodais nativos (GPT-4o, Claude com visão) recebem imagem + texto
- Pipelines compostos: cada modalidade processada separadamente, resultado concatenado

---

## 3. Saída — Expressão

O oráculo responde. A resposta é sempre dupla: imagem e som.

### 3.1 Expressão visual

O que o oráculo mostra:

- Imagens geradas em resposta à percepção
- Vídeo gerado ou transformado em tempo real
- Visuais procedurais e generativos contínuos

Tecnologias em investigação:
- **StreamDiffusion** — diffusion em tempo real, latência de frames; mais adequado para fluxo contínuo
- **ComfyUI** — pipelines de diffusion modulares; flexível, não nativo para tempo real mas otimizável
- **ControlNet** — condicionamento da geração por pose, profundidade, bordas — conecta diretamente à percepção
- **Runway Gen-3** — geração de vídeo de alta qualidade, latência maior
- **TouchDesigner / VVVV / Notch** — ambientes de síntese visual procedural em tempo real; não generativos por IA mas altamente expressivos e de baixíssima latência

Questão em aberto: geração por IA (diffusion) vs. síntese procedural vs. combinação dos dois. São registros visuais muito diferentes.

### 3.2 Expressão sonora

O que o oráculo fala ou soa:

- Voz sintetizada — o oráculo fala?
- Música ou textura sonora gerada
- Som como resposta emocional ou atmosférica, não necessariamente verbal

Tecnologias em investigação:
- **ElevenLabs** — voice cloning e síntese de fala expressiva; latência baixa via API
- **AudioCraft (Meta)** — geração de música e efeitos sonoros por texto; MusicGen, AudioGen
- **Síntese granular** — técnica de síntese que fragmenta e reconstrói som; altamente expressiva
- **Max/MSP, SuperCollider** — síntese ao vivo, reatividade total a parâmetros em tempo real

---

## 4. Renderização em tempo real

Camada que integra expressão visual e a apresenta na tela, projeção ou superfície final. Pode ser o ambiente onde tudo roda, ou apenas a camada de saída.

Tecnologias em investigação:
- **TouchDesigner** — ambiente visual de dataflow, integração nativa com OSC/NDI/Syphon, síntese procedural, referência no campo de arte interativa
- **Unreal Engine 5** (Nanite + Lumen) — renderização fotorrealista em tempo real; overhead maior, mas capacidade visual incomparável
- **VVVV** — visual programming environment, forte em instalações interativas
- **Notch** — ferramenta focada em VFX ao vivo, usada em shows e instalações
- **WebGPU** — renderização na web com acesso direto à GPU; viabiliza instalações sem software proprietário

---

## 5. Presença física

Como o oráculo habita o espaço. Esta é a camada de maior abertura conceitual — ver documento específico quando a pesquisa avançar.

Direções em investigação:
- **Video mapping** — projeção sobre superfícies irregulares; a superfície vive
- **Volumes de LED** — presença luminosa escultórica; brilho em qualquer ambiente
- **Hologramas (ilusão óptica)** — Pepper's Ghost, ventiladores LED; flutuação e imaterialidade
- **Fog screen / névoa** — projeção em partículas; a imagem existe sem superfície
- **OLED transparente** — camadas sobrepostas de realidade; tecnologia emergente
- **Realidade aumentada** — o oráculo existe apenas mediado por dispositivo

A tensão entre presença física e imaterialidade permanece em aberto como questão norteadora do projeto.

---

## 6. Integração — conectando os módulos

Os sistemas acima são heterogêneos — rodam em ambientes diferentes, com linguagens e protocolos diferentes. Esta camada os conecta.

Protocolos em investigação:
- **OSC (Open Sound Control)** — protocolo padrão para comunicação entre ferramentas de arte digital; suportado por TouchDesigner, Max/MSP, SuperCollider, Unity e outros
- **NDI (Network Device Interface)** — transporte de vídeo de alta qualidade via rede local; conecta geração de imagem à renderização
- **Syphon (macOS) / Spout (Windows)** — compartilhamento de texturas GPU entre aplicações na mesma máquina; latência quase zero
- **WebSockets / HTTP** — para integração com APIs de LLM e serviços externos

Questão em aberto: arquitetura centralizada (um orquestrador) vs. distribuída (módulos autônomos se comunicando). Impacto direto em latência, robustez e complexidade.

---

## Questões transversais

Perguntas que atravessam todos os módulos e precisarão ser respondidas ao longo da pesquisa:

- **Latência** — quanto atraso é aceitável entre percepção e resposta? O oráculo precisa ser instantâneo ou pode ter uma cadência própria, mais lenta e ritualística?
- **Hardware** — qual máquina roda o sistema? GPU local vs. cloud vs. híbrido?
- **Autonomia** — o oráculo funciona sozinho durante uma exposição? Qual é o plano para falhas?
- **Identidade** — o oráculo tem um personagem estável ou ele emerge da interação?
- **Memória** — o oráculo aprende com as interações? Reconhece visitantes recorrentes?

---

*Documento vivo. Atualizar conforme a pesquisa avança.*
