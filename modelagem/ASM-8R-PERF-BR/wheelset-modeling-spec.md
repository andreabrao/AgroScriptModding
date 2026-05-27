# Wheelset Modeling Spec

## Rodado Performance BR

O rodado e uma assinatura visual do `ASM-8R-PERF-BR`. Ele deve comunicar trator pesado de lavoura grande brasileira: pneu largo, duplo traseiro, cubos reforcados e lastro maximo.

## Pneus traseiros 800/70R38

Calculo de referencia:

```text
Largura nominal: 800 mm
Perfil: 70%
Aro: 38 in = 965.2 mm
Altura do flanco: 800 * 0.70 = 560 mm
Diametro externo aproximado: 965.2 + (560 * 2) = 2085.2 mm
```

Dimensoes aplicadas no high-poly:

```text
Diametro externo: 2.085 m
Raio externo: 1.0425 m
Largura: 0.800 m
Raio do aro: 0.4826 m
Raio visual do aro no modelo: 0.58 m
```

## Pneus dianteiros

Referencia visual compativel com 8R pesado:

```text
Diametro externo: 1.640 m
Raio externo: 0.820 m
Largura: 0.650 m
Raio visual do aro: 0.45 m
```

## Garras e sulcos

### Traseiro

- 42 a 48 garras por pneu no high-poly.
- Garras em V alternado.
- Centro com canal sutil.
- Altura de garra sugerida: 0.055 m a 0.075 m.
- Garras devem passar levemente para o ombro do pneu.

### Dianteiro

- 34 a 40 garras.
- Perfil menos agressivo que o traseiro.
- Ombros fortes para leitura de peso no ILS.

## Flanco

Detalhes planejados para o passe de refinamento:

- Lettering da medida `800/70R38`.
- Marca generica ou marca licenciada conforme permissao.
- Setas de sentido de rotacao.
- Ranhuras radiais finas.
- Deformacao sutil na base por peso.

## Rodas e cubos

### Traseiro

- Aro amarelo John Deere.
- Prato interno com concavidade.
- Cubo central reforcado.
- Parafusos distribuidos radialmente.
- Discos de peso em ferro fundido nos lados interno e externo.
- Espaçadores para configuracao dupla.

### Dianteiro

- Aro amarelo menor.
- Cubo ILS destacado.
- Parafusos e prato central.
- Preparar pivot para esterco e rotacao.

## Materiais

| Material | Roughness | Metallic | Observacao |
| --- | ---: | ---: | --- |
| Borracha pneu | 0.82 | 0.00 | Normal forte e sujeira |
| Aro amarelo | 0.42 | 0.15 | Pintura semi-brilho |
| Cubo metalico | 0.55 | 0.65 | Metal pintado/gasto |
| Peso ferro fundido | 0.76 | 0.80 | Rugoso, escuro e pesado |
| Parafusos | 0.38 | 0.85 | Highlights pequenos |

## UV e bake

- Pneus podem usar simetria/tiling nas garras, mas flancos visiveis precisam de UV propria.
- Rodas devem ter UV unica para desgaste nos parafusos e bordas.
- Pesos devem ter UV propria para sujeira e ferrugem leve.
- Criar high-poly detalhado suficiente para bake em low-poly separado.

## Notas FS

- A malha high-poly nao deve ir diretamente para o jogo.
- Criar LOD0 game-ready depois do bake.
- Pivots de roda devem ficar no centro exato do eixo.
- Evitar objetos soltos sem nome; tudo deve começar com `hp_`, `lp_`, `empty_` ou `guide_`.
