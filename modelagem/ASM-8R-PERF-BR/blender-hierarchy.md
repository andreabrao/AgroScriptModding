# Hierarquia Blender / DCC

## Unidade e escala

- Unidade: metros.
- Escala do objeto raiz: `1, 1, 1`.
- Frente do trator: eixo `+Y`.
- Altura: eixo `+Z`.
- Origem principal: centro do chassi, alinhado ao solo em `Z = 0`.

## Colecoes principais

```text
ASM_8R_PERF_BR
  00_reference
  01_blockout
  02_high_poly
    body
    engine_powertech_9l
    chassis_transmission
    ils_front_axle
    rear_hitch_hydraulics
    wheels_tires
    cab_exterior
    cab_interior
    lights
    weights
    asm_customs
  03_game_ready
    lod0
    lod1
    lod2
    collision
  04_bake
    cages
    low_targets
    high_sources
  05_textures
  06_export_i3d
```

## Objetos raiz para jogo

```text
vehicle_root
  body_root
  chassis_root
  engine_root
  cab_root
    cab_interior_root
  wheel_front_l
  wheel_front_r
  wheel_rear_l_outer
  wheel_rear_l_inner
  wheel_rear_r_outer
  wheel_rear_r_inner
  ils_front_axle
  rear_hitch_root
  front_weight_root
  lights_root
```

## Padrao de nomes

Use prefixos curtos e consistentes:

- `hp_` para high-poly.
- `lp_` para game-ready.
- `col_` para collision mesh.
- `mat_` para materiais.
- `tex_` para texturas.
- `empty_` para pivots/empties.

Exemplos:

```text
hp_powertech_block_9l
hp_turbo_aftercooler
lp_body_hood_lod0
lp_rear_hitch_arm_left
col_chassis_main
empty_ils_upper_arm_l_pivot
mat_jd_green_clearcoat
tex_asm8r_body_basecolor_4k
```

## Pivots obrigatorios

| Parte | Pivot |
| --- | --- |
| Rodas | Centro do eixo de rotacao |
| Bracos ILS | Ponto de articulacao no chassi |
| Manga de eixo | Centro de esterco |
| Cilindros hidraulicos | Base da camisa e haste separadas |
| Levante traseiro | Ponto real de articulacao no chassi |
| Barra de tracao | Centro de oscilacao |
| Volante | Centro da coluna |
| Assento | Centro de giro do assento |
| Portas | Linha de dobradica |

## Separacao high-poly vs game-ready

O high-poly deve manter parafusos, soldas, vincos e detalhes reais. O game-ready deve receber bake desses detalhes e preservar geometria apenas onde o jogador ve de perto:

- Interior de cabine.
- Pneus e rodas.
- Levante traseiro.
- Motor visivel.
- Pesos e escape ASM.
- Grade e conjunto de farois.

## Materiais sugeridos

```text
mat_jd_green_clearcoat
mat_jd_yellow_rims
mat_chassis_dark_metal
mat_engine_cast_metal
mat_black_rubber
mat_cab_glass
mat_led_lens
mat_stainless_exhaust
mat_cast_iron_weights
mat_asm_decals
```

## Observacoes para animacao

- Nao aplique transforms finais em objetos animaveis sem validar pivots.
- Bracos, hastes e cilindros precisam ser objetos separados.
- Pneus duplos devem permitir configuracao por visibilidade.
- Luzes devem ficar separadas por tipo: farol, trabalho, freio, pisca, auxiliar ASM.
- Interior deve ser separado da cabine externa para otimizar LODs.
