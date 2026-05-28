# Production Pass 08 - Low-poly, UV, Bake e Texturas 4K

## Objetivo deste passo

Converter a base high-poly do `ASM-8R-PERF-BR` em um pacote preparado para jogo, mantendo a leitura visual robusta do trator e organizando tudo para bake PBR 4K:

- Criar malha low-poly principal derivada do high-poly.
- Separar LOD0, LOD1 e LOD2.
- Definir colisoes simplificadas.
- Organizar UVs por atlas.
- Preparar cages de bake.
- Gerar o plano de mapas 4K.
- Definir mascara de sujeira/desgaste para Farming Simulator.

## Arquivo de partida

Use o script:

```text
scripts/create_asm8r_bake_texture_setup.py
```

No Blender:

1. Abra o arquivo high-poly aprovado ate o passo 7.
2. Va em `Scripting`.
3. Abra `create_asm8r_bake_texture_setup.py`.
4. Clique em `Run Script`.
5. Use as colecoes criadas como guia para low-poly, UV, bake e atlas.
6. Salve como:

```text
modelagem/ASM-8R-PERF-BR/blender/ASM_8R_PERF_BR_game_ready_bake_v001.blend
```

## LODs obrigatorios

| Nivel | Uso | Regra de leitura |
| --- | --- | --- |
| `LOD0` | Camera proxima, loja, screenshots | Mantem silhouette, pneus, cabine, luzes e implementos detalhados |
| `LOD1` | Distancia media em gameplay | Reduz parafusos, cabos finos, sulcos secundarios e detalhes internos |
| `LOD2` | Distancia longa | Mantem volume geral, cores e luzes principais |
| `COL` | Colisao | Formas simples por chassi, rodas, cabine e pesos |

## Atlases de textura

| Atlas | Resolucao | Conteudo |
| --- | --- | --- |
| `asm8r_body_4k` | 4096 | Capo, cabine externa, paralamas, grade e decals ASM |
| `asm8r_engine_chassis_4k` | 4096 | Motor, chassi, transmissao, ILS, hidraulico e pesos |
| `asm8r_wheels_tires_4k` | 4096 | Pneus, rodas, discos de peso, lettering e lama |
| `asm8r_interior_4k` | 4096 | CommandView III, assento, CommandARM, G5 e controles |
| `asm8r_lights_2k` | 2048 | Lentes, refletores, emissive e decals de luz |
| `asm8r_decals_2k` | 2048 | Logos, etiquetas, avisos, numeros e placas de acabamento |

## Mapas obrigatorios

- `baseColor`
- `normal`
- `metallic`
- `roughness`
- `glossiness`
- `dirtWear`
- `emissive`

## Regras de bake

- Objetos high-poly devem usar prefixo `hp_`.
- Objetos low-poly devem usar prefixo `lp_`.
- Cages devem usar prefixo `cage_`.
- Objetos de colisao devem usar prefixo `col_`.
- Cada parte animavel deve manter pivot separado antes do bake final.
- Normal map deve preservar fundicao do motor, textura de borracha e metal escovado.
- Parafusos pequenos podem ir para normal map quando nao mudam silhouette.
- Lettering de pneu pode ser geometria no high-poly e normal/height no low-poly.

## Sujeira e desgaste

Preparar mascara `dirtWear` com maior intensidade em:

- Laterais dos pneus.
- Sulcos e contato com solo.
- Pesos dianteiros.
- Articulacoes do ILS.
- Levante traseiro.
- VCRs e PTO.
- Degraus de acesso.
- Paralama traseiro e base da cabine.

## Checklist de aprovacao

- [ ] LOD0 mantem a identidade Performance BR.
- [ ] LOD1 nao perde silhouette de cabine, rodas e pesos.
- [ ] LOD2 continua reconhecivel em distancia longa.
- [ ] Colisoes estao simples e separadas.
- [ ] UVs nao possuem sobreposicao indesejada.
- [ ] Texel density esta coerente entre body, rodas e interior.
- [ ] Mapas PBR estao nomeados por atlas.
- [ ] Dirt/wear preparado para o shader do FS.
- [ ] Emissive separado para LEDs e displays.
- [ ] Cages de bake organizados por conjunto.

## Proximo passo apos aprovar

`Production Pass 09 - Integracao FS22/FS25, entrega final e bloqueio de modelagem`.
