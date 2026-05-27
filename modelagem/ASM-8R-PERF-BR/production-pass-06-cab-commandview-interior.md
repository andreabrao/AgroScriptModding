# Production Pass 06 - Cabine CommandView III, Interior, ActiveSeat II e CommandARM

## Objetivo deste passo

Criar a base high-poly da cabine e do interior do `ASM-8R-PERF-BR`, priorizando leitura realista em camera interna e organizacao para game-ready:

- Estrutura externa da cabine CommandView III.
- Vidros separados com espessura visual.
- Portas com pivots.
- Teto, colunas, para-lamas traseiros e espelhos.
- Interior completo para camera de jogador.
- Assento ActiveSeat II com base, suspensao e giro.
- Console CommandARM.
- Display G5.
- Volante inclinavel/telescopico.
- Pedais, painel, vents, botoes e comandos principais.

## Arquivo de partida

Use o script:

```text
scripts/create_asm8r_cab_commandview_interior.py
```

No Blender:

1. Abra o blockout aprovado ou um arquivo novo.
2. Va em `Scripting`.
3. Abra `create_asm8r_cab_commandview_interior.py`.
4. Clique em `Run Script`.
5. Salve como:

```text
modelagem/ASM-8R-PERF-BR/blender/ASM_8R_PERF_BR_highpoly_cab_interior_v001.blend
```

## Componentes obrigatorios

### Cabine externa

- Casco da cabine.
- Colunas A/B/C.
- Parabrisa frontal.
- Vidro traseiro.
- Vidros laterais.
- Portas esquerda/direita separadas.
- Dobradiças e puxadores.
- Teto com base para barra LED ASM futura.
- Espelhos laterais.
- Limpador de parabrisa.

### Interior

- Piso e tapete.
- Assento ActiveSeat II.
- Base/suspensao do assento.
- Apoios de braço.
- Console CommandARM.
- Joystick/comandos principais.
- Display G5 separado com material de tela.
- Volante e coluna.
- Pedais.
- Painel, vents e comandos auxiliares.

## Regras de animacao

- Portas separadas com pivot de dobradica.
- Volante separado com pivot no centro.
- Coluna do volante separada para inclinacao.
- Assento separado com pivot de giro.
- Display separado para material emissive/textura.
- Vidros separados do metal da cabine.

## Pivots/empties minimos

| Pivot | Uso |
| --- | --- |
| `empty_door_l_hinge_pivot` | Abrir porta esquerda |
| `empty_door_r_hinge_pivot` | Abrir porta direita |
| `empty_active_seat_rotation_pivot` | Giro do ActiveSeat II |
| `empty_steering_wheel_pivot` | Rotacao do volante |
| `empty_steering_column_tilt_pivot` | Inclinacao da coluna |
| `empty_g5_display_mount` | Referencia do display G5 |
| `empty_interior_camera_reference` | Referencia para camera interna |

## Checklist de aprovacao

- [ ] Silhueta externa da cabine confere com 8R moderno.
- [ ] Vidros têm objetos separados e leitura limpa.
- [ ] Porta esquerda e direita têm pivots.
- [ ] Assento tem base, encosto, apoios e suspensao.
- [ ] CommandARM tem joystick, botoes e apoio.
- [ ] Display G5 esta separado e posicionado no console.
- [ ] Volante e coluna estao separados.
- [ ] Pedais e painel existem para camera interna.
- [ ] Materiais separados para vidro, plastico, tecido, borracha, tela e metal.
- [ ] Interior nao atravessa vidro/cabine externa.

## Proximo passo apos aprovar

`Production Pass 07 - Luzes, eletrica, LED 360, barra ASM e acabamento externo`.
