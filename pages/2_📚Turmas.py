import streamlit as st
import pandas as pd

# Criando um DataFrame de exemplo com dados de informação
data = {
    "Data de Informação": ["2024-09-20", "2024-09-21", "2024-09-22"],
    "Nome": ["Professor A", "Professor B", "Professor C"],
    "Disponibilidade": ["Sim", "Não", "Sim"]
}

df = pd.DataFrame(data)

# Exibindo a tabela no Streamlit
st.write("Tabela de Disponibilidade:")
st.dataframe(df)

# Exportando para Excel
excel_file = "disponibilidade.xlsx"
df.to_excel(excel_file, index=False)

# Botão para download
st.download_button(
    label="Baixar tabela como Excel",
    data=open(excel_file, "rb").read(),
    file_name=TURMAS,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
