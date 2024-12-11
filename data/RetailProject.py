import pandas as pd

# Carregar o CSV
df = pd.read_csv('Mock_kaggle.csv')

# Ver as primeiras linhas dos dados
print(df.head())

# Verificar os tipos de dados e valores nulos
print(df.info())

# Limpeza: Remover ou preencher valores nulos, corrigir tipos de dados
df = df.dropna()  # Remover linhas com valores nulos (se houver)
df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d')  # Garantir que a coluna 'data' esteja no formato datetime
