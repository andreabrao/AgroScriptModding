# Production Pass 09 - Integracao FS22/FS25, Entrega Final e Bloqueio

## Objetivo deste passo

Fechar a modelagem do `ASM-8R-PERF-BR` como pacote final de producao, pronto para exportacao I3D, configuracao no Giants Editor e montagem do mod para Farming Simulator 22/25.

Este passo encerra a modelagem tecnica. Depois dele nao entram novas alteracoes de design, proporcao, acessorios ou estrutura. A partir daqui, somente sao permitidos ajustes de exportacao, bugs, textura, XML e compatibilidade.

## Arquivo de partida

Use o script:

```text
scripts/create_asm8r_mod_skeleton.py
```

Execute com Python comum a partir da raiz do projeto ou pelo terminal:

```text
python modelagem/ASM-8R-PERF-BR/scripts/create_asm8r_mod_skeleton.py
```

O script cria uma pasta de exportacao inicial:

```text
modelagem/ASM-8R-PERF-BR/export/FS22_ASM_8R_PERF_BR/
```

## Estrutura final esperada

```text
FS22_ASM_8R_PERF_BR/
  modDesc.xml
  README_EXPORT.txt
  store/
    store_ASM_8R_PERF_BR.dds
    icon_ASM_8R_PERF_BR.dds
  vehicles/
    ASM_8R_PERF_BR.xml
    ASM_8R_PERF_BR.i3d
  textures/
    asm8r_body_4k_*.png
    asm8r_engine_chassis_4k_*.png
    asm8r_wheels_tires_4k_*.png
    asm8r_interior_4k_*.png
    asm8r_lights_2k_*.png
  sounds/
    README.txt
```

## Node plan para I3D

| Node | Uso |
| --- | --- |
| `ASM_8R_PERF_BR` | Raiz do veiculo |
| `visual` | Malhas visuais |
| `wheels` | Rodas e discos |
| `steering` | Conjunto estercante |
| `ils_front_axle` | Suspensao dianteira ILS |
| `rear_hitch` | Levante traseiro |
| `hydraulics` | Cilindros e mangueiras |
| `lights` | Luzes de fabrica e ASM |
| `cab_interior` | Interior CommandView III |
| `collisions` | Shapes de colisao |
| `attacherJoints` | Engates traseiros, barra e PTO |
| `cameras` | Camera externa e interna |

## XML minimo

O arquivo `vehicles/ASM_8R_PERF_BR.xml` deve receber, na fase de implementacao:

- Store data do trator.
- Configuracoes de rodas.
- Motor e transmissao.
- Sons.
- Luzes.
- Animacoes ILS.
- Steering e wheel setup.
- Attacher joints.
- Dirt/wear.
- Indoor camera.
- Interactive controls, se aplicavel.

## Criterios de bloqueio final

- Modelagem high-poly concluida.
- Low-poly e LODs planejados.
- UV e textura 4K especificadas.
- Luzes e emissives especificados.
- Interior CommandView finalizado.
- Peso frontal, rodas duplas e escapamento ASM incluidos.
- Sistema traseiro e hidraulico incluidos.
- Manifesto do projeto atualizado.
- Checklist final anexado.

## Resultado

O pacote entra em estado:

```text
FINAL MODELING PACKAGE LOCKED
```

Sem mais alteracoes de modelagem apos este passo.
