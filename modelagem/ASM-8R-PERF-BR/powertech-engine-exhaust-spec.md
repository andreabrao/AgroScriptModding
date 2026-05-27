# PowerTech Engine and ASM Exhaust Spec

## Direcao tecnica

O motor deve ser tratado como peça de credibilidade, nao apenas como volume escondido no capô. Mesmo quando parcialmente coberto, a presenca de turbo, tubulacoes, radiador, common rail e escape ASM reforça o realismo do mod.

## Layout geral

```text
Motor: John Deere PowerTech 9.0 L
Cilindros: 6 em linha
Posicao no trator: longitudinal
Frente do trator: +Y
Escape ASM: lado direito visual do motor, subindo ao lado do capô
Radiador/aftercooler: dianteiro, antes do bloco
Transmissao e23: atras do motor
```

## Envelope de modelagem

Valores de referencia para encaixe no blockout:

```text
Comprimento conjunto motor: 1.65 m a 1.95 m
Largura maxima com turbo/tubos: 1.15 m a 1.35 m
Altura ate tampa de valvulas: 1.25 m a 1.45 m
Altura ate ponteira ASM: 3.15 m a 3.35 m
Centro do bloco: Y = 0.92, Z = 1.34
```

## Componentes high-poly

### Bloco

- Carcaca retangular com laterais chanfradas.
- Nervuras verticais e horizontais.
- Tampas laterais.
- Furos/parafusos grandes.
- Carter inferior mais escuro.
- Flanges de montagem.

### Cabecote e tampa de valvulas

- Cabecote separado do bloco.
- Tampa superior com parafusos e respiros.
- Seis posicoes de cilindro marcadas visualmente.
- Tampas/portas laterais para bake.

### Common Rail

Objetos separados:

```text
hp_common_rail_tube
hp_common_rail_bracket_01
hp_injector_01 ... hp_injector_06
hp_injector_line_01 ... hp_injector_line_06
```

As linhas podem começar como curvas/cilindros simples e depois serem refinadas com bevel em curva.

### Turbo

- Carcaca quente mais escura.
- Carcaca fria metalica.
- Centro do turbo.
- Tubo de admissao.
- Tubo pressurizado.
- Abraçadeiras.

### Aftercooler e radiador

- Caixa do radiador.
- Colmeia frontal com textura/normal futura.
- Aftercooler separado.
- Mangueira superior e inferior.
- Ventoinha com pas separadas ou disco para bake.

### Escape ASM Performance BR

- Downpipe saindo do turbo.
- Tubo vertical inox de maior diametro.
- Ponteira chanfrada.
- Abraçadeiras e suportes.
- Soldas leves.
- Discoloracao termica planejada no material/textura.

## Materiais

| Material | Uso |
| --- | --- |
| `mat_hp_engine_cast` | Bloco, cabecote, carter |
| `mat_hp_engine_dark` | Coletor quente, interior do escape |
| `mat_hp_common_rail` | Flauta e linhas |
| `mat_hp_stainless_exhaust` | Escape ASM inox |
| `mat_hp_rubber_hose` | Mangueiras e coifas |
| `mat_hp_radiator_core` | Colmeia radiador/aftercooler |
| `mat_hp_bolt_metal` | Parafusos e abraçadeiras |

## Bake e texturas

### Normal map

Priorizar:

- Fundicao do bloco.
- Nervuras e tampas.
- Parafusos.
- Abraçadeiras.
- Colmeia do radiador.
- Soldas do escape inox.

### Roughness/Metallic

- Bloco e cabecote com metal pintado/fundido.
- Escape com metalico alto e roughness medio.
- Coletor quente mais escuro e menos uniforme.
- Mangueiras com metallic zero e roughness alto.

### Dirt/Wear

Acumular sujeira:

- Base do motor.
- Carter.
- Atrás da ventoinha.
- Suportes e flanges.
- Junta do coletor.
- Base do escape.

## Animacao e efeitos

- `empty_fan_rotation_pivot`: futura animacao da ventoinha.
- `empty_exhaust_smoke_pivot`: ponto de particula no XML/I3D.
- `empty_turbo_center_pivot`: referencia visual, se houver efeito/rotacao.

## Riscos comuns

- Motor parecer um bloco generico sem leitura de 6 cilindros.
- Tubos atravessando capô/chassi.
- Escape ASM grosso demais e caricatural.
- Common rail plano demais, sem linhas individuais.
- Radiador sem espessura.
- Esquecer pivot da ventoinha e ponto de fumaca.

## Referencias oficiais base

- John Deere 8R 410 Tractor: https://www.deere.com/en/tractors/row-crop-tractors/row-crop-8-family/8r-410-tractor/
- John Deere Power & Efficiency 8R/8RT/8RX: https://www.deere.com/en/tractors/row-crop-tractors/row-crop-8-family/power-efficiency/
