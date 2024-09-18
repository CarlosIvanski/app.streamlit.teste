import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Função para carregar dados
def carregar_dados():
    if os.path.exists("disponibilidade.csv"):
        return pd.read_csv("disponibilidade.csv")
    else:
        return pd.DataFrame(columns=['Professor', 'Unidades', 'Carro', 'Máquinas', 'Disponibilidade', 'Módulo', 'Observações', 'Nome do Preenchendor', 'Data', 'Dominio'])

# Função para salvar dados
def salvar_dados(df):
    df.to_csv("disponibilidade.csv", index=False)

# Carregar dados na sessão
if 'df_disponibilidade' not in st.session_state:
    st.session_state.df_disponibilidade = carregar_dados()

# Título do dashboard
st.title("Dashboard de Disponibilidade")

# Nome da pessoa que preenche o formulário
nome_preenchedor = st.text_input("Digite seu nome:")

# Data da modificação
data_modificacao = st.date_input("Data da modificação", value=datetime.today())

# Formatação da data
data_formatada = data_modificacao.strftime("%d/%m/%Y")
st.write(f"Data selecionada: {data_formatada}")

# Definir opções para o formulário
unidades = ['Satélite', 'Vicentina', 'Jardim', 'Online']
periodos = ['Manhã', 'Tarde', 'Noite', 'Sábado']
modulos = ['Stage 1', 'VIP', 'CONVERSATION', 'MBA', 'KIDS']

# Inicializa a disponibilidade do professor
st.subheader("Disponibilidade do Professor")
professor = st.text_input("Nome do professor")

with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("Unidades:")
        unidades_selecionadas = [unidade for unidade in unidades if st.checkbox(unidade, key=f"{unidade}")]

    with col2:
        st.write("Máquinas:")
        maquina_notebook = st.checkbox("Notebook")
        maquina_computador = st.checkbox("Computador")
        maquina_nda = st.checkbox("NDA")

    with col3:
        st.write("Disponibilidade:")
        disponibilidade_selecionada = [periodo for periodo in periodos if st.checkbox(periodo, key=f"{periodo}")]

# Domínio e módulo
with st.container():
    col4, col5 = st.columns(2)
    
    with col4:
        st.write("Domínio:")
        dominio_ingles = st.checkbox("Inglês")
        dominio_espanhol = st.checkbox("Espanhol")

    with col5:
        st.write("Módulo:")
        modulos_selecionados = [modulo for modulo in modulos if st.checkbox(modulo, key=f"{modulo}")]

# Observações
observacoes = st.text_area("Observações")

# Conversão dos dados para DataFrame
def converter_para_dataframe():
    data = {
        'Professor': professor,
        'Unidades': ", ".join(unidades_selecionadas),
        'Carro': 'Sim' if st.checkbox("Carro disponível") else 'Não',
        'Máquinas': ", ".join([maquina for maquina in ['Notebook', 'Computador', 'NDA'] if eval(f'maquina_{maquina.lower()}')]),
        'Disponibilidade': ", ".join(disponibilidade_selecionada),
        'Módulo': ", ".join(modulos_selecionados),
        'Observações': observacoes,
        'Nome do Preenchendor': nome_preenchedor,
        'Data': data_formatada,
        'Dominio': ", ".join([dom for dom in ['Inglês', 'Espanhol'] if eval(f'dominio_{dom.lower()}')])
    }
    return pd.DataFrame([data])

# Botão para salvar os dados
if st.button("Salvar"):
    novo_df = converter_para_dataframe()
    st.session_state.df_disponibilidade = pd.concat([st.session_state.df_disponibilidade, novo_df], ignore_index=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success("Dados salvos com sucesso!")

# Exibir dados salvos
st.subheader("Dados Salvos")
st.dataframe(st.session_state.df_disponibilidade)

# Opção para deletar linha
linha_para_deletar = st.number_input("Número da linha para deletar", min_value=0, max_value=len(st.session_state.df_disponibilidade)-1, step=1)
if st.button("Deletar Linha"):
    st.session_state.df_disponibilidade = st.session_state.df_disponibilidade.drop(linha_para_deletar).reset_index(drop=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success(f"Linha {linha_para_deletar} deletada com sucesso!")
