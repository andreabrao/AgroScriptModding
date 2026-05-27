# Production Pass 03 - Chassi, ILS e Transmissao

## Objetivo deste passo

Criar a base high-poly funcional do conjunto estrutural do `ASM-8R-PERF-BR`:

- Chassi monobloco pesado.
- Carcaca externa da transmissao e23.
- Diferencial dianteiro e traseiro.
- Sistema ILS dianteiro com bracos, cubos, mangas, links e cilindros separados.
- Cardans e pontos de transmissao visual.
- Pivots/empties para animacao futura no Farming Simulator.

## Arquivo de partida

Use o script:

```text
scripts/create_asm8r_chassis_ils_transmission.py
```

No Blender:

1. Abra o blockout aprovado ou um arquivo novo.
2. Va em `Scripting`.
3. Abra `create_asm8r_chassis_ils_transmission.py`.
4. Clique em `Run Script`.
5. Salve como:

```text
modelagem/ASM-8R-PERF-BR/blender/ASM_8R_PERF_BR_highpoly_chassis_ils_v001.blend
```

## Componentes obrigatorios

### Chassi

- Longarinas centrais robustas.
- Travessas frontal, central e traseira.
- Suportes de motor e transmissao.
- Suporte para lastro dianteiro.
- Suportes para cabine.
- Pontos de fixacao do ILS.

### Transmissao e23

- Carcaca externa volumosa.
- Tampas laterais.
- Parafusos e nervuras de fundicao.
- Conexao com motor PowerTech e diferencial traseiro.
- Saida para cardan dianteiro.

### ILS dianteiro

- Subframe dianteiro.
- Diferencial dianteiro.
- Bracos superiores esquerdo/direito.
- Bracos inferiores esquerdo/direito.
- Manga de eixo esquerda/direita.
- Cubo de roda esquerdo/direito.
- Cilindros de suspensao com camisa e haste separadas.
- Links de direcao.
- Cardan dianteiro.

## Regras de animacao

- Cada parte movel deve ser objeto separado.
- Cada objeto movel deve ter `empty_..._pivot` no eixo correto.
- Cilindro hidraulico deve ter camisa e haste separadas.
- Cubo e manga de eixo devem permitir esterco independente.
- Bracos ILS devem permitir movimento vertical sem atravessar o chassi.
- Cardan deve ficar separado para animacao/rotacao visual se necessario.

## Pivots minimos

| Pivot | Local |
| --- | --- |
| `empty_ils_upper_arm_l_pivot` | Fixacao do braco superior esquerdo no chassi |
| `empty_ils_upper_arm_r_pivot` | Fixacao do braco superior direito no chassi |
| `empty_ils_lower_arm_l_pivot` | Fixacao do braco inferior esquerdo no chassi |
| `empty_ils_lower_arm_r_pivot` | Fixacao do braco inferior direito no chassi |
| `empty_steering_knuckle_l_pivot` | Centro da manga esquerda |
| `empty_steering_knuckle_r_pivot` | Centro da manga direita |
| `empty_front_diff_input_pivot` | Entrada do diferencial dianteiro |
| `empty_front_driveshaft_pivot` | Linha do cardan dianteiro |

## Checklist de aprovacao

- [ ] O conjunto suporta visualmente o peso do trator.
- [ ] ILS separado em componentes animaveis.
- [ ] Bracos superiores e inferiores nao se cruzam.
- [ ] Cubos dianteiros alinham com o rodado do Passo 02.
- [ ] Transmissao e23 tem volume, tampas e nervuras.
- [ ] Cardans e diferenciais existem como objetos separados.
- [ ] Pivots estao nomeados e posicionados.
- [ ] Materiais separados para chassi, fundicao, haste cromada e parafusos.
- [ ] Malha high-poly tem detalhes suficientes para bake.

## Proximo passo apos aprovar

`Production Pass 04 - Motor PowerTech 9.0 L, Turbo-Aftercooler e Exaustao ASM`.
