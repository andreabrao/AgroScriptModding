# Especificacao - Low-poly, UV, Bake e Texturas

## Escopo

Esta especificacao fecha a ponte entre modelagem high-poly e asset de jogo do `ASM-8R-PERF-BR`. O objetivo e manter realismo visual com uma malha que possa ser exportada para I3D sem excesso de peso.

## Nomeacao tecnica

| Prefixo | Uso |
| --- | --- |
| `hp_` | Malha high-poly usada como fonte de bake |
| `lp_` | Malha low-poly final |
| `lod0_` | Malha principal em camera proxima |
| `lod1_` | Malha reduzida para media distancia |
| `lod2_` | Malha reduzida para longa distancia |
| `cage_` | Cage de bake |
| `col_` | Colisao simplificada |
| `mat_` | Material |
| `tex_` | Textura exportada |
| `empty_` | Pivot, marker ou referencia |

## Separacao de materiais

### Carroceria

- Verde John Deere como material principal.
- Amarelo John Deere nos detalhes de roda.
- Decals ASM em atlas separado ou decal sheet.
- Roughness medio com pontos de desgaste em bordas.

### Chassi, motor e transmissao

- Cinza metalico com variacao de roughness.
- Normal map com fundicao, nervuras, tampas e parafusos.
- Dirt/wear mais forte em juntas e partes inferiores.

### Rodas e pneus

- Borracha com roughness alto.
- Lettering em normal/height.
- Deformacao visual do pneu preservada no low-poly.
- Lama e sujeira concentradas no contato com solo.

### Interior

- Plasticos escuros.
- Assento com tecido ou couro escuro.
- G5 com material emissive.
- CommandARM com botoes e labels via decal/normal.

### Luzes

- Lentes com material de policarbonato.
- Refletores com metallic alto.
- Emissive separado por grupo de luz.

## Atlases finais

```text
textures/
  asm8r_body_4k_baseColor.png
  asm8r_body_4k_normal.png
  asm8r_body_4k_metallic.png
  asm8r_body_4k_roughness.png
  asm8r_body_4k_glossiness.png
  asm8r_body_4k_dirtWear.png

  asm8r_engine_chassis_4k_baseColor.png
  asm8r_engine_chassis_4k_normal.png
  asm8r_engine_chassis_4k_metallic.png
  asm8r_engine_chassis_4k_roughness.png
  asm8r_engine_chassis_4k_glossiness.png
  asm8r_engine_chassis_4k_dirtWear.png

  asm8r_wheels_tires_4k_baseColor.png
  asm8r_wheels_tires_4k_normal.png
  asm8r_wheels_tires_4k_metallic.png
  asm8r_wheels_tires_4k_roughness.png
  asm8r_wheels_tires_4k_glossiness.png
  asm8r_wheels_tires_4k_dirtWear.png

  asm8r_interior_4k_baseColor.png
  asm8r_interior_4k_normal.png
  asm8r_interior_4k_metallic.png
  asm8r_interior_4k_roughness.png
  asm8r_interior_4k_glossiness.png
  asm8r_interior_4k_emissive.png

  asm8r_lights_2k_baseColor.png
  asm8r_lights_2k_normal.png
  asm8r_lights_2k_emissive.png
```

## Regras de UV

- Manter orientacao visual coerente com linhas do capo e cabine.
- Reservar espaco maior para logotipos, frente, pneus e interior visivel.
- Repeticao pode ser usada em borracha, cabos e mangueiras.
- Nao repetir decals exclusivos de marca ou plano ASM.
- Usar padding suficiente para mipmaps do FS.
- Manter ilhas de partes animaveis separadas quando necessario.

## Regras de performance

- Parafusos visiveis perto da camera podem ficar em geometria no LOD0.
- Parafusos secundarios devem virar normal map.
- Mangueiras principais ficam em geometria; cabos finos podem virar textura.
- Interior pode ter LOD proprio para camera interna.
- Colisao deve ignorar detalhes pequenos.

## Saida esperada

- Arquivo Blender game-ready com colecoes `LOD0`, `LOD1`, `LOD2`, `COL`, `BAKE_CAGES` e `TEXTURE_ATLASES`.
- Texturas PBR nomeadas por atlas.
- Checklist de bake aprovado.
- Modelo pronto para exportacao I3D no passo final.
