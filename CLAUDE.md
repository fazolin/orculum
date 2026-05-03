# CLAUDE.md — Orientações para o Oraculum

Este arquivo orienta instâncias futuras do Claude Code que trabalharão neste repositório. Leia com atenção antes de qualquer ação.

---

## O que é este projeto

Oraculum é uma instalação de arte interativa — um oráculo contemporâneo que percebe o mundo (visão, som, movimento, fala) e responde com imagem e som gerados em tempo real. É um trabalho de arte. Não é um produto de software.

O repositório documenta um processo vivo de pesquisa conceitual e técnica. Nenhuma decisão tecnológica está finalizada. Nenhuma arquitetura foi definida.

Este é um **monorepo** — toda a pesquisa, documentação e implementação vivem aqui, nesta pasta. Não existe repositório separado para nenhum módulo.

---

## Princípio fundamental

**Pesquisa precede implementação.**

Não escreva código antes que a pesquisa de um campo esteja suficientemente madura para justificá-lo. "Suficientemente madura" significa: decisões de tecnologia documentadas, alternativas consideradas, implicações conceituais compreendidas.

Quando houver implementação, aplique boas práticas rigorosamente — clean code, separação de responsabilidades, nomes claros. A qualidade do código reflete o respeito pelo trabalho.

---

## A tensão norteadora

Uma questão central ainda em aberto guia a pesquisa da camada física:

> O oráculo deve ter **presença física** — algo que você pode quase tocar — ou **imaterialidade** — algo que parece não pertencer ao mundo físico?

Não resolva esta questão. Não incline a documentação para nenhum dos lados sem instrução explícita. Esta tensão *é* parte do trabalho — ela deve permanecer aberta e produtiva enquanto a pesquisa não a fechar naturalmente.

---

## Campos de investigação

O projeto se articula em cinco campos:

- **Percepção** — computer vision, áudio, voz; como o oráculo recebe o mundo
- **Inteligência** — LLMs, raciocínio simbólico, integração multimodal; como o oráculo interpreta
- **Expressão** — imagem generativa, síntese sonora, renderização em tempo real; como o oráculo responde
- **Presença física** — formas de manifestação no espaço (video mapping, LED, hologramas, fog screen, OLED, AR)
- **Integração** — protocolos e arquitetura entre sistemas (OSC, NDI, Syphon, Spout)

---

## Como contribuir para a documentação

- Registre o que foi encontrado, não apenas conclusões
- Inclua alternativas consideradas e por que foram ou não descartadas
- Cite fontes, ferramentas e referências com precisão — não invente
- Tangentes conceituais são bem-vindas — registre-as, não as descarte
- Use linguagem clara mas não simplificada; este é um trabalho técnico-artístico

---

## Tecnologias em pesquisa (não definitivas)

As tecnologias abaixo estão sendo investigadas. Nenhuma foi escolhida. Não trate nenhuma delas como decisão tomada sem evidência no repositório.

**Renderização em tempo real:** TouchDesigner, Unreal Engine 5, VVVV, Notch, WebGPU

**Computer vision:** MediaPipe, SAM (Segment Anything), YOLO, RealSense, Azure Kinect

**Áudio e voz:** Whisper, Max/MSP, SuperCollider

**Expressão sonora generativa:** AudioCraft, ElevenLabs, síntese granular

**Expressão visual generativa:** StreamDiffusion, ComfyUI, ControlNet, Runway Gen-3

**Inteligência:** LLMs (família a definir), integração multimodal

**Integração:** OSC, NDI, Syphon, Spout

**Presença física:** video mapping, volumes LED, Pepper's Ghost, fog screen, OLED transparente, AR

---

## O que não fazer

- Não tome decisões estruturais (pastas, arquitetura, convenções) sem instrução explícita do usuário
- Não invente tecnologias, ferramentas ou decisões que não estejam documentadas no repositório
- Não resolva a tensão entre presença física e imaterialidade — ela é parte do trabalho
- Não crie código sem instrução explícita
- Não simplifique questões conceituais abertas para fechar logo uma decisão
- Não descarte tangentes — registre-as

---

*Este documento deve ser atualizado à medida que o projeto evolui.*
