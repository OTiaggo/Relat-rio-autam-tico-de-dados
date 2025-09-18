import numpy as np
import pandas as pd
import textwrap

# ==== CHAME A FUNÇÃO PASSANDO O DATAFRAME ==== #
def gerar_relatorio(dataset):
  colunas = dataset.columns

  # Selecionar apenas colunas numéricas
  dataset_numerico = dataset.select_dtypes(include=np.number)

  # Medidas de localização
  estatisticas = dataset_numerico.describe()  # mín, max, Q1, Q3, mediana, média, desvio padrão
  moda = dataset_numerico.mode()

  # dispersões (amplitude, IQR, variância)
  amplitude = dataset_numerico.max() - dataset_numerico.min()
  IQR = dataset_numerico.quantile(0.75) - dataset_numerico.quantile(0.25)
  variancia = dataset_numerico.var()

  # distribuições (assimetria, curtose)
  assimetria = dataset_numerico.skew()
  curtose = dataset_numerico.kurtosis()

  # Detecção de outliers via Tukey(1,5IQR)
  limite_inferior = dataset_numerico.quantile(0.25) - (1.5 * IQR)
  limite_superior = dataset_numerico.quantile(0.75) + (1.5 * IQR)

  outliers_mask = (dataset_numerico < limite_inferior) | (dataset_numerico > limite_superior)
  outlier_rows = dataset[outliers_mask.any(axis=1)]

  # Colunas categóricas
  dataset_categorico = dataset.select_dtypes(exclude=np.number)

  # Frequências (top-5) and Domain Percentage
  if not dataset_categorico.empty and len(dataset_categorico.columns) > 0:
      frequencias = dataset_categorico.stack().value_counts().head(5)
      # Indicador de diversidade (domínio da categoria mais frequente)
      total_registros = len(dataset)
      dominio_categoria_mais_frequente = (frequencias.iloc[0] / total_registros) * 100
  else:
      frequencias = "Não aplicável"
      dominio_categoria_mais_frequente = "Não aplicável"

  correlacoes = dataset.corr()

  conteudo = f"""
    RELATÓRIO DESCRITIVO DO DATASET

    1. Informações Gerais:
      - Número total de registros: {len(dataset)}
      - Número total de colunas: {len(colunas)}
      - Colunas numéricas: {list(dataset_numerico.columns) if not dataset_numerico.empty else "Nenhuma"}
      - Colunas categóricas: {list(dataset_categorico.columns) if not dataset_categorico.empty else "Nenhuma"}

    2. Estatísticas Descritivas (colunas numéricas):
{textwrap.indent(str(estatisticas), "\t\t")}

    3. Moda das variáveis numéricas:
{textwrap.indent(str(moda.iloc[0] if not moda.empty else "Não aplicável"), "\t\t")}

    4. Medidas de Dispersão:
      - Amplitude:
{textwrap.indent(str(amplitude), "\t\t")}

      - Intervalo Interquartil (IQR):
{textwrap.indent(str(IQR), "\t\t")}

      - Variância:
{textwrap.indent(str(variancia), "\t\t")}

    5. Medidas de Distribuição:
      - Assimetria (Skewness):
{textwrap.indent(str(assimetria), "\t\t")}

      - Curtose (Kurtosis):
{textwrap.indent(str(curtose), "\t\t")}

    6. Outliers (Tukey - 1.5 * IQR):
      - Quantidade de linhas com outliers:
{textwrap.indent(str(len(outlier_rows)), "\t\t")}

      - Linhas com outliers:
{textwrap.indent(str(outlier_rows), "\t\t")}

    7. Colunas Categóricas:
      - Frequências (Top-5 categorias):
{textwrap.indent(str(frequencias), "\t\t")}

      - Domínio da categoria mais frequente (%):
{textwrap.indent(str(dominio_categoria_mais_frequente), "\t\t")}

    8. Correlações:
      - Todas as correlações:
{textwrap.indent(str(correlacoes), "\t\t")}

      - Principais correlações positivas:
{textwrap.indent(str(correlacoes.where(np.triu(np.ones(correlacoes.shape), k=1).astype(np.bool_)).stack().sort_values(ascending=False).head(5)), "\t\t")}

      - Principais correlações negativas:
{textwrap.indent(str(correlacoes.where(np.triu(np.ones(correlacoes.shape), k=1).astype(np.bool_)).stack().sort_values(ascending=True).head(5)), "\t\t")}

  """

  # Salvar automaticamente em TXT
  caminho_arquivo = "relatorio_descritivo.txt"
  with open(caminho_arquivo, "w", encoding="utf-8") as f:
      f.write(conteudo)

  print(f"✅ Relatório salvo em: {caminho_arquivo}")


# Carregue seu dataset aqui

# Chamada da função
gerar_relatorio("seu dataset")