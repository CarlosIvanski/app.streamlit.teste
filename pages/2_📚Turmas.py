import streamlit as st
import pandas as pd
import io
from time import sleep

st.set_page_config(page_title="Turmas", layout="wide")

st.title("Detalhes das Turmas")

st.subheader('Importar dados das turmas e professores')

# Função para carregar arquivo Excel
def load_excel(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df

# Carregar arquivo Excel
uploaded_file1 = st.file_uploader("Escolha o arquivo de disponibilidade de professores", type=["xlsx"])
uploaded_file2 = st.file_uploader("Escolha o arquivo de turmas", type=["xlsx"])

# Carregar os dados do Excel para o st.session_state apenas uma vez
if uploaded_file1 is not None and 'df1' not in st.session_state:
    st.session_state.df1 = load_excel(uploaded_file1)
    st.success('Arquivo de disponibilidade de professores carregado com sucesso!')

if uploaded_file2 is not None and 'df2' not in st.session_state:
    st.session_state.df2 = load_excel(uploaded_file2)
    st.success('Arquivo de turmas carregado com sucesso!')

    # Procurar pelo professor 'Carlos' na primeira tabela
    professor_name = 'Carlos'
    professor_row = st.session_state.df1[st.session_state.df1['Professor'] == professor_name]

    if not professor_row.empty:
        # Pegar o nome do professor (neste caso, 'Carlos')
        professor_name = professor_row['Professor'].values[0]
        
        # Colocar o nome do professor 'Carlos' na primeira linha vazia da coluna 'Teacher' da segunda tabela
        empty_teacher_idx = st.session_state.df2['Teacher'].isna().idxmax()
        st.session_state.df2.at[empty_teacher_idx, 'Teacher'] = professor_name

    # Mostrar a tabela de turmas atualizada
    st.dataframe(st.session_state.df2)

    # Botão para exportar os dados editados para Excel
    st.subheader("Exportar Dados Editados para Excel")
    if st.button("Exportar para Excel"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.df2.to_excel(writer, index=False, sheet_name='Turmas Atualizadas')
        buffer.seek(0)
        
        st.download_button(
            label="Baixar Excel",
            data=buffer,
            file_name="turmas_atualizadas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
