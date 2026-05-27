# Production Pass 01 - Blockout Tecnico

## Objetivo deste passo

Criar a primeira maquete 3D proporcional do `ASM-8R-PERF-BR`, separando os volumes principais para validar escala, silhueta, posicao de rodas, cabine, capo, chassi, ILS, levante traseiro, lastro e customizacoes Performance BR.

## Arquivo de partida

Use o script:

```text
scripts/create_asm8r_blockout.py
```

No Blender:

1. Abra um arquivo novo.
2. Va em `Scripting`.
3. Abra `create_asm8r_blockout.py`.
4. Clique em `Run Script`.
5. Salve como:

```text
modelagem/ASM-8R-PERF-BR/blender/ASM_8R_PERF_BR_blockout_v001.blend
```

## Validacoes do blockout

- [ ] Entre-eixos com eixo dianteiro e traseiro coerentes.
- [ ] Rodado traseiro duplo com largura visual Performance BR.
- [ ] Capo longo e robusto, com grade frontal agressiva mas realista.
- [ ] Cabine alta, centralizada e com espaco interno suficiente.
- [ ] Chassi e transmissao com massa visual pesada.
- [ ] ILS dianteiro ja separado em bracos, cubos e cilindros.
- [ ] Levante traseiro, VCRs e barra de tracao em posicao funcional.
- [ ] 22 pesos frontais posicionados individualmente.
- [ ] Discos de peso traseiros visiveis.
- [ ] Escape inox e barra LED ASM entram na silhueta.

## O que nao fazer ainda

- Nao iniciar detalhes finos antes de aprovar proporcao.
- Nao unir objetos animaveis ao chassi.
- Nao aplicar subdivisao em tudo sem necessidade.
- Nao texturizar antes de fechar UV plan.
- Nao modelar logos finais antes de confirmar permissao de uso.

## Sequencia recomendada apos blockout

1. Ajustar proporcoes com imagens laterais/frontais.
2. Criar `high_poly_body_v001`.
3. Criar rodas e pneus high-poly com sulcos reais.
4. Criar ILS high-poly animavel.
5. Criar levante traseiro e VCRs.
6. Criar interior da cabine.
7. Fazer low-poly LOD0.
8. Fazer UV e bake.

## Nomenclatura de versoes

```text
ASM_8R_PERF_BR_blockout_v001.blend
ASM_8R_PERF_BR_blockout_v002.blend
ASM_8R_PERF_BR_highpoly_body_v001.blend
ASM_8R_PERF_BR_highpoly_wheels_v001.blend
ASM_8R_PERF_BR_lod0_v001.blend
```

## Criterio de aceite

O blockout passa quando a silhueta ja parece um 8R pesado Performance BR mesmo sem detalhes, e quando todos os pontos animaveis principais existem como objetos separados.
