import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="Turmas",
)

st.title("Detalhes das Turmas")

st.subheader('Importar dados das turmas')

# Função para carregar arquivo Excel
def load_excel(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df

# Função para adicionar uma nova linha seguindo os mesmos cabeçalhos
def add_row():
    # Apenas adicionar uma nova linha se a tabela já foi carregada
    if 'df' in st.session_state:
        # Cria uma nova linha com valores vazios para todas as colunas existentes
        new_row = pd.DataFrame({col: [None] for col in st.session_state.df.columns})
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)

# Carregar arquivo Excel
uploaded_file = st.file_uploader("Escolha um arquivo Excel", type=["xlsx"])

# Carregar os dados do Excel para o st.session_state apenas uma vez
if uploaded_file is not None and 'df' not in st.session_state:
    st.session_state.df = load_excel(uploaded_file)
    st.success('Arquivo carregado com sucesso!')

# Adicionar um botão para adicionar mais linhas
if 'df' in st.session_state:
    if st.button('Adicionar Linha'):
        add_row()
        # Atualize o DataFrame no st.session_state após adicionar a linha
        st.session_state.df = st.session_state.df.copy()

    # Mostrar os dados carregados em uma tabela editável
    df_editable = st.data_editor(st.session_state.df, use_container_width=True)
    
    # Atualizar o DataFrame na sessão após a edição
    st.session_state.df = df_editable

    # Botão para exportar os dados editados para Excel
    st.subheader("Exportar Dados Editados para Excel")
    if st.button("Exportar para Excel"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.df.to_excel(writer, index=False, sheet_name='Dados Editados')
        buffer.seek(0)
        
        st.download_button(
            label="Baixar Excel",
            data=buffer,
            file_name="dados_editados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
