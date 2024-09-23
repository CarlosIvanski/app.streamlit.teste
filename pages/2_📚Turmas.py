import streamlit as st
import pandas as pd
import io

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
    # Inicializar variáveis para os dois arquivos importantes
    df_professores = None
    df_turmas = None
    df_classificacoes = None
    
    for uploaded_file in uploaded_files:
        df = load_excel(uploaded_file)
        st.session_state[f'df_{uploaded_file.name}'] = df
        st.success(f'Arquivo {uploaded_file.name} carregado com sucesso!')

        # Mostrar os dados carregados em uma tabela editável
        df_editable = st.data_editor(df, use_container_width=True)
        st.session_state[f'df_{uploaded_file.name}'] = df_editable

        # Identificar qual arquivo é de professores, turmas e classificações
        if 'professores' in uploaded_file.name.lower():
            df_professores = df_editable
        elif 'turmas' in uploaded_file.name.lower():
            df_turmas = df_editable
        elif 'classificacoes' in uploaded_file.name.lower():
            df_classificacoes = df_editable

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

    # Se todos os arquivos estiverem carregados
    if df_professores is not None and df_turmas is not None and df_classificacoes is not None:
        # Botão para fundir os professores na tabela de turmas e criar uma nova tabela
        if st.button("Fundir Professores com Turmas e Criar Nova Tabela"):
            df_fusao = df_turmas.copy()  # Criar uma cópia da tabela de turmas para a fusão
            for i, row in df_classificacoes.iterrows():
                if i < len(df_fusao):
                    df_fusao.at[i, 'Teacher'] = row['Nome']  # Substituir a coluna "Teacher" com os nomes dos professores
            
            st.success("Fusão realizada com sucesso! Nova tabela criada.")
        
        # Mostrar a nova tabela de fusão
        st.subheader("Tabela de Fusão (Turmas + Professores)")
        st.dataframe(df_fusao)

        # Botão para exportar a nova tabela de fusão para Excel
        st.subheader("Exportar Nova Tabela de Fusão para Excel")
        if st.button("Exportar Nova Tabela de Fusão"):
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df_fusao.to_excel(writer, index=False, sheet_name='Tabela de Fusão')
            buffer.seek(0)

            st.download_button(
                label="Baixar Excel",
                data=buffer,
                file_name="tabela_fusao.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
