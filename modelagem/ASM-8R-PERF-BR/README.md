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
- `blender-hierarchy.md`: padrao de colecoes, nomes e pivots.
- `fs22-fs25-integration.md`: notas para Giants Editor, materiais, LODs e sujeira.
- `quality-checklist.md`: criterios de aprovacao antes da exportacao.
- `project-manifest.json`: metadados do projeto.
- `scripts/create_blender_collections.py`: script opcional para montar a estrutura inicial no Blender.
- `scripts/create_asm8r_blockout.py`: script opcional para gerar o blockout proporcional inicial.
- `scripts/create_asm8r_wheelset_highpoly.py`: script opcional para gerar base high-poly procedural do rodado.

## Referencias oficiais base

- John Deere 8 Series Tractors: https://www.deere.com/8R
- John Deere Power & Efficiency 8R/8RT/8RX: https://www.deere.com/en/tractors/row-crop-tractors/row-crop-8-family/power-efficiency/
- John Deere Cab Packages/CommandARM/ActiveSeat II: https://www.deere.com/en/tractors/row-crop-tractors/row-crop-8-family/comfort-visibility/
- John Deere Versatility & Capability/ILS/Hitch/PTO: https://www.deere.com/en/tractors/row-crop-tractors/row-crop-8-family/versatility-capability/
- G5 CommandCenter: https://www.deere.com/en/technology-products/precision-ag-technology/guidance/g5-commandcenter/

## Escopo inicial

Este pacote nao contem o mesh 3D final. Ele define a estrutura de producao para iniciar a modelagem no Blender, Maya, 3ds Max ou outro DCC e preparar a entrega para Farming Simulator.
