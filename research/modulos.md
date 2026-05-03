# Módulos do sistema — visão geral

> Documento de pesquisa aberta. Seções marcadas com **[DECIDIDO]** refletem escolhas já tomadas.

O Oraculum é um sistema de ponta a ponta: percebe o mundo, interpreta o que percebeu, e responde com som e imagem. Esta página mapeia os módulos que compõem esse fluxo, das entradas até os resultados, e as tecnologias sendo investigadas em cada camada.

---

## Fluxo geral

```
[ ENTRADA ]  →  [ INTERPRETAÇÃO ]  →  [ DECISÃO ]  →  [ SAÍDA ]  →  [ PRESENÇA FÍSICA ]
  percepção       processamento        lógica / IA    expressão      manifestação
                        ↕
               [ BANCO DE DADOS VIVO ]
                       memória
```

---

## Princípio de arquitetura **[DECIDIDO]**

O sistema deve ser **modular e substituível**. A IA evolui rápido — qualquer modelo em qualquer camada deve poder ser trocado por um mais rápido ou mais poderoso com o mínimo de fricção. Nenhum módulo deve ser acoplado ao modelo específico que o implementa. A interface entre módulos é o que importa, não a implementação interna.

---

## 1. Entrada — Percepção

O oráculo percebe o máximo possível do que acontece ao seu redor.

### 1.1 Visão **[DECIDIDO]**

O oráculo vê o máximo que a tecnologia permite. Não há limitação intencional de percepção — o escopo é perceber presença, movimento, pose, expressão facial, profundidade espacial e identidade. A decisão de *o que fazer* com cada dado é da camada de interpretação, não desta.

O que esta camada extrai:

- **Detecção de presença** — alguém está na sala? quantas pessoas?
- **Rastreamento de pose corporal** — posição, movimento, gesto
- **Expressão facial** — estado emocional inferido
- **Profundidade espacial** — distância e volumetria do espaço
- **Reconhecimento facial** — identidade de quem está diante do oráculo; base para memória persistente

Tecnologias em investigação:
- **MediaPipe** — detecção de pose, mãos, face; roda localmente, baixa latência
- **YOLO** — detecção de objetos e pessoas em tempo real
- **SAM (Segment Anything, Meta)** — segmentação semântica de qualquer elemento visual
- **Câmeras de profundidade** — Intel RealSense, Microsoft Azure Kinect; adicionam dimensão Z ao espaço
- **Modelos de reconhecimento facial** — DeepFace, InsightFace; para identificar e guardar pessoas no banco de dados vivo

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

Esta camada recebe os dados brutos da percepção e produz significado. É aqui que o oráculo decide o que o mundo está dizendo — e alimenta o banco de dados vivo com o que aprendeu.

### 2.1 Camada de raciocínio — LLM

Um modelo de linguagem grande atua como motor de raciocínio: recebe tudo que o oráculo percebeu (o que foi dito, como a pessoa se movia, como ela parecia, o que o banco de dados sabe sobre ela) e produz uma interpretação — e uma intenção de resposta.

Questões em aberto:
- Qual modelo? Modelos locais (Llama, Mistral) vs. API (Claude, GPT-4o) — trade-off entre latência, custo e capacidade. A arquitetura deve permitir trocar o modelo sem reescrever o sistema.
- O LLM é o único ponto de decisão ou há lógicas paralelas (regras, estados)?
- Qual é o "personagem" do oráculo — como ele interpreta e qual é sua voz?

### 2.2 Integração multimodal

Como combinar visão + áudio + memória do banco de dados em uma única entrada para o modelo de linguagem:
- Modelos multimodais nativos (GPT-4o, Claude com visão) recebem imagem + texto diretamente
- Pipelines compostos: cada modalidade processada separadamente, resultado concatenado antes do LLM

---

## 3. Banco de dados vivo — Memória do oráculo **[DECIDIDO]**

O oráculo tem memória. Cada encontro gera informações que são guardadas e consultadas nos encontros seguintes. O banco de dados é alimentado pela camada de interpretação a cada ciclo.

O que o banco de dados guarda:

- **Identidades** — rostos reconhecidos, embeddings faciais, primeira vez que apareceram, quantas vezes retornaram
- **Histórico de interações** — o que foi dito, o que o oráculo respondeu, contexto da sessão
- **Estado emocional observado** — por pessoa, ao longo do tempo
- **Presenças** — quando cada pessoa esteve diante do oráculo, por quanto tempo

O que o banco de dados permite:

- O oráculo reconhece quem já conhece
- O oráculo lembra do que aconteceu antes
- O oráculo pode tratar um retornante de forma diferente de um estranho
- A história do oráculo cresce com o tempo — ele envelhece, acumula

Tecnologias em investigação para o banco de dados:
- **SQLite** — leve, local, sem servidor; adequado para instalações isoladas
- **PostgreSQL com pgvector** — para armazenar e buscar embeddings faciais por similaridade
- **Redis** — para estado de sessão em tempo real (quem está na frente agora)
- **Embeddings faciais** — representações vetoriais de rostos; permitem busca por similaridade sem armazenar imagens

Questão em aberto: privacidade e consentimento. O oráculo que lembra de rostos levanta questões éticas e legais em espaços públicos. Como comunicar isso ao visitante? O apagamento de identidade é uma opção que o visitante pode escolher?

---

## 4. Saída — Expressão

O oráculo responde. A resposta é sempre dupla: imagem e som.

### 4.1 Expressão visual

O que o oráculo mostra:

- Imagens geradas em resposta à percepção
- Vídeo gerado ou transformado em tempo real
- Visuais procedurais e generativos contínuos
- Um avatar — o corpo e o rosto do oráculo

Tecnologias em investigação:
- **StreamDiffusion** — geração de imagem em tempo real, latência de frames; mais adequado para fluxo contínuo
- **ComfyUI** — criação de imagem por etapas modulares; flexível, não nativo para tempo real mas otimizável
- **ControlNet** — condicionamento da geração por pose, profundidade, bordas — conecta diretamente à percepção
- **Runway Gen-3** — geração de vídeo de alta qualidade, tempo de resposta maior
- **TouchDesigner / VVVV / Notch** — ambientes de síntese visual em tempo real; não por inteligência artificial, mas altamente expressivos e de resposta imediata

Questão em aberto: geração por inteligência artificial vs. síntese visual direta vs. combinação dos dois. São registros visuais muito diferentes.

### 4.2 Avatar — O corpo do oráculo

O oráculo pode ter um rosto, um corpo, uma presença visual contínua — não apenas imagens geradas em resposta, mas uma figura que existe, olha, e fala. Esta direção muda o caráter da instalação: o oráculo deixa de ser um fenômeno e passa a ser uma entidade.

Questões conceituais em aberto:
- O avatar tem forma humana, ou é algo entre humano e não-humano?
- O rosto do oráculo é estável — sempre o mesmo — ou muda com cada visitante ou ao longo do tempo?
- O lipsync (movimento da boca sincronizado com a fala) é essencial para a sensação de presença, ou cria uma ilusão que conflita com o caráter oracular?
- Esta direção reforça presença física ou imaterialidade?

Caminhos técnicos em investigação:

**Avatar 3D em tempo real**
- **MetaHuman (Unreal Engine 5)** — avatares humanos fotorrealistas criados e animados em tempo real; lipsync nativo com MetaHuman Animator; exige hardware potente
- **NVIDIA Audio2Face** — anima automaticamente o rosto de um avatar a partir do áudio em tempo real; integra com Unreal Engine e outras ferramentas
- **VRM / VRoid** — formato aberto de avatar 3D humanóide; ecossistema de ferramentas, mais leve que MetaHuman; origem no universo de VTubers
- **Ready Player Me** — criação de avatares 3D compatíveis com múltiplas plataformas; menos fotorrealista, mais estilizado

**Rosto falante (imagem animada)**
- **SadTalker** — anima uma imagem estática de rosto a partir do áudio; roda localmente
- **LivePortrait** — animação de retrato em tempo real com alta qualidade; roda localmente
- **Wav2Lip** — sincronização de lábios em vídeo a partir de qualquer áudio; mais técnico, menos expressivo

**Personagem conversacional com avatar**
- **Convai** — personagem de inteligência artificial com avatar 3D e voz em tempo real; voltado para jogos e instalações interativas
- **Inworld AI** — personagens com memória, emoção e avatar; mais voltado para entretenimento

**Síntese visual procedural com presença**
- Não um avatar humano, mas uma forma visual que "respira", reage e fala — construída em TouchDesigner ou similar, sem tentar imitar o humano

Questão em aberto: o avatar é renderizado localmente (mais controle, mais poder de processamento) ou via serviço externo (mais fácil, mais dependente de conexão)?

### 4.3 Expressão sonora

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

## 5. Renderização em tempo real

Camada que integra expressão visual e a apresenta na tela, projeção ou superfície final.

Tecnologias em investigação:
- **TouchDesigner** — ambiente visual de dataflow, integração nativa com OSC/NDI/Syphon, síntese procedural, referência no campo de arte interativa
- **Unreal Engine 5** (Nanite + Lumen) — renderização fotorrealista em tempo real; overhead maior, mas capacidade visual incomparável
- **VVVV** — visual programming environment, forte em instalações interativas
- **Notch** — ferramenta focada em VFX ao vivo, usada em shows e instalações
- **WebGPU** — renderização na web com acesso direto à GPU; viabiliza instalações sem software proprietário

---

## 6. Presença física

Como o oráculo habita o espaço. Esta é a camada de maior abertura conceitual.

Direções em investigação:
- **Video mapping** — projeção sobre superfícies irregulares; a superfície vive
- **Volumes de LED** — presença luminosa escultórica; brilho em qualquer ambiente
- **Hologramas (ilusão óptica)** — Pepper's Ghost, ventiladores LED; flutuação e imaterialidade
- **Fog screen / névoa** — projeção em partículas; a imagem existe sem superfície
- **OLED transparente** — camadas sobrepostas de realidade; tecnologia emergente
- **Realidade aumentada** — o oráculo existe apenas mediado por dispositivo

A tensão entre presença física e imaterialidade permanece em aberto como questão norteadora do projeto.

---

## 7. Integração — conectando os módulos

Protocolos em investigação:
- **OSC (Open Sound Control)** — protocolo padrão para comunicação entre ferramentas de arte digital
- **NDI (Network Device Interface)** — transporte de vídeo de alta qualidade via rede local
- **Syphon (macOS) / Spout (Windows)** — compartilhamento de texturas GPU entre aplicações; latência quase zero
- **WebSockets / HTTP** — para integração com APIs de LLM e serviços externos

Questão em aberto: arquitetura centralizada (um orquestrador) vs. distribuída (módulos autônomos se comunicando).

---

## Questões transversais

- **Latência** — quanto atraso é aceitável? O oráculo precisa ser instantâneo ou pode ter cadência própria, mais lenta e ritualística?
- **Hardware** — qual máquina roda o sistema? GPU local vs. cloud vs. híbrido?
- **Autonomia** — o oráculo funciona sozinho durante uma exposição? Qual é o plano para falhas?
- **Identidade** — o oráculo tem um personagem estável ou ele emerge da interação?
- **Privacidade** — como comunicar ao visitante que o oráculo o reconhece e o lembra?

---

*Documento vivo. Atualizar conforme a pesquisa avança.*
