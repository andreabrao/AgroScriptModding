# Rear Hitch and Hydraulics Spec

## Direcao tecnica

O conjunto traseiro precisa parecer capaz de puxar e levantar implementos pesados de lavoura grande. Ele deve ser mecanicamente legivel, animavel e preparado para os attacher joints do Farming Simulator.

## Layout geral

```text
Frente do trator: +Y
Traseira do trator: -Y
Centro do conjunto: Y = -3.05
Altura base dos bracos: Z = 0.62
Altura do terceiro ponto: Z = 1.36
PTO: Z = 0.72
Bloco VCR: lado direito visual, X = 0.64
```

## Levante traseiro Categoria 4N/3

### Bracos inferiores

- Comprimento visual: 1.05 m a 1.25 m.
- Perfil retangular pesado com chanfrados.
- Olhal traseiro com espessura.
- Pino/trava visual.
- Pivot na base do chassi.

### Terceiro ponto

- Barra central ajustavel.
- Corpo com rosca visual.
- Olhais nas duas pontas.
- Pivot superior no suporte central.

### Estabilizadores

- Links laterais conectando bracos inferiores ao suporte.
- Podem começar como cilindros/tubos.
- Separar esquerdo/direito.

## Cilindros hidraulicos

Cada cilindro deve ter:

```text
hp_hitch_cylinder_body_l
hp_hitch_cylinder_rod_l
hp_hitch_cylinder_body_r
hp_hitch_cylinder_rod_r
```

Regras:

- Camisa escura/metalica.
- Haste cromada.
- Pontas com olhais.
- Empties na base e na haste.

## VCRs e engates rapidos

### Bloco VCR

- 5 saidas visuais.
- Cada saida com anel externo, centro escuro e tampa.
- Pequenos codigos de cor podem ser texturizados depois.
- Mangueiras devem sair com curva natural.

### Objetos

```text
hp_rear_scv_block_5_outputs
hp_scv_quick_coupler_01 ... hp_scv_quick_coupler_05
hp_scv_cap_01 ... hp_scv_cap_05
hp_hydraulic_hose_01 ... hp_hydraulic_hose_05
```

## PTO e drawbar

### PTO

- Eixo cilíndrico com estrias simplificadas.
- Capa/protecao ao redor.
- Pivot proprio para rotacao.

### Barra de tracao

- Barra retangular pesada.
- Furo/pino traseiro.
- Suporte de oscilacao.
- Pivot central.

## Materiais

| Material | Uso |
| --- | --- |
| `mat_hp_hitch_cast` | Suportes, bracos, corpo do levante |
| `mat_hp_hydraulic_body` | Camisas dos cilindros |
| `mat_hp_chrome_rod` | Hastes cromadas |
| `mat_hp_rubber_hose` | Mangueiras |
| `mat_hp_quick_coupler` | Engates VCR |
| `mat_hp_pin_bolt` | Pinos, travas e parafusos |
| `mat_hp_pto_dark` | PTO e capa |

## Bake e texturas

### Normal map

Priorizar:

- Pinos e travas.
- Olhais dos bracos.
- Rosca do terceiro ponto.
- Engates rapidos.
- Estrias da PTO.
- Soldas e bordas do suporte.

### Dirt/Wear

Areas com sujeira forte:

- Bracos inferiores.
- Barra de tracao.
- Pinos e olhais.
- PTO.
- Base dos cilindros.
- Parte inferior do bloco VCR.

## Attacher joints futuros

Criar empties que depois podem guiar XML/I3D:

```text
empty_attacher_rear_3pt
empty_attacher_drawbar
empty_power_takeoff_rear
empty_hydraulic_connector_rear
```

## Riscos comuns

- Levante parecer pequeno para o porte 8R.
- VCRs virarem apenas textura plana.
- Cilindro ser peça unica, impedindo animacao.
- Barra de tracao grudada no chassi.
- PTO sem pivot.
- Mangueiras retas demais ou atravessando peças.
