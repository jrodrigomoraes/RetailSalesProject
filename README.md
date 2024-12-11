# Documentação do Projeto de Previsão de Vendas

## **Resumo do Projeto**

Este projeto foi desenvolvido com o objetivo de criar um sistema capaz de:

1. Realizar análises exploratórias em um dataset de vendas.

2. Processar, limpar e transformar os dados utilizando o BigQuery.

3. Desenvolver modelos de machine learning para prever vendas futuras.

4. Implementar um sistema interativo para visualização de insights e previsões em tempo real, utilizando Streamlit.

## **Estrutura do Projeto**

O projeto foi dividido em sete etapas principais:

### 1. Exploração Inicial do Dataset (Localmente com Python)

- **Ferramentas Utilizadas:** Python (Pandas, Matplotlib, Seaborn).

- **Tarefas Realizadas:**

  - Inspeção inicial do dataset para entender colunas, tipos de dados e valores inconsistentes.

  - Identificação de valores nulos e duplicados.

  - Cálculo de estatísticas descritivas e visualizações iniciais, como histogramas e correlações.

**Resultados Principais:**

- Não foram encontrados valores nulos em colunas como Estoque e Preço.

- O estoque não é um fator limitante para vendas

### 2. Carregamento de Dados para o BigQuery

- **Tarefas Realizadas:**

  - Upload do dataset para um bucket no Google Cloud Storage.

  - Carregamento do dataset no BigQuery para criação de uma tabela bruta.

  - Execução de consultas simples para verificar consistência dos dados.

**Resultados Principais:**

- Dataset carregado com sucesso e validado no BigQuery.

### 3. Transformação e Limpeza no BigQuery

- **Tarefas Realizadas:**

  - Criação de uma tabela temporária para operações de limpeza.

  - Não precisou de tratamento de valores nulos utilizando funções SQL (COALESCE e CASE).

  - Não precisou de remoção de duplicatas com DISTINCT.

  - Conversão de tipos de colunas (e.g., DATE, FLOAT).

  - Criação de uma tabela final limpa e pronta para análise. Principalmente devido a conversões de tipos de colunas(DATE).

**Resultados Principais:**

- Dados limpos e armazenados em uma tabela final no BigQuery.

### 4. Análise de Dados no BigQuery

- **Tarefas Realizadas:**

  - Consultas SQL para extrair insights, como:

  - Receita total por mês e ano.

  - Dias com maior volume de vendas.

  - Correlações entre Preço e volume de vendas.

  - Criação de views para armazenar consultas recorrentes.

**Resultados Principais:**

- Tabelas de fácil e rápido acesso que evidenciaram sazonalidades e períodos de alta demanda.

### 5. Integração com Python e Machine Learning

- **Ferramentas Utilizadas:** Python (Scikit-learn, Pandas, Google BigQuery API).

- **Tarefas Realizadas:**

  - Exportação dos dados limpos do BigQuery para o Python.

  - Criação de modelos de previsão de vendas, como:

  - Regressão Linear.

  - Random Forest.

  - Avaliação de desempenho utilizando métricas como RMSE e R².

**Resultados Principais:**

- Modelo de Regressão Linear se saiu um pouco melhor

### 6. Deploy de Análise e Previsões

- **Ferramentas Utilizadas:** Streamlit.

- **Tarefas Realizadas:**

  - Criação de uma interface para visualização de insights e previsões.

  - Integração com BigQuery para buscar dados atualizados em tempo real.

  - Implementação de gráficos interativos e painéis de previsões.

**Resultados Principais:**

- Aplicativo funcional que permite análise em tempo real e teste de previsões.

## Conclusão:
O projeto atingiu todos os objetivos planejados, desde a exploração inicial do dataset até o deploy de um aplicativo interativo. Os resultados demonstram a viabilidade de combinar ferramentas como BigQuery, Python e Streamlit para resolver problemas reais e fornecer soluções de negócios baseadas em dados.
