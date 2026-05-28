# ASM-8R-PERF-BR

Projeto de modelagem tecnica para o trator pesado John Deere Serie 8R, ano modelo acima de 2020, customizado na configuracao AgroScriptModding Performance BR.

## Objetivo

Criar um asset 3D high-poly para Farming Simulator 22/25 com foco em realismo estrutural, texturizacao 4K, partes animaveis e preparacao para conversao posterior para malha de jogo.

## Entregaveis

- Modelo high-poly completo.
- Malha game-ready derivada com LODs.
- UVs organizadas para textura 4K.
- Mapas Normal, Metallic, Roughness, Glossiness, Dirt/Wear.
- Hierarquia preparada para exportacao I3D.
- Checklist de animacoes e pontos dinamicos.

## Arquivos deste pacote

- `briefing-tecnico.md`: especificacao principal do modelo.
- `part-breakdown.csv`: lista tecnica de componentes, prioridade e uso no jogo.
- `reference-scale-data.md`: medidas de escala e envelope usadas no blockout.
- `production-pass-01-blockout.md`: roteiro do primeiro passe de modelagem.
- `production-pass-02-wheels-tires.md`: roteiro do passe high-poly de rodado e pneus.
- `wheelset-modeling-spec.md`: especificacao detalhada dos pneus, rodas, pesos e bake.
- `production-pass-03-chassis-ils-transmission.md`: roteiro do passe de chassi, ILS e transmissao.
- `chassis-ils-transmission-spec.md`: especificacao mecanica para pivots, partes animaveis e bake.
- `production-pass-04-engine-exhaust.md`: roteiro do passe do motor PowerTech, turbo-aftercooler e exaustao ASM.
- `powertech-engine-exhaust-spec.md`: especificacao do bloco, common rail, arrefecimento, turbo e escape inox.
- `production-pass-05-rear-hitch-hydraulics.md`: roteiro do passe de levante traseiro, VCRs, PTO e drawbar.
- `rear-hitch-hydraulics-spec.md`: especificacao do conjunto traseiro, pivots e attacher joints.
- `production-pass-06-cab-commandview-interior.md`: roteiro do passe de cabine, interior, ActiveSeat II, CommandARM e G5.
- `cab-commandview-interior-spec.md`: especificacao da cabine, vidros, camera interna e comandos.
- `production-pass-07-lights-electrical-finish.md`: roteiro do passe de luzes, eletrica, LED 360 e acabamento externo.
- `lights-electrical-finish-spec.md`: especificacao das luzes de fabrica, barra LED ASM, farois auxiliares e chicotes.
- `production-pass-08-lowpoly-uv-bake-textures.md`: roteiro de low-poly, UV, bake, LODs e texturas 4K.
- `lowpoly-uv-bake-textures-spec.md`: especificacao de atlases, mapas PBR, cages e regras de performance.
- `production-pass-09-fs-integration-final.md`: roteiro de integracao FS22/FS25, exportacao e bloqueio de modelagem.
- `fs-final-integration-delivery-spec.md`: especificacao final de entrega para I3D/XML e Giants Editor.
- `final-modeling-lock.md`: bloqueio final de modelagem sem novas alteracoes de design.
- `final-delivery-checklist.md`: checklist final de entrega, textura, FS e bloqueio.
- `templates/FS22_ASM_8R_PERF_BR/vehicles/ASM_8R_PERF_BR.i3d`: template I3D inicial com a hierarquia base do veiculo.
- `blender-hierarchy.md`: padrao de colecoes, nomes e pivots.
- `fs22-fs25-integration.md`: notas para Giants Editor, materiais, LODs e sujeira.
- `quality-checklist.md`: criterios de aprovacao antes da exportacao.
- `project-manifest.json`: metadados do projeto.
- `scripts/create_blender_collections.py`: script opcional para montar a estrutura inicial no Blender.
- `scripts/create_asm8r_blockout.py`: script opcional para gerar o blockout proporcional inicial.
- `scripts/create_asm8r_wheelset_highpoly.py`: script opcional para gerar base high-poly procedural do rodado.
- `scripts/create_asm8r_chassis_ils_transmission.py`: script opcional para gerar base high-poly de chassi, ILS e transmissao.
- `scripts/create_asm8r_engine_powertech_exhaust.py`: script opcional para gerar base high-poly do motor e exaustao ASM.
- `scripts/create_asm8r_rear_hitch_hydraulics.py`: script opcional para gerar base high-poly do levante traseiro e hidraulico.
- `scripts/create_asm8r_cab_commandview_interior.py`: script opcional para gerar base high-poly da cabine e interior.
- `scripts/create_asm8r_lights_electrical_finish.py`: script opcional para gerar base high-poly das luzes e acabamento externo.
- `scripts/create_asm8r_bake_texture_setup.py`: script opcional para montar guias de low-poly, UV, bake e textura.
- `scripts/create_asm8r_mod_skeleton.py`: script opcional para criar a estrutura inicial do mod FS22.

## Referencias oficiais base

- John Deere 8 Series Tractors: https://www.deere.com/8R
- John Deere Power & Efficiency 8R/8RT/8RX: https://www.deere.com/en/tractors/row-crop-tractors/row-crop-8-family/power-efficiency/
- John Deere Cab Packages/CommandARM/ActiveSeat II: https://www.deere.com/en/tractors/row-crop-tractors/row-crop-8-family/comfort-visibility/
- John Deere Versatility & Capability/ILS/Hitch/PTO: https://www.deere.com/en/tractors/row-crop-tractors/row-crop-8-family/versatility-capability/
- G5 CommandCenter: https://www.deere.com/en/technology-products/precision-ag-technology/guidance/g5-commandcenter/

## Estado final

Este pacote fecha a modelagem tecnica do `ASM-8R-PERF-BR` em estado `FINAL MODELING PACKAGE LOCKED`. A partir deste ponto, novas mudancas devem ficar restritas a exportacao, textura, XML, compatibilidade e correcao de bugs, sem reabrir design ou proporcao do modelo.
