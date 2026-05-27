# Production Pass 05 - Levante Traseiro, Hidraulico, VCRs e Barra de Tracao

## Objetivo deste passo

Criar a base high-poly funcional do conjunto traseiro de trabalho do `ASM-8R-PERF-BR`:

- Levante traseiro Categoria 4N/3.
- Bracos inferiores esquerdo/direito.
- Terceiro ponto.
- Estabilizadores.
- Cilindros hidraulicos com camisa e haste separadas.
- Barra de tracao oscilante.
- PTO traseira e protecao.
- Bloco de VCRs com 4 ou 5 saidas.
- Engates rapidos, tampas, mangueiras e suportes.
- Pivots/empties para animacao e attacher joints futuros.

## Arquivo de partida

Use o script:

```text
scripts/create_asm8r_rear_hitch_hydraulics.py
```

No Blender:

1. Abra o arquivo do chassi/ILS aprovado ou um arquivo novo.
2. Va em `Scripting`.
3. Abra `create_asm8r_rear_hitch_hydraulics.py`.
4. Clique em `Run Script`.
5. Salve como:

```text
modelagem/ASM-8R-PERF-BR/blender/ASM_8R_PERF_BR_highpoly_rear_hitch_v001.blend
```

## Componentes obrigatorios

### Levante traseiro Categoria 4N/3

- Suporte central reforcado.
- Bracos inferiores com olhais.
- Terceiro ponto com rosca/ajuste visual.
- Estabilizadores laterais.
- Pinos e travas.
- Pontos para attacher joints.

### Hidraulico

- Cilindros principais esquerdo e direito.
- Camisa e haste separadas.
- Mangueiras saindo para o bloco VCR.
- Suportes e abraçadeiras.

### VCRs

- Bloco com 5 saidas visuais.
- Engates rapidos individuais.
- Tampas de protecao.
- Conectores coloridos discretos.
- Mangueiras curvas indo para a traseira.

### PTO e barra de tracao

- Eixo PTO com estrias simplificadas.
- Protecao/capa da PTO.
- Barra de tracao oscilante.
- Pino e trava.
- Suporte de arraste reforcado.

## Regras de animacao

- Bracos inferiores separados.
- Terceiro ponto separado.
- Cilindros com camisa e haste separadas.
- Barra de tracao separada para oscilacao.
- PTO separada para possivel rotacao.
- Empties para pivots e pontos de attacher.

## Pivots/empties minimos

| Pivot | Uso |
| --- | --- |
| `empty_rear_lower_link_l_pivot` | Rotacao do braco inferior esquerdo |
| `empty_rear_lower_link_r_pivot` | Rotacao do braco inferior direito |
| `empty_top_link_pivot` | Terceiro ponto |
| `empty_hitch_cylinder_l_base` | Base do cilindro esquerdo |
| `empty_hitch_cylinder_l_rod` | Ponta da haste esquerda |
| `empty_hitch_cylinder_r_base` | Base do cilindro direito |
| `empty_hitch_cylinder_r_rod` | Ponta da haste direita |
| `empty_drawbar_pivot` | Oscilacao da barra de tracao |
| `empty_pto_rotation_pivot` | Rotacao da PTO |
| `empty_attacher_rear_3pt` | Futuro attacher 3 pontos |
| `empty_attacher_drawbar` | Futuro attacher drawbar |

## Checklist de aprovacao

- [ ] O levante parece dimensionado para trator pesado.
- [ ] Bracos inferiores têm olhais, pinos e travas.
- [ ] Terceiro ponto tem volume e rosca/ajuste visual.
- [ ] Cilindros têm haste cromada separada.
- [ ] VCRs têm 5 saidas com engates rapidos.
- [ ] PTO e protecao estao presentes.
- [ ] Barra de tracao oscilante esta separada.
- [ ] Pivots/empties estao posicionados.
- [ ] Mangueiras nao atravessam chassi ou levante.
- [ ] Materiais separados para fundicao, cromado, borracha, engate e pinos.

## Proximo passo apos aprovar

`Production Pass 06 - Cabine CommandView III, Interior, ActiveSeat II e CommandARM`.
