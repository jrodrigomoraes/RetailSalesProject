import os
import json
import streamlit as st
import pandas as pd
from google.cloud import bigquery
from sklearn.metrics import mean_squared_error, r2_score
import joblib  # Para salvar e carregar modelos
import plotly.express as px
import plotly.graph_objects as go

# Configurações Iniciais do Streamlit
st.set_page_config(page_title="Análise e Previsão de Vendas", layout="wide")
st.title("Análise e Previsão de Vendas")

# Acessando as credenciais do BigQuery armazenadas no painel de Secrets do Streamlit
credentials = st.secrets["google_cloud"]["credentials_json"]

# Carregando o JSON
credentials_dict = json.loads(credentials)

# Definindo a variável de ambiente para autenticação com o Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_dict

#Extraindo project_id das credenciais:
project_id = credentials_dict["project_id"]

# Configuração do cliente BigQuery
client = bigquery.Client(project=project_id)

@st.cache_data
def fetch_data(query):
    return client.query(query).to_dataframe()

# Carregar Modelos Treinados
def load_model(model_name):
    return joblib.load(f"{model_name}.pkl")

# Fetch das Views do BigQuery
@st.cache_data
def fetch_views():
    queries = {
        "base": "SELECT * FROM `arctic-nectar-443501-m3.retail_sales.view_base`",
        "estoque": "SELECT * FROM `arctic-nectar-443501-m3.retail_sales.view_estoqueminmax`",
        "receita": "SELECT * FROM `arctic-nectar-443501-m3.retail_sales.view_receitatotal`",
        "volume": "SELECT * FROM `arctic-nectar-443501-m3.retail_sales.view_volumemedio`"
    }
    views = {name: fetch_data(query) for name, query in queries.items()}
    return views


"""
Abaixo estão as análises interativas realizadas utilizando Python, conectando-se às views do BigQuery. 
Esses gráficos fornecem uma visão detalhada e dinâmica dos dados, permitindo explorar insights sobre a receita total, 
volume de vendas e estoque disponível por data. Além disso, também podemos selecionar a Previsão de Vendas e escolher
qual modelo utilizaremos na previsão de vendas com base em dados históricos.
"""

# Carregar Dados e Views
views = fetch_views()

# Inspecionar as Views carregadas
for name, df in views.items():
    print(f"Inspecionando o DataFrame: {name}")
    print(df.head())  # Mostra as primeiras linhas do DataFrame
    print(df.columns)  # Lista as colunas disponíveis

# Opção 1: Análise de Dados
st.sidebar.title("Opções")
section = st.sidebar.radio("Escolha a seção", ["Análise de Dados", "Previsão de Vendas"])

if section == "Análise de Dados":
    st.subheader("Visualizações Interativas")

    # Fetch valores de estoque mínimo e máximo
    estoque_min = views['estoque']['estoque'].iloc[0]
    estoque_max = views['estoque']['estoque'].iloc[1]

    # Filtrar os dados de estoque pela data selecionada
    df_base = views['base']
    df_base['data'] = pd.to_datetime(df_base['data'])  # Garantir que a coluna 'data' seja do tipo datetime

    # Selecionar a data com um calendário interativo
    selected_date = st.date_input("Acompanhamento do Estoque por Data", value=pd.Timestamp("2024-12-10"))

    # Garantir que a data selecionada seja um timestamp compatível
    selected_date = pd.Timestamp(selected_date)

    # Filtrar o DataFrame para encontrar o estoque na data selecionada
    estoque_na_data = df_base[df_base['data'] == selected_date]

    # Selecionar o intervalo de datas para os eixos
    date_range = pd.date_range(df_base['data'].min(), df_base['data'].max())

    # Criar gráfico
    fig = go.Figure()

    if not estoque_na_data.empty:
        # Estoque do dia selecionado
        valor_estoque = estoque_na_data['estoque'].iloc[0]

        # Barra do estoque do dia
        fig.add_trace(go.Bar(
            x=[selected_date],
            y=[valor_estoque],
            name=f"Estoque em {selected_date.strftime('%d/%m/%Y')}",
            marker_color='blue',
            text=[f"{valor_estoque}"],  # Adiciona o valor como texto
            textposition="outside"  # Posição do texto acima da barra
        ))

        # Adicionar anotação acima da barra
        fig.add_annotation(
            x=selected_date,
            y=valor_estoque + (valor_estoque*0.15),
            text=f"{valor_estoque} unidades",
            showarrow=False,
            font=dict(size=16, color="white"),
            align="center"
        )
    else:
        st.write(f"Não há dados de estoque para a data selecionada ({selected_date.strftime('%d/%m/%Y')}).")

    # Linhas de estoque mínimo e máximo
    fig.add_trace(go.Scatter(
        x=date_range,
        y=[estoque_min] * len(date_range),
        mode='lines',
        name="Estoque Mínimo",
        line=dict(color="red", dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=date_range,
        y=[estoque_max] * len(date_range),
        mode='lines',
        name="Estoque Máximo",
        line=dict(color="green", dash="dash")
    ))

    # Configurações do gráfico
    fig.update_layout(
        title=f"Estoque em {selected_date.strftime('%d/%m/%Y')}" if not estoque_na_data.empty else "Estoque - Sem dados para a data selecionada",
        xaxis_title="Data",
        yaxis_title="Estoque",
        xaxis=dict(
            type="date",
            tickformat="%d-%m-%Y"
        ),
        barmode='overlay',
        template="plotly_white"
    )

    # Mostrar gráfico no Streamlit
    st.plotly_chart(fig)

    # Receita Total
    st.write("### Receita Total")

    # Ajustar os rótulos para incluir valores e porcentagens
    fig_receita = px.pie(
        views['receita'],
        names="ano", values="receita_total",
        title="Receita por Ano"
    )

    # Customizar os rótulos para exibir valores e porcentagens
    fig_receita.update_traces(
        textinfo='value+percent',  # Mostra o valor e a porcentagem
        texttemplate='%{value:.2f}<br>(%{percent})',
        # Formata o valor com 2 casas decimais e a porcentagem com 1 casa decimal
        hovertemplate='%{label}<br>Receita: %{value:.2f}<br>Porcentagem: %{percent:.1f}%'  # Exibe valor e porcentagem no hover
    )

    # Mostrar o gráfico
    st.plotly_chart(fig_receita)

    # Volume Médio
    st.write("### Volume Médio de Vendas")

    # Gráfico de barras com cores diferentes para cada faixa de preço
    fig_volume = px.bar(
        views['volume'],
        x="faixa_preco", y="volume_medio_vendas",
        color="faixa_preco",  # Diferencia as barras por cor com base na faixa de preço
        title="Volume Médio por Faixa de Preço",
        labels={'faixa_preco': 'Faixa de Preço', 'volume_medio_vendas': 'Volume Médio de Vendas'},
        color_discrete_map={"Alto": "indigo", "Médio": "darkviolet", "Baixo": "darkorchid"}  # Definir cores personalizadas
    )
    st.plotly_chart(fig_volume)


elif section == "Previsão de Vendas":
    st.subheader("Previsão de Vendas com Modelos")

    # Seleção do Modelo
    model_choice = st.selectbox("Escolha o Modelo de Previsão", ["Random Forest", "Linear Regression"])
    st.write(f"Modelo Selecionado: {model_choice}")

    # Carregar Dados de Teste e Modelos Treinados
    X_test = pd.read_csv("X_test.csv")  # Ajuste o caminho se necessário
    y_test = pd.read_csv("y_test.csv")["vendas_futuras"]

    model_file = "random_forest" if model_choice == "Random Forest" else "linear_regression"
    model = load_model(model_file)

    # Previsões
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    # Exibir Métricas
    st.write(f"### Métricas para o modelo {model_choice}")
    st.write(f"- **RMSE:** {rmse:.2f}")
    st.write(f"- **R²:** {r2:.2f}")

    # Visualização de Resultados
    st.write("### Comparação: Valores Reais vs Previstos")
    comparison = pd.DataFrame({"Real": y_test, "Previsto": y_pred})
    fig_comparison = px.scatter(comparison, x="Real", y="Previsto", title="Valores Reais vs Previstos")
    st.plotly_chart(fig_comparison)

    "No futuro, pretendo inserir um selectbox para que o usuário escolha as features para testar"
