# Briefing Tecnico

## Codigo

`ASM-8R-PERF-BR`

## Nome do asset

John Deere Serie 8R Performance BR - AgroScriptModding

## Plataforma alvo

Farming Simulator 22 e Farming Simulator 25.

## Direcao de modelagem

Modelo high-poly de alta fidelidade para bake e derivacao game-ready. A modelagem deve preservar proporcoes reais do John Deere Serie 8R acima de 2020, com customizacoes brasileiras de potencia visual, lastro, rodado largo, iluminacao auxiliar e escapamento direto.

## Caracteristicas real life obrigatorias

### Motor PowerTech 9.0 L

- Bloco de 6 cilindros com geometria externa visivel.
- Tampas, nervuras, parafusos, suportes e detalhes de fundicao.
- Turbo-aftercooler com tubulacao de admissao e pressurizacao.
- Common Rail representado por flauta, linhas e conectores.
- Sistema de exaustao saindo do conjunto do motor para escape vertical.
- Radiador, intercooler, ventoinha, mangueiras e caixas laterais.

### Chassi e Suspensao

- Chassi monobloco robusto, com travessas e suportes visiveis.
- Eixo dianteiro ILS com bracos independentes funcionais.
- Pivots e links separados para futura animacao.
- Diferencial dianteiro, cardans, mangas de eixo e cubos modelados.
- Carcaca da transmissao e23 externa conectada ao bloco/chassi.

### Sistema hidraulico traseiro

- Levante traseiro Categoria 4N/3.
- Bracos inferiores, terceiro ponto, estabilizadores e cilindros.
- Barra de tracao oscilante com pino e suporte.
- Bloco VCR com 4 ou 5 saidas, engates rapidos, tampas e mangueiras.
- PTO traseira e protecao.

### Cabine CommandView III

- Interior completo visivel por vidro.
- Assento ActiveSeat II com base, amortecimento e giro sugerido de 40 graus.
- Console CommandARM com comandos, botoes e joystick.
- Display G5 em especificacao brasileira.
- Volante inclinavel/telescopico com coluna separada.
- Pedais, tapetes, alavancas, porta-copos e acabamento interno.

### Iluminacao de fabrica

- Pacote LED 360 graus.
- Farol dianteiro na grade.
- Luzes laterais na linha de cintura.
- Luzes de trabalho nos para-lamas traseiros.
- Luzes de sinalizacao, lanternas e repetidores.

## Customizacoes ASM Performance BR

### Rodado largo BR

- Pneus traseiros 800/70R38, Michelin ou Trelleborg, em configuracao dupla.
- Dianteiros compativeis com opcao simples ou dupla, conforme configuracao de jogo.
- Flancos com lettering, sulcos profundos e deformacao sutil por peso.
- Cubos e espaçadores reforcados para rodado duplo.

### Escapamento direto inox

- Substituir o silenciador padrao por escapamento direto de maior diametro.
- Material inox escovado com soldas, abraçadeiras e leve discoloracao termica.
- Ponteira vertical com corte chanfrado e interior escurecido.

### Luzes revisadas

- Barra LED slim no topo frontal da cabine.
- Farol de milha extra na grade dianteira.
- Lentes de policarbonato com espessura, reflexo interno e parafusos.
- Cabos e suportes discretos, sem aspecto improvisado.

### Lastreamento maximo

- Suporte frontal completo.
- 22 pesos de 50 kg + peso de fixacao.
- Discos de peso de ferro fundido nas rodas traseiras internas e externas.
- Marcas de fundicao, parafusos e desgaste em areas de contato.

## Materiais principais

- Verde John Deere para carroceria.
- Amarelo John Deere para rodas e detalhes.
- Cinza metalico para motor, chassi e transmissao.
- Borracha com roughness alto para pneus.
- Aco inox com anisotropia visual simulada para escapamento.
- Vidro da cabine com transparencia, sujeira leve e reflexo.

## Texturas e mapas

| Mapa | Resolucao alvo | Uso |
| --- | --- | --- |
| BaseColor | 4096 x 4096 | Cor principal, decals e desgaste |
| Normal | 4096 x 4096 | Fundicao, parafusos, ranhuras e pneu |
| Metallic | 4096 x 4096 | Separacao metal/pintura/borracha |
| Roughness | 4096 x 4096 | Verniz, plastico, metal e borracha |
| Glossiness | 4096 x 4096 | Compatibilidade de shader |
| Dirt/Wear | 4096 x 4096 | Sistema de sujeira/desgaste FS |

## Preparacao para sujeira/desgaste

As areas abaixo devem ter UV e vertex/texture masks prontas para acumulo de sujeira:

- Banda de rodagem e flanco interno dos pneus.
- Pesos frontais e discos traseiros.
- Bracos do ILS, cubos, diferenciais e cardans.
- Levante traseiro, VCRs, terceiro ponto e barra de tracao.
- Degraus, para-lamas, parte inferior da cabine e chassi.

## Nivel de fidelidade esperado

- High-poly com bordas chanfradas e parafusos reais nos pontos visiveis.
- Peças grandes separadas por funcao, nao um bloco unico.
- Interior completo o suficiente para camera interna.
- Todas as partes que podem animar devem ter pivot e nome proprio.
- Evitar detalhes apenas pintados quando o detalhe for proximo da camera.

## Observacoes de marca

Este projeto descreve um mod inspirado em maquina real. Conferir direitos de uso de logotipos, nomes e decals antes de distribuicao publica.
