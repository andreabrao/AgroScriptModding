# Chassis, ILS and Transmission Spec

## Direcao tecnica

O conjunto de chassi, ILS e transmissao e o centro de credibilidade do trator. Mesmo que parte dele fique parcialmente escondida por capô, rodas e cabine, o jogador percebe quando a estrutura tem massa, conexoes coerentes e animacao funcional.

## Chassi monobloco

### Volume principal

```text
Comprimento estrutural: 5.35 m
Largura central: 1.05 m
Altura media: 0.42 m
Eixo dianteiro: Y = +1.525
Eixo traseiro: Y = -1.525
```

### Detalhes obrigatorios

- Longarinas com chanfrados e espessura aparente.
- Travessas soldadas/parafusadas.
- Pontos de fixacao do motor.
- Pontos de fixacao da transmissao.
- Suporte frontal para lastro.
- Suportes laterais para escadas e cabine.
- Furos, tampas e parafusos grandes em areas visiveis.

## Transmissao e23

### Forma base

A carcaca da e23 deve parecer uma peça de fundicao pesada, nao uma caixa lisa:

- Corpo principal central.
- Tampa lateral esquerda e direita.
- Nervuras diagonais e verticais.
- Flange frontal para motor.
- Flange traseira para diferencial.
- Saida inferior/frontal para cardan dianteiro.
- Parafusos em anel nas tampas.

### Bake

Detalhes de fundicao, porosidade leve, nervuras e parafusos podem ser high-poly para bake em normal map.

## ILS dianteiro

### Estrutura visual

O ILS precisa comunicar suspensao independente real:

- Subframe central robusto.
- Diferencial dianteiro central.
- Braco superior esquerdo e direito.
- Braco inferior esquerdo e direito.
- Manga/cubo de cada roda.
- Cilindros com camisa e haste.
- Link de direcao.
- Eixo/cardans curtos ate os cubos.

### Separacao de objetos

```text
hp_ils_subframe
hp_front_differential_case
hp_ils_upper_arm_l
hp_ils_upper_arm_r
hp_ils_lower_arm_l
hp_ils_lower_arm_r
hp_ils_cylinder_body_l
hp_ils_cylinder_rod_l
hp_ils_cylinder_body_r
hp_ils_cylinder_rod_r
hp_steering_knuckle_l
hp_steering_knuckle_r
hp_front_hub_l
hp_front_hub_r
hp_steering_link_l
hp_steering_link_r
hp_front_driveshaft
hp_front_halfshaft_l
hp_front_halfshaft_r
```

## Materiais

| Material | Uso |
| --- | --- |
| `mat_hp_chassis_dark_metal` | Longarinas, travessas, suportes |
| `mat_hp_cast_transmission` | Carcaca e23, diferencial, mangas |
| `mat_hp_hydraulic_body` | Camisa dos cilindros |
| `mat_hp_chrome_rod` | Hastes cromadas |
| `mat_hp_bolt_metal` | Parafusos, pinos e arruelas |
| `mat_hp_grease_dark` | Juntas, coifas e pontos escuros |

## Animacao e pivots

### Bracos ILS

- Pivot na fixacao do chassi.
- Eixo local deve favorecer rotacao vertical.
- Braco nao deve compartilhar malha com o subframe.

### Manga/cubo

- Pivot no centro de esterco.
- Cubo deve ficar separado da manga para aceitar rotacao da roda.
- Link de direcao deve apontar visualmente para a manga.

### Cilindros

- Camisa e haste separadas.
- Haste deve apontar para o ponto movel do braco.
- Deixar empties nas duas extremidades para constraint futura.

## Low-poly futuro

Na etapa game-ready:

- Manter silhueta dos bracos e cubos.
- Bakear nervuras e parafusos pequenos.
- Simplificar interior da transmissao escondido pelo chassi.
- Manter cilindros com geometria suficiente para reflexo.
- Reduzir faces em suportes pouco visiveis.

## Riscos comuns

- Fazer o ILS como peça unica e perder animacao.
- Pivots fora dos pontos reais.
- Cardan atravessando a transmissao.
- Cubo dianteiro desalinhado com pneu do Passo 02.
- Transmissao lisa demais, sem leitura de fundicao.
- Chassi fino demais para a classe de potencia do 8R.
