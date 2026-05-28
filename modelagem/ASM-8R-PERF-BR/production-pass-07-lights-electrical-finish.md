# Production Pass 07 - Luzes, Eletrica e Acabamento Externo

## Objetivo deste passo

Fechar os elementos externos de acabamento do `ASM-8R-PERF-BR`, com foco em leitura noturna, detalhes premium e customizacao ASM Performance BR:

- LED 360 de fabrica.
- Farol na grade dianteira.
- Luzes laterais na linha de cintura.
- Luzes de trabalho nos para-lamas traseiros.
- Barra LED slim ASM no teto.
- Farol de milha ASM na grade.
- Lanternas, pisca, freio e luz de re.
- Chicotes, suportes, conectores e caixas eletricas.
- Decals, badges, frisos e acabamento externo final.

## Arquivo de partida

Use o script:

```text
scripts/create_asm8r_lights_electrical_finish.py
```

Salve como:

```text
modelagem/ASM-8R-PERF-BR/blender/ASM_8R_PERF_BR_highpoly_lights_finish_v001.blend
```

## Componentes obrigatorios

### Luzes de fabrica

- Farol principal na grade.
- Luzes na linha de cintura.
- Luzes no teto frontal e traseiro.
- Luzes de trabalho nos para-lamas traseiros.
- Lanternas traseiras, freio e pisca.

### Luzes ASM Performance BR

- Barra LED slim no teto.
- Farol de milha extra na grade.
- Suportes discretos.
- Cabos/chicotes visiveis sem exagero.

### Eletrica e acabamento

- Chicotes dos farois auxiliares.
- Caixa eletrica pequena no teto/interior da grade.
- Suportes e parafusos.
- Frisos externos, badges ASM e areas para decals.
- Lentes com material separado de emissive.

## Regras de exportacao

- Cada grupo de luz deve ter objeto proprio.
- Lentes devem ficar separadas de refletores/suportes.
- Objetos emissive devem ser nomeados com `light_` ou `hp_light_`.
- Criar empties para futuros nodes de luz no Giants Editor.
- Decals ASM devem ficar em atlas proprio.

## Empties minimos

| Empty | Uso |
| --- | --- |
| `empty_light_front_main_l` | Farol dianteiro esquerdo |
| `empty_light_front_main_r` | Farol dianteiro direito |
| `empty_light_roof_work_front` | Luz de trabalho frontal teto |
| `empty_light_roof_work_rear` | Luz de trabalho traseira teto |
| `empty_light_asm_led_bar` | Barra LED ASM |
| `empty_light_rear_brake_l` | Freio traseiro esquerdo |
| `empty_light_rear_brake_r` | Freio traseiro direito |

## Checklist de aprovacao

- [ ] LED 360 de fabrica completo.
- [ ] Barra LED ASM visivel sem parecer improvisada.
- [ ] Farol de milha ASM com lente, refletor e suporte.
- [ ] Lanternas traseiras separadas.
- [ ] Empties de luz posicionados.
- [ ] Chicotes nao atravessam vidros/cabine.
- [ ] Decals/badges preparados em objetos separados.
- [ ] Materiais separados para lente, refletor, plastico, metal e emissive.

## Proximo passo

`Production Pass 08 - Low-poly, UV, Bake e Texturas 4K`.
