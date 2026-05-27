# Cab CommandView III and Interior Spec

## Direcao tecnica

A cabine e a parte que mais aparece em camera interna. O objetivo e equilibrar detalhe visual e organizacao para LOD: o interior deve parecer completo, mas com objetos agrupaveis e texturas planejadas para bake.

## Envelope de modelagem

```text
Centro da cabine: Y = -1.12
Largura externa: 1.90 m
Comprimento externo: 1.90 m
Altura ate teto: 3.30 m
Altura piso interno: 1.48 m
Assento: X = -0.18, Y = -1.22, Z = 1.78
CommandARM: X = 0.42, Y = -1.12, Z = 1.84
Display G5: X = 0.50, Y = -0.82, Z = 2.10
Volante: X = 0.00, Y = -0.54, Z = 1.98
```

## Cabine externa

### Casco e colunas

- Coluna A esquerda/direita.
- Coluna B esquerda/direita.
- Coluna C esquerda/direita.
- Estrutura do teto.
- Base de cabine.
- Porta esquerda/direita separada.
- Dobradiças e maçanetas.

### Vidros

Objetos separados:

```text
hp_cab_glass_front
hp_cab_glass_rear
hp_cab_glass_door_l
hp_cab_glass_door_r
hp_cab_glass_side_l
hp_cab_glass_side_r
```

Regras:

- Material transparente separado.
- Espessura visual com bevel leve.
- Nao unir vidro ao casco.
- Preparar mask de sujeira no vidro.

## Interior

### ActiveSeat II

Separar:

```text
hp_active_seat_base
hp_active_seat_cushion
hp_active_seat_backrest
hp_active_seat_headrest
hp_active_seat_left_armrest
hp_active_seat_right_armrest
hp_active_seat_suspension_scissor
```

Regras:

- Pivot de giro no centro da base.
- Encosto com volume e costura planejada para normal map.
- Apoio direito alinhado ao CommandARM.

### CommandARM

Componentes:

- Apoio de braco.
- Console lateral.
- Joystick principal.
- Botoes e seletores.
- Alavanca/knob rotativo.
- Display G5 em suporte.

### Display G5

- Tela separada com material proprio.
- Moldura preta.
- Suporte articulado.
- Textura futura para interface.

### Volante e comandos

- Volante separado.
- Coluna telescopica/inclinavel.
- Dashboard frontal.
- Pedais de freio/acelerador.
- Vents e botoes principais.

## Materiais

| Material | Uso |
| --- | --- |
| `mat_hp_cab_green` | Casco externo e teto |
| `mat_hp_cab_glass` | Vidros |
| `mat_hp_interior_dark_plastic` | Painel, console, portas internas |
| `mat_hp_seat_fabric` | Assento e encosto |
| `mat_hp_rubber_floor` | Piso e pedais |
| `mat_hp_screen_g5` | Tela do display |
| `mat_hp_bolt_metal` | Dobradiças, parafusos e suportes |

## Bake e textura

### Normal map

Priorizar:

- Costuras do assento.
- Botoes do CommandARM.
- Textura do piso.
- Vents do painel.
- Dobradiças e maçanetas.
- Moldura do display.

### Dirt/Wear

Areas com uso:

- Piso e tapete.
- Degrau/soleira da porta.
- Apoios de braço.
- Base do assento.
- Volante.
- Maçanetas.

## Camera interna

Criar empty:

```text
empty_interior_camera_reference
```

Posicao sugerida:

```text
X = -0.16
Y = -1.03
Z = 2.22
```

Esse empty serve para revisar se display, volante, painel e capo ficam com boa leitura.

## Riscos comuns

- Interior parecer vazio em primeira pessoa.
- Vidros unidos ao casco, dificultando shader.
- Console CommandARM generico demais.
- Display muito pequeno ou colado em lugar errado.
- Volante sem pivot.
- Assento sem pivot de giro.
- Portas sem dobradica/pivot.
- Muitos botoes como geometria final sem plano de LOD/bake.
