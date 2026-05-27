# Production Pass 02 - Rodado, Pneus e Lastro de Rodas

## Objetivo deste passo

Criar a base high-poly do conjunto de rodados do `ASM-8R-PERF-BR`, priorizando o visual pesado da configuracao Performance BR:

- Pneus traseiros 800/70R38 em configuracao dupla.
- Pneus dianteiros largos compativeis com trator pesado.
- Rodas amarelas com cubos, parafusos e pratos.
- Discos de peso de ferro fundido nas rodas traseiras.
- Espaçadores e cubos para duplo traseiro.
- Sulcos e garras em geometria para bake de normal map.

## Arquivo de partida

Use o script:

```text
scripts/create_asm8r_wheelset_highpoly.py
```

No Blender:

1. Abra um arquivo novo ou o blockout aprovado.
2. Va em `Scripting`.
3. Abra `create_asm8r_wheelset_highpoly.py`.
4. Clique em `Run Script`.
5. Salve como:

```text
modelagem/ASM-8R-PERF-BR/blender/ASM_8R_PERF_BR_highpoly_wheels_v001.blend
```

## Especificacao dimensional usada

| Conjunto | Medida alvo | Uso |
| --- | ---: | --- |
| Traseiro | 800/70R38 | Rodado duplo Performance BR |
| Diametro traseiro aprox. | 2.085 m | Base para pneu high-poly |
| Largura traseira aprox. | 0.800 m | Banda larga com garras profundas |
| Dianteiro | 650/60R34 aprox. | Volume compativel com 8R pesado |
| Diametro dianteiro aprox. | 1.640 m | Balanceado com ILS |
| Largura dianteira aprox. | 0.650 m | Pneu largo mas sem exagero |

## Estrutura de objetos

```text
ASM_8R_PERF_BR_WHEELSET_HIGHPOLY
  rear_dual_wheels
    hp_tire_rear_l_outer_800_70r38
    hp_tire_rear_l_inner_800_70r38
    hp_tire_rear_r_inner_800_70r38
    hp_tire_rear_r_outer_800_70r38
    hp_rim_*
    hp_rear_cast_weight_disc_*
    hp_rear_dual_spacer_*
  front_wheels
    hp_tire_front_l_wide
    hp_tire_front_r_wide
    hp_rim_front_*
  bake_helpers
  scale_guides
```

## Checklist de aprovacao

- [ ] Traseira dupla parece pesada sem passar do limite visual do trator.
- [ ] Sulcos/garras têm altura suficiente para gerar normal map forte.
- [ ] Lados esquerdo e direito têm orientação de garra espelhada.
- [ ] Rodas amarelas têm prato interno, aro, cubo e parafusos.
- [ ] Discos de peso traseiro têm volume de ferro fundido.
- [ ] Espaçadores do duplo traseiro aparecem entre roda interna e externa.
- [ ] Pivots das rodas estão no centro do eixo.
- [ ] Nomes dos objetos seguem o padrao `hp_`.
- [ ] Materiais estão separados para borracha, aro, cubo, peso e metal.

## Proximo passo apos aprovar

Depois de aprovar este conjunto:

1. Refinar flanco dos pneus com lettering e detalhes de medida.
2. Criar low-poly das rodas.
3. Fazer bake normal/roughness dos sulcos e parafusos.
4. Integrar o conjunto ao blockout aprovado.
5. Iniciar `Production Pass 03 - Chassi, ILS e transmissao`.
