# Reference Scale Data

## Modelo base

Base tecnica usada para o blockout: John Deere 8R 410, Serie 8R acima de 2020.

## Dados oficiais aplicados no blockout

| Item | Valor usado | Observacao |
| --- | ---: | --- |
| Potencia nominal | 410 hp | Modelo 8R 410 |
| Potencia maxima | 443 hp | Referencia visual de classe/potencia |
| Motor | PowerTech 9.0 L | Base para volume do compartimento do motor |
| Transmissao | e23 PowerShift / EVT | Modelar carcaca externa e espaco de transmissao |
| Entre-eixos ILS | 3.050 m | Usado como distancia entre centros dos eixos |
| Entre-eixos MFWD | 3.080 m | Mantido como referencia alternativa |
| Comprimento total | 6.636 m | Usado para envelope geral |
| Peso base ILS/e23 | 12.700 kg | Base para aspecto de massa visual |
| Lastro maximo permissivel | 20.000 kg | Referencia para visual Performance BR pesado |
| Bomba hidraulica | 227.1 L/min ou 318 L/min | Suporte ao bloco VCR detalhado |
| Levante traseiro Cat. 4N/3 | 9.072 kg em 610 mm | Visual de levante pesado |

## Envelope visual do asset

Estes valores guiam o blockout e nao substituem modelagem por blueprint:

```text
Comprimento: 6.636 m
Largura visual com duplo traseiro ASM: 3.20 m a 3.45 m
Altura visual ate teto: 3.45 m a 3.60 m
Entre-eixos ILS: 3.050 m
Diametro pneu traseiro 800/70R38 aproximado: 2.08 m
Diametro pneu dianteiro aproximado: 1.55 m a 1.70 m
```

## Sistema de coordenadas do blockout

```text
Frente do trator: +Y
Traseira do trator: -Y
Altura: +Z
Lateral direita: +X
Origem: centro do chassi no solo
Eixo dianteiro: Y = +1.525
Eixo traseiro: Y = -1.525
```

## Decisoes ASM Performance BR

- Rodado traseiro duplo aumenta a largura visual acima da configuracao base.
- Discos de peso de roda sao modelados em ambos os lados da roda traseira.
- 22 pesos frontais de 50 kg sao representados no blockout como blocos individuais.
- Escape inox de maior diametro recebe silhueta propria desde o blockout.
- Barra LED e farois auxiliares entram como volumes separados desde o inicio.

## Fontes oficiais consultadas

- John Deere 8R 410 Tractor: https://www.deere.com/en/tractors/row-crop-tractors/row-crop-8-family/8r-410-tractor/
- John Deere 8R/8RT/8RX Engine Power: https://www.deere.com/en/tractors/row-crop-tractors/row-crop-8-family/power-efficiency/
- John Deere Latin America 8R 410 wheel weights: https://www.deere.com/latin-america/es/tractores/tractores-grandes/8r-rt-rx-serie/8r410/
