# Regressão Linear aplicada a Pricing & Revenue Management: uma abordagem "simplificada"
Projeto de otimização de preços via regressão linear simples
### Introdução

Uma das formas mais eficazes e práticas de avaliar a precificação de produtos é por meio do estudo da regressão linear. No caso mais simplificado, a regressão linear "simples" oferece uma fórmula direta e adequada para o mercado de **bens normais** — aqueles sujeitos aos mecanismos da lei da oferta e da demanda, com inclinação negativa na curva de demanda. Consideraremos também que a variável dependente **Y** correponde à quantidade e a variável independente **X** ao preço. Tal qual segue:

![](https://media.licdn.com/dms/image/v2/D4D12AQEwmFL-WflmOQ/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1733432263665?e=1738800000&v=beta&t=3UJsu3UBH43I42TdUsxzeTSe6c2iIvt-jyRhUt65HWA)

**Observação 1:** Não abordarei outros aspectos da precificação, como sazonalidade, concorrência e fatores semelhantes. O foco será exclusivamente na relação linear entre demanda e preço.

**Observação 2:** Como este é um exemplo ilustrativo de como se aplica regressões para revenue management, é levado como premissa que podemos de fato movimentar os preços dos produtos aqui descritos.

Vamos ao que interessa!

Descobri uma base de dados interessante na plataforma Kaggle, que reúne informações sobre preços e volumes de abacates vendidos nos Estados Unidos. Os dados estão organizados por tipo de produto — orgânico ou convencional —, além de incluir detalhes sobre as regiões e datas de venda, totalizando **1.296** observações disponíveis.

Realizei a separação dos dados pertinentes e já de cara obtive alguns insights por meio da análise descritiva dos histogramas:

  

![](https://media.licdn.com/dms/image/v2/D4D12AQEt1OAk0Zjfog/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1733425909218?e=1738800000&v=beta&t=uLQ6bwTdvWWTeqMqXv-8wQZ0XgdUB-H34menLOZ1e2M)

Distribuição com leve concentração à direita

![](https://media.licdn.com/dms/image/v2/D4D12AQEUccziAm0Tkg/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1733425884543?e=1738800000&v=beta&t=icry_q4ltt58lgZgx7S902dbbufDEW7-Ys7sWgk94P0)

Distribuição com leve concentração à esquerda

Já de início já podemos verificar uma natureza distinta nas duas distribuições de preços, o que fará mais sentido a seguir com a construção do modelo.

### Modelagem

Após uma sessão de regressão linear simples em massa no Python, chego às seguintes amostras em que cada observação de região e tipo de produto recebem um modelo individual de regressão linear, garantindo uma granularidade específica a cada caso.

![](https://media.licdn.com/dms/image/v2/D4D12AQFpFXJHzk_xQQ/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1733432932300?e=1738800000&v=beta&t=cGlGHU8NitfWmLpFWrhhOg6v9HJpIYgu3OCKBrqCWI8)

Totalizaram-se 107 registros únicos de regressão

Foram incluídas as variáveis:

- **intercepto** (intercept) - alfa da regressão
- **inclinação** (slope) - beta da regressão (negativo)
- **elasticidade** (elasticity) - apresentado a seguir
- **último preço praticado** (last price) - dentro dos períodos analisados foi escolhido o último da amostra
- **preço ótimo** (price_optimal) - apresentado a seguir
- **variação de preço %** (Var%)
- **diferença de preço** (Price Difference)
- **categoria de elasticidade** (Elasticity Category): valores absolutos > 1: elástica; <1: inelástica.
- **status de preço** (Price Status): Quando Var% < -12%: underpriced; Quando >12%: overpriced; OU quando < 12% E > -12%: stationary — Este aqui seria um preço próximo ou igual ao de equilíbrio, o **preço ótimo**. (Aqui vale ressaltar que coloquei o valor arbitrário que pode ser calibrado a depender do contexto de aplicação e necessidade.)

Realizei uma seleção dos dados que respeitavam a condição de uma curva de demanda linear negativa, caracterizando bens com comportamento normal. Caso contrário, seria necessário adotar outras abordagens de modelagem, considerando características típicas de bens de Giffen, Veblen, entre outros.

Por meio de um editor gratuito de LaTeX, apresento as definições utilizadas para se chegar à elasticidade e ao preço ótimo:

![](https://media.licdn.com/dms/image/v2/D4D12AQG_AckfwBXdBA/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1733432529902?e=1738800000&v=beta&t=SyX1DDOHVnhgZ0jEMsDzONinxaOebx8Hrdkrj2DgHr4)

P* é o Preço Ótimo estimado e baseado na ponderação das médias das quantidades utilizadas nos cálculos.

### Resultados e Análises

Após realizar algumas análises, elaborei um gráfico de colunas empilhadas que ilustra a distribuição de frequência dos preços classificados como ajustados ou desajustados, conforme o critério definido anteriormente ("Overpriced", "Stationary" e "Underpriced"). É interessante observar como os preços dos abacates convencionais se encontram mais frequentemente acima do ponto de equilíbrio em comparação com os orgânicos. Esse comportamento reforça o insight inicial apresentado no artigo, em que os histogramas indicavam uma tendência de desvio à direita para os preços dos convencionais e à esquerda para os orgânicos. Em resumo, os abacates convencionais estão mais caros do que deveriam, enquanto os orgânicos estão relativamente mais baratos. No entanto, ambos apresentam uma concentração significativa de preços acima do **preço ótimo**, o que sugere uma boa oportunidade para ajuste.

![](https://media.licdn.com/dms/image/v2/D4D12AQGhf8aompipkQ/article-inline_image-shrink_1000_1488/article-inline_image-shrink_1000_1488/0/1733439032851?e=1738800000&v=beta&t=ma_sPskrYVpIZLXQmWL-OTc_aSDvwg4r124jziJA7QI)

A imagem permite uma visualização mais incisiva sobre o comportamento de preços de maneira comparada a diferentes segmentos de produtos; cada um com seus próprios índices de preço.

A seguir, uso de exemplo um abacate orgânico vendido em Cincinnati. Nele ilustro no gráfico de dispersão a curva de regressão linear e a respectiva função com intercepto (a) e coeficiente (b). Para cada observação e registro utilizado no cálculo em Python é possível construir um gráfico como esse.

![](https://media.licdn.com/dms/image/v2/D4E12AQHYwaMEYhErgA/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1733440604766?e=1738800000&v=beta&t=twyx5sN8MxvDReX-emATl-sngRg9F1EpFxg0Dz8D9sk)

Aqui, apresento a aplicação prática da regressão linear para determinar o ponto de maximização da receita no mercado de Cincinnati. A análise é complementada por uma tabela que detalha a evolução dos parâmetros de preço. O cálculo resulta em um preço ótimo de **$1,015**, associado a uma quantidade de **39.531** unidades.

Novamente, uma aplicação das fórmulas em LaTeX:

![](https://media.licdn.com/dms/image/v2/D4E12AQG842NjOvUwug/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1733443697378?e=1738800000&v=beta&t=QZQGL6rfNEB2nT8s9FG6w_Ski6j_mP2yfcVuQ84EuPw)

![](https://media.licdn.com/dms/image/v2/D4E12AQEREk_RbtStqQ/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1733443894962?e=1738800000&v=beta&t=d5IaQq0BDB5m0jXHatKHxc1cYWl-aJjqHEmX7o78VzQ)

De maneira mais elegante, chegamos nesse gráfico final:

![](https://media.licdn.com/dms/image/v2/D4E12AQF4vJ_TaBBwFA/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1733445758056?e=1738800000&v=beta&t=XgfeenDf3qPkd7BCXA_Va6MOLviEQwIp3AMfugi4s2Y)

Eixo Y: Receita Total. Eixo X: Preço Praticado. Ponto Vermelho: Preço Ótimo.

### Conclusão

Por meio de algoritmos de machine learning e conhecimentos em economia, é possível explorar um amplo universo de possibilidades em pricing e revenue management. Neste exemplo, foi adotado um viés criterioso para demonstrar como e onde ajustar preços, utilizando inclusive a possibilidade de um **batch update**, com o objetivo de maximizar as receitas para todos os produtos.

Ressalta-se ainda a possibilidade de extensão desse modelo para outros mercados, permitindo ajustes estratégicos fundamentados em bases científicas. Além disso, a agilidade na definição das alterações necessárias assegura uma resposta rápida a eventuais choques de demanda.

E, novamente, destaco que esse é apenas um dos modelos possíveis. Existe uma ampla gama de modelos em machine learning aplicáveis nas definições de preços.

---

### Referências:

VARIAN, H. R. _Microeconomia: princípios básicos._ 9. ed. São Paulo: Pearson, 2014.

Sartoris Neto, A. Estatística e Introdução à Econometria. 2ª ed. São Paulo: Saraiva, 2015.

Fávero LP, Belfiore P. 2024. Manual de Análise de Dados: Estatística e Machine Learning com Excel, SPSS, STATA, R e Python. 2a ed. Rio de Janeiro: LTC Livros Técnicos e Científicos Ltda.
