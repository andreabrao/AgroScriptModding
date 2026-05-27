# Production Pass 04 - Motor PowerTech 9.0 L, Turbo-Aftercooler e Exaustao ASM

## Objetivo deste passo

Criar a base high-poly do conjunto do motor e exaustao do `ASM-8R-PERF-BR`, com leitura mecanica realista e elementos separados para bake, materiais e possivel animacao visual:

- Bloco John Deere PowerTech 9.0 L de 6 cilindros.
- Cabecote, tampa de valvulas e carter.
- Common Rail com flauta, linhas e pontos de injetor.
- Turbo, aftercooler/intercooler e tubulacoes.
- Coletor de escape.
- Radiador, ventoinha e polias/correias.
- Escapamento direto inox ASM de maior diametro.
- Pontos/empties para fumaca e calor visual.

## Referencias tecnicas usadas

- A linha 8R usa motor John Deere PowerTech 9.0 L.
- O 8R 410 tem motor PowerTech 9.0 L e transmissao e23.
- Motores PowerTech 9.0 L usam configuracoes turbo-aftercooled e common rail em linhas John Deere.

## Arquivo de partida

Use o script:

```text
scripts/create_asm8r_engine_powertech_exhaust.py
```

No Blender:

1. Abra o arquivo do chassi/ILS aprovado ou um arquivo novo.
2. Va em `Scripting`.
3. Abra `create_asm8r_engine_powertech_exhaust.py`.
4. Clique em `Run Script`.
5. Salve como:

```text
modelagem/ASM-8R-PERF-BR/blender/ASM_8R_PERF_BR_highpoly_engine_v001.blend
```

## Componentes obrigatorios

### Bloco e cabecote

- Bloco principal com volume pesado.
- Cabecote e tampa de valvulas separados.
- Carter inferior.
- Nervuras de fundicao.
- Tampas laterais e parafusos.
- Seis portas/volumes de cilindro visualmente marcados.

### Common Rail

- Flauta common rail separada.
- Seis linhas para injetores.
- Seis pontos de injetor no cabecote.
- Conectores e suportes.

### Turbo-aftercooler

- Turbo com carcaça fria/quente e miolo.
- Tubo de admissao para aftercooler.
- Tubo pressurizado retornando ao coletor.
- Aftercooler/intercooler dianteiro.
- Abraçadeiras nos tubos.

### Arrefecimento

- Radiador.
- Colmeia/tela frontal.
- Ventoinha.
- Polias e correia principal.
- Mangueiras superiores e inferiores.

### Exaustao ASM Performance BR

- Coletor de escape.
- Downpipe ate escape vertical.
- Escapamento direto inox com diametro maior.
- Abraçadeiras, suportes e soldas.
- Ponteira chanfrada.
- Empty para emissao de particula/fumaca.

## Regras de separacao

- Coletor, turbo, tubos e escape devem ser objetos separados.
- Common rail e linhas devem ficar separados do bloco.
- Ventoinha deve ter pivot proprio.
- Escape ASM deve ficar separado para configuracao visual.
- Parafusos e nervuras podem ser high-poly para bake.

## Pivots/empties minimos

| Pivot | Uso |
| --- | --- |
| `empty_fan_rotation_pivot` | Giro da ventoinha |
| `empty_turbo_center_pivot` | Centro do turbo |
| `empty_exhaust_smoke_pivot` | Ponto de particula/fumaca |
| `empty_engine_mount_front` | Alinhamento com chassi |
| `empty_engine_mount_rear` | Alinhamento com transmissao |

## Checklist de aprovacao

- [ ] O conjunto parece um motor 6 cilindros pesado.
- [ ] Bloco, cabecote, carter e tampa de valvulas estao separados.
- [ ] Turbo tem carcaça quente/fria e tubulacao coerente.
- [ ] Common rail e 6 linhas existem como objetos separados.
- [ ] Radiador, aftercooler e fan estao na frente do motor.
- [ ] Escape ASM inox tem diametro maior e silhueta propria.
- [ ] Empty de fumaca fica no topo da ponteira.
- [ ] Materiais separados para fundicao, inox, borracha, mangueiras e cromado.
- [ ] Nomes seguem `hp_`, `empty_` e `guide_`.

## Proximo passo apos aprovar

`Production Pass 05 - Levante traseiro, hidraulico, VCRs e barra de tracao`.
