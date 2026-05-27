# Integracao FS22 / FS25

## Estrategia de malha

O high-poly sera usado para bake e marketing/render. A versao de jogo deve ser derivada com LODs e collision simplificada.

## LODs sugeridos

| LOD | Uso | Alvo |
| --- | --- | --- |
| LOD0 | Camera proxima, interior, garagem | Maximo detalhe visual |
| LOD1 | Distancia media em campo | Reducao de parafusos, cabos e detalhes pequenos |
| LOD2 | Distancia longa | Silhueta principal, rodas simplificadas |
| Collision | Fisica e interacao | Malhas convexas simples |

## Texturas

Padrao de nomes:

```text
asm8r_body_basecolor.dds
asm8r_body_normal.dds
asm8r_body_metallic.dds
asm8r_body_roughness.dds
asm8r_body_gloss.dds
asm8r_body_dirt.dds
asm8r_tires_basecolor.dds
asm8r_tires_normal.dds
asm8r_interior_basecolor.dds
asm8r_lights_emissive.dds
```

## Conjuntos UV

- `body_4k`: capo, cabine externa, paralamas, pesos e chassi visivel.
- `engine_chassis_4k`: motor, transmissao, ILS, hidraulico e escape.
- `tires_wheels_4k`: pneus, rodas e pesos de roda.
- `interior_4k`: cabine, assento, console, display e volante.
- `decal_atlas_2k`: emblemas, logos, adesivos ASM e avisos pequenos.

## Sujeira e desgaste

Preparar masks para:

- Poeira seca em partes horizontais.
- Lama nas rodas, pneus, ILS, levante e chassi inferior.
- Desgaste nos pesos frontais, engates, degraus, barra de tracao e cubos.
- Leve risco/verniz em capo e paralamas.

## Animacoes planejadas

| Sistema | Elementos |
| --- | --- |
| Rodas | Rotacao, esterco e compressao visual do pneu |
| ILS | Bracos superiores/inferiores, mangas e cilindros |
| Direcao | Volante e rodas dianteiras |
| Levante traseiro | Bracos inferiores, terceiro ponto, cilindros |
| Luzes | LED fabrica, barra LED ASM, farol de milha, freio e pisca |
| Cabine | Portas opcionais, assento com giro, tela emissive |
| Escape | Ponto de particula/fumaca no escape inox |

## XML/Config futuras

Quando a malha game-ready estiver pronta, criar arquivos:

```text
modDesc.xml
vehicles/ASM_8R_PERF_BR.xml
vehicles/store_ASM_8R_PERF_BR.dds
vehicles/ASM_8R_PERF_BR.i3d
vehicles/ASM_8R_PERF_BR.i3d.shapes
```

Configurar no XML:

- `brand`: AGRO SCRIPT MODDING ou John Deere conforme permissao.
- `category`: tractorsL.
- `power`: faixa alta, compativel com 8R customizado.
- `wheels`: configuracoes simples/dupla BR.
- `lights`: fabricas e ASM auxiliares.
- `workAreas`: se houver interacoes especiais.
- `attacherJoints`: traseiro Categoria 4N/3, PTO e drawbar.
- `motorConfigurations`: padrao e Performance BR.

## Collision

- Chassi, cabine, capo e pesos com malhas simples.
- Rodas com collision propria do sistema de wheels quando possivel.
- Evitar collision detalhada em mangueiras, VCRs, farois e interior.

## Regras de exportacao

- Aplicar transforms antes da exportacao final.
- Manter escala em metros.
- Conferir nomes sem acentos e sem espacos.
- Evitar faces internas desnecessarias em game-ready.
- Checar normais e tangents antes do bake.
- Garantir que objetos animaveis tenham pivots corretos.
