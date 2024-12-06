# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:35:29 2024

@author: rafac
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv("avocado.csv")

#%%

# Filtrar o DataFrame para o ano de 2018
df_2018 = df[df['year'] == 2018]

# Converte o volume para números inteiros
df_2018['Total Volume'] = df_2018['Total Volume'].astype(int)

# Selecionar apenas as colunas de interesse (país, preço e volume)
selected_data = df_2018[['region','type','AveragePrice', 'Total Volume','Date']]

# Exibir o resultado
print(selected_data)

#%% ANÁLISE PREÇO

# Estatística descritiva
statistics = selected_data.describe()

# Histograma para AveragePrice separado por 'type'

# Filtrar dados para cada tipo
conventional_data = selected_data[selected_data['type'] == 'conventional']
organic_data = selected_data[selected_data['type'] == 'organic']

# Histograma para 'conventional'
plt.figure(figsize=(10, 5))
plt.hist(conventional_data['AveragePrice'], bins=10, alpha=0.7, edgecolor='black', color='blue')
plt.title("Histograma de Preços - Conventional")
plt.xlabel("Preço")
plt.ylabel("Frequência")
plt.show()

# Histograma para 'organic'
plt.figure(figsize=(10, 5))
plt.hist(organic_data['AveragePrice'], bins=10, alpha=0.7, edgecolor='black', color='green')
plt.title("Histograma de Preços - Organic")
plt.xlabel("Preço")
plt.ylabel("Frequência")
plt.show()


# Boxplot para AveragePrice
plt.figure(figsize=(8, 6))
plt.boxplot(selected_data['AveragePrice'], vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))
plt.title("Boxplot de Preços")
plt.xlabel("Preço")
plt.show()




#%% CASO NÃO HAJA REMOÇÃO DE OUTLIERS:
    
    filtered_data = selected_data
    

#%% TESTE NOVO MODELO



# Filtrar os dados necessários (supondo que 'region', 'type', 'AveragePrice', 'Total Volume', 'Date' já estão no DataFrame)
grouped = filtered_data.groupby(['region', 'type'])

# Inicializando listas para armazenar os resultados
results = []

# Iterar sobre cada combinação de 'region' e 'type'
for (region, type_), data in grouped:
    # Preparar os dados para a regressão
    X = data['AveragePrice'].values.reshape(-1, 1)  # Preço (variável independente)
    y = data['Total Volume'].values  # Volume (variável dependente)

    # Ajustar o modelo de regressão linear
    model = LinearRegression()
    model.fit(X, y)

    # Coeficientes da regressão
    intercept = model.intercept_
    slope = model.coef_[0]

    # Calcular a elasticidade-preço da demanda no ponto médio
    mean_price = data['AveragePrice'].mean()
    mean_volume = data['Total Volume'].mean()
    elasticity = (slope * mean_price) / mean_volume

    # Calcular o preço ótimo (com E = -1)
    price_optimal = -intercept / (2 * slope)

    # Verificar o último preço praticado em 2018-01-07
    last_price_data = data[data['Date'] == '2018-01-07']
    last_price = last_price_data['AveragePrice'].values[0] if not last_price_data.empty else None

    # Armazenar os resultados
    results.append({
        'region': region,
        'type': type_,
        'intercept': intercept,
        'slope': slope,
        'elasticity': elasticity,
        'last_price': last_price,
        'price_optimal': price_optimal,
        'Var%': (price_optimal / last_price -1) if last_price else none
        
    })

# Converter resultados para DataFrame para visualização
results_df = pd.DataFrame(results)

# Converter todos os campos numéricos do DataFrame para até 4 casas decimais
results_df = results_df.round(4)

# Configurar o Pandas para exibir números grandes sem notação científica
pd.options.display.float_format = '{:.4f}'.format

# Exibir os resultados
print(results_df)
#%% ADIÇÕES

# Acrescentar novas colunas ao results_df para enriquecer a análise de preços

# Calcular diferença absoluta entre o preço ótimo e o último preço
results_df['Price Difference'] = results_df['price_optimal'] - results_df['last_price']

# Categorizar elasticidade (Elástica, Inelástica, Unidade Elástica)
results_df['Elasticity Category'] = results_df['elasticity'].apply(
    lambda x: 'Elastic' if abs(x) > 1 else ('Inelastic' if abs(x) < 1 else 'Unit Elastic')
)

# Atualizar a lógica de classificação do status
def classify_price_status(var_percent):
    if -0.12 <= var_percent <= 0.12:
        return 'Stationary'
    elif var_percent > 0.12:
        return 'Underpriced'
    else:
        return 'Overpriced'

# Aplicar a função à coluna 'Var%' e criar a nova coluna 'Price Status'
results_df['Price Status'] = results_df['Var%'].apply(classify_price_status)

# Verificar se o DataFrame results_df está disponível
if 'results_df' in locals():
    # Filtrar os resultados onde o coeficiente angular (beta) é negativo
   results_df = results_df[results_df['slope'] < 0]


# Exibir o DataFrame atualizado
print(results_df.head())

# Exportar para Excel (opcional)
results_df.to_excel("updated_results_analysis.xlsx", index=False)
print("Arquivo exportado como 'updated_results_analysis.xlsx'.")

#%% GRÁFICO DE COLUNAS EMPILHADAS - STATUS DE PREÇO

# Criar o gráfico de colunas empilhadas com valores reais
ax = stacked_data.plot(kind='bar', stacked=True, figsize=(10, 6), color=['blue', 'green', 'darkorange'])

# Configurar título e rótulos
plt.title("Distribuição Real de Classificadores de Preço por Tipo (Empilhado)")
plt.xlabel("Tipo de Produto")
plt.ylabel("Preços em Frequência")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Reordenar a legenda para a mesma ordem do gráfico
handles, labels = ax.get_legend_handles_labels()
order = ['Overpriced', 'Stationary', 'Underpriced']  # Ordem desejada
handles = [handles[labels.index(o)] for o in order]
labels = [o for o in order]
plt.legend(handles, labels, title="Price Status", loc="upper right")

# Ajustar o limite superior do eixo Y
max_value = stacked_data.sum(axis=1).max()  # Valor máximo do empilhamento
plt.ylim(0, max_value + max_value * 0.15)  # Adicionar 15% ao limite superior

# Exibir o gráfico
plt.tight_layout()
plt.show()


#%% nova versão
# Agrupar os dados e contar a frequência por 'type' e 'Price Status'
stacked_data = results_df.groupby(['type', 'Price Status']).size().unstack(fill_value=0)

# Garantir que as colunas estejam na ordem correta
stacked_data = stacked_data[['Underpriced', 'Stationary', 'Overpriced']]

# Calcular o total por tipo (conventional ou organic)
totals_by_type = stacked_data.sum(axis=1)

# Criar a matriz de validação para porcentagens
validation_matrix = stacked_data.div(totals_by_type, axis=0) * 100

# Criar o gráfico de colunas empilhadas
ax = stacked_data.plot(kind='bar', stacked=True, figsize=(10, 6), color=['blue', 'green', 'darkorange'])

# Configurar título e rótulos
plt.title("Distribuição Real de Classificadores de Preço por Tipo (Empilhado)")
plt.xlabel("Tipo de Produto")
plt.ylabel("Frequência Absoluta")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Reordenar a legenda para a mesma ordem do gráfico
handles, labels = ax.get_legend_handles_labels()
order = ['Overpriced', 'Stationary', 'Underpriced']
handles = [handles[labels.index(o)] for o in order]
labels = [o for o in order]
plt.legend(handles, labels, title="Price Status", loc="upper right")

# Adicionar rótulos diretamente da matriz de validação
for i, (index, row) in enumerate(validation_matrix.iterrows()):
    for j, value in enumerate(row):
        if value > 0:
            # Adicionar o rótulo correspondente da matriz
            ax.text(
                x=i + (j * 0.05),  # Ajuste horizontal básico para centralizar
                y=stacked_data.iloc[i, :j + 1].sum() - (stacked_data.iloc[i, j] / 2),  # Altura ajustada
                s=f'{value:.1f}%',  # Rótulo formatado como porcentagem
                ha='center', va='center', color='white', fontsize=9
            )

# Ajustar o limite superior do eixo Y
max_value = stacked_data.sum(axis=1).max()  # Valor máximo do empilhamento
plt.ylim(0, max_value + max_value * 0.15)  # Adicionar 15% ao limite superior

# Exibir o gráfico
plt.tight_layout()
plt.show()

#%% VALIDADOR POR REGIÃO
# Filtrar apenas os dados de Albany e do tipo 'conventional'
albany_data = filtered_data[(filtered_data['region'] == 'CincinnatiDayton') & (filtered_data['type'] == 'organic')]

# Preparar os dados para a regressão
X = albany_data['AveragePrice'].values.reshape(-1, 1)  # Preço (variável independente)
y = albany_data['Total Volume'].values  # Volume (variável dependente)

# Ajustar o modelo de regressão linear
model = LinearRegression()
model.fit(X, y)

# Coeficientes da regressão
intercept = model.intercept_
slope = model.coef_[0]

# Calcular a elasticidade-preço da demanda no ponto médio
mean_price = albany_data['AveragePrice'].mean()
mean_volume = albany_data['Total Volume'].mean()
elasticity = (slope * mean_price) / mean_volume

# Calcular o preço ótimo (com E = -1)
price_optimal = -intercept / (2 * slope)

# Exibir os resultados
print("Região: CincinnatiDayton")
print(f"Intercepto (a): {intercept}")
print(f"Coeficiente Angular (b): {slope}")
print(f"Elasticidade: {elasticity}")
print(f"Preço Ótimo: {price_optimal}")

# Gerar o gráfico de dispersão e a reta da função de regressão
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', label='Dados reais')  # Gráfico de dispersão dos dados
plt.plot(X, model.predict(X), color='red', label=f'Regressão Linear: y = {slope:.2f}x + {intercept:.2f}')  # Reta da regressão
plt.title("Regressão Linear: CincinnatiDayton (Organic)")
plt.xlabel("Average Price")
plt.ylabel("Total Volume")
plt.legend()
plt.show()


