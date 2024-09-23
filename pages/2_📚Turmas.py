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

# Permitir upload de múltiplos arquivos Excel
uploaded_files = st.file_uploader("Escolha os arquivos Excel", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        df = load_excel(uploaded_file)
        st.session_state[f'df_{uploaded_file.name}'] = df
        st.success(f'Arquivo {uploaded_file.name} carregado com sucesso!')
        
        # Mostrar os dados carregados em uma tabela editável
        df_editable = st.data_editor(df, use_container_width=True)
        st.session_state[f'df_{uploaded_file.name}'] = df_editable

        # Botão para exportar os dados editados para Excel
        if st.button(f"Exportar {uploaded_file.name} para Excel"):
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_editable.to_excel(writer, index=False, sheet_name='Dados Editados')
            buffer.seek(0)
            st.download_button(
                label=f"Baixar {uploaded_file.name} editado",
                data=buffer,
                file_name=f"{uploaded_file.name}_editado.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

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
