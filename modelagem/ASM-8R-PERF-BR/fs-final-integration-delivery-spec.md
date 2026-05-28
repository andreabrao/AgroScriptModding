# Especificacao - Entrega Final FS22/FS25

## Status

`ASM-8R-PERF-BR` esta fechado como pacote de modelagem final para Farming Simulator 22/25.

## Entrega de modelagem

O pacote final inclui:

- Briefing tecnico completo.
- Breakdown de pecas.
- Escala e proporcoes.
- Passes de modelagem 01 a 09.
- Especificacoes por subsistema.
- Scripts procedurais opcionais para Blender.
- Plano de textura, UV, bake e LOD.
- Plano de integracao I3D/XML.
- Checklist final.

## Versoes alvo

| Jogo | Pasta sugerida | Observacao |
| --- | --- | --- |
| FS22 | `FS22_ASM_8R_PERF_BR` | Base principal do mod |
| FS25 | `FS25_ASM_8R_PERF_BR` | Adaptacao posterior mantendo prefixos e nodes |

## Naming final

| Tipo | Nome |
| --- | --- |
| Mod | `FS22_ASM_8R_PERF_BR` |
| Veiculo XML | `vehicles/ASM_8R_PERF_BR.xml` |
| Veiculo I3D | `vehicles/ASM_8R_PERF_BR.i3d` |
| Store icon | `store/store_ASM_8R_PERF_BR.dds` |
| Mod icon | `store/icon_ASM_8R_PERF_BR.dds` |
| Textura body | `textures/asm8r_body_4k_*` |
| Textura rodas | `textures/asm8r_wheels_tires_4k_*` |

## Material slots finais

- `mat_jd_green_paint`
- `mat_jd_yellow_rim`
- `mat_metallic_gray_chassis`
- `mat_black_rubber_tire`
- `mat_dark_plastic_interior`
- `mat_cab_glass`
- `mat_polycarbonate_lens`
- `mat_led_emissive_white`
- `mat_screen_g5_emissive`
- `mat_stainless_direct_exhaust`
- `mat_asm_decals`
- `mat_dirt_wear_mask`

## Transform e escala

- Unidade: metro.
- Rotacao aplicada antes da exportacao.
- Escala aplicada em todos os objetos.
- Pivots mantidos em rodas, ILS, volante, assento, portas, levante e hidraulico.
- Colisoes simplificadas fora dos materiais visuais.

## Checklist antes do Giants Editor

- [ ] Nomes sem espacos, acentos ou caracteres especiais.
- [ ] Objetos animaveis separados.
- [ ] Pivots revisados.
- [ ] Normais corrigidas.
- [ ] UVs finalizadas.
- [ ] Texturas linkadas.
- [ ] LODs separados.
- [ ] Colisoes separadas.
- [ ] Luzes separadas por grupo.
- [ ] Cameras e attacher joints marcados.

## Checklist no Giants Editor

- [ ] I3D abre sem erro.
- [ ] Shape count aceitavel.
- [ ] Texturas carregam sem missing file.
- [ ] Materials aceitam dirt/wear.
- [ ] Rodas giram e estercam.
- [ ] ILS nao clipa.
- [ ] Levante traseiro funciona.
- [ ] Luzes ligam por grupo.
- [ ] Interior aparece correto em primeira pessoa.
- [ ] Store data aparece no jogo.

## Itens fora do escopo de modelagem

Estes itens pertencem a fase de implementacao do mod e nao reabrem a modelagem:

- Ajuste fino de motor XML.
- Audio real de motor.
- Compra e configuracao na loja.
- Configuracoes alternativas de roda.
- Compatibilidade multiplayer.
- Testes em mapas.
- Otimizacao final apos profiler.
