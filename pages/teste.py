import pandas as pd
import streamlit as st

# Dados pré-programados
dados_amostragem = {
    "Coluna 1": ["Dado 1", "Dado 2", "Dado 3"],
    "Coluna 2": [10, 20, 30],
    "Coluna 3": ["A", "B", "C"]
}

# Criação da tabela de amostragem
tabela_amostragem = pd.DataFrame(dados_amostragem)

# Exibição da tabela no Streamlit
st.write("Tabela de Amostragem:")
st.dataframe(tabela_amostragem)

# Botão para gerar o arquivo
if st.button("Gerar arquivo"):
    tabela_amostragem.to_csv("tabela_de_amostragem.csv", index=False)
    st.success("Arquivo gerado com sucesso!")
