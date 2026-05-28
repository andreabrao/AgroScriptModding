# Lights, Electrical and Finish Spec

## Direcao tecnica

As luzes precisam funcionar em duas camadas: forma fisica realista de dia e emissao clara a noite. O conjunto ASM deve parecer instalado por preparador profissional, nao acessorio improvisado.

## Grupos de luz

```text
factory_front_headlights
factory_waist_lights
factory_roof_work_lights
factory_rear_fender_lights
rear_signal_brake_reverse
asm_roof_led_bar
asm_grille_aux_lights
```

## Materiais

| Material | Uso |
| --- | --- |
| `mat_hp_light_lens_clear` | Lentes transparentes |
| `mat_hp_light_lens_red` | Lanterna/freio |
| `mat_hp_light_lens_orange` | Pisca |
| `mat_hp_light_reflector` | Refletores internos |
| `mat_hp_light_emissive_white` | Objetos emissive brancos |
| `mat_hp_electrical_black` | Cabos e suportes |
| `mat_hp_decal_asm` | Decals ASM |

## Bake e textura

- Lentes devem ter bevel real.
- Refletor pode receber normal map radial.
- Chicotes podem ser geometria simples com roughness alto.
- Decals devem ficar em atlas separado para troca futura.
- Sujeira leve nas lentes, forte nos suportes inferiores.

## XML/I3D futuro

Mapear objetos/empties para:

- `frontLight`
- `workLightFront`
- `workLightBack`
- `turnLightLeft`
- `turnLightRight`
- `brakeLight`
- `reverseLight`
- `beaconLight` se aplicavel

## Riscos comuns

- Luzes em um unico mesh sem controle por grupo.
- Emissive aplicado no suporte inteiro.
- Barra ASM grande demais.
- Farol auxiliar sem lente separada.
- Falta de chicote/suporte, deixando a peça flutuando.
