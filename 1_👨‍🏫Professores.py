import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# Funções existentes
def carregar_dados():
    if os.path.exists("disponibilidade.csv"):
        return pd.read_csv("disponibilidade.csv")
    else:
        return pd.DataFrame(columns=['Professor', 'Unidades', 'Carro', 'Máquinas', 'Disponibilidade', 'Módulo', 'Observações', 'Nome do Preenchendor', 'Data'])

def salvar_dados(df):
    df.to_csv("disponibilidade.csv", index=False)

def deletar_linha(index):
    st.session_state.df_disponibilidade = st.session_state.df_disponibilidade.drop(index).reset_index(drop=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success(f"Linha {index} deletada com sucesso!")

if 'df_disponibilidade' not in st.session_state:
    st.session_state.df_disponibilidade = carregar_dados()

st.title("Dashboard de Disponibilidade")
nome_preenchedor = st.text_input("Digite seu nome:")
data_modificacao = st.date_input("Data da modificação", value=datetime.today())
data_modificada_formatada = data_modificacao.strftime("%d/%m/%Y")
st.write(f"Data selecionada: {data_modificada_formatada}")

nomes_iniciais = ['Pessoa A']
unidades = ['Satélite', 'Vicentina', 'Jardim', 'Online']
if 'disponibilidade' not in st.session_state:
    st.session_state.disponibilidade = {nome: {} for nome in nomes_iniciais}

st.subheader("Tabela de Disponibilidade:")

# Adicionando CSS para melhorar a visualização
st.markdown(
    """
    <style>
    .table-container {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 10px;
        margin-bottom: 20px;
    }
    .table-container > div {
        border: 1px solid #ddd;
        padding: 8px;
        background-color: #f9f9f9;
    }
    .table-header {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .table-row {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
    }
    .table-cell {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Cria o container para a tabela
with st.container():
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    # Cabeçalho da tabela
    st.markdown('<div class="table-header">Nome do Professor</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-header">Unidades</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-header">Carro</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-header">Máquinas</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-header">Disponibilidade</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-header">Módulo</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-header">Observações</div>', unsafe_allow_html=True)

    for i, nome_inicial in enumerate(nomes_iniciais):
        cols = st.columns(7)  # Ajusta o número de colunas

        with cols[0]:
            nome_professor = st.text_input(f"Nome do professor", nome_inicial, key=f"nome_{i}")
            if nome_professor != nome_inicial:
                st.session_state.disponibilidade[nome_professor] = st.session_state.disponibilidade.pop(nome_inicial, {})
            if nome_professor not in st.session_state.disponibilidade:
                st.session_state.disponibilidade[nome_professor] = {}
            st.session_state.disponibilidade[nome_professor]

        with cols[1]:
            st.write("Unidades")
            for unidade in unidades:
                st.session_state.disponibilidade[nome_professor][unidade] = st.checkbox(f"{unidade}", 
                    value=st.session_state.disponibilidade[nome_professor].get(unidade, False), 
                    key=f"{nome_professor}_{unidade}")

        with cols[2]:
            st.write("Carro")
            st.session_state.disponibilidade[nome_professor]['Carro'] = st.checkbox("Tem carro", 
                value=st.session_state.disponibilidade[nome_professor].get('Carro', False), 
                key=f"{nome_professor}_carro")

        with cols[3]:
            st.write("Máquina")
            maquinas = {}
            st.markdown('<div class="table-cell">', unsafe_allow_html=True)
            maquinas['Notebook'] = st.checkbox("Notebook", 
                value='Notebook' in st.session_state.disponibilidade[nome_professor].get('Máquina', []), 
                key=f"{nome_professor}_notebook")
            maquinas['Computador'] = st.checkbox("Computador", 
                value='Computador' in st.session_state.disponibilidade[nome_professor].get('Máquina', []), 
                key=f"{nome_professor}_computador")
            maquinas['NDA'] = st.checkbox("NDA", 
                value='NDA' in st.session_state.disponibilidade[nome_professor].get('Máquina', []), 
                key=f"{nome_professor}_nda")
            st.markdown('</div>', unsafe_allow_html=True)
            st.session_state.disponibilidade[nome_professor]['Máquina'] = [key for key, value in maquinas.items() if value]

        with cols[4]:
            st.write("Disponibilidade")
            periodos = ['Manhã', 'Tarde', 'Noite', 'Sábado']
            disponibilidade_horarios = {}
            st.markdown('<div class="table-cell">', unsafe_allow_html=True)
            for periodo in periodos:
                disponibilidade_horarios[periodo] = st.checkbox(periodo, 
                    value=periodo in st.session_state.disponibilidade[nome_professor].get('Disponibilidade', []), 
                    key=f"{nome_professor}_{periodo}")
            st.markdown('</div>', unsafe_allow_html=True)
            st.session_state.disponibilidade[nome_professor]['Disponibilidade'] = [key for key, value in disponibilidade_horarios.items() if value]

        with cols[5]:
            st.write("Módulo")
            modulo_opcoes = {}
            st.markdown('<div class="table-cell">', unsafe_allow_html=True)
            modulo_opcoes['Stage 1'] = st.checkbox("Stage 1", 
                value='Stage 1' in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                key=f"{nome_professor}_stage1")
            modulo_opcoes['VIP'] = st.checkbox("VIP", 
                value='VIP' in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                key=f"{nome_professor}_vip")
            modulo_opcoes['CONVERSATION'] = st.checkbox("CONVERSATION", 
                value='CONVERSATION' in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                key=f"{nome_professor}_conversation")
            modulo_opcoes['MBA'] = st.checkbox("MBA", 
                value='MBA' in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                key=f"{nome_professor}_mba")
            st.markdown('</div>', unsafe_allow_html=True)
            st.session_state.disponibilidade[nome_professor]['Modulo'] = [key for key, value in modulo_opcoes.items() if value]

        with cols[6]:
            st.write("Observações")
            observacoes = st.text_area("Observações", 
                value=st.session_state.disponibilidade[nome_professor].get('Observações', ''), 
                key=f"{nome_professor}_observacoes")
            st.session_state.disponibilidade[nome_professor]['Observações'] = observacoes

    st.markdown('</div>', unsafe_allow_html=True)

def converter_para_dataframe(dados, nome_usuario, data):
    registros = []
    for professor, detalhes in dados.items():
        registro = {
            'Professor': professor,
            'Unidades': ', '.join([unidade for unidade, selecionado in detalhes.items() if unidade in unidades and selecionado]),
            'Carro': 'Sim' if detalhes.get('Carro', False) else 'Não',
            'Máquinas': ', '.join(detalhes.get('Máquina', [])),
            'Disponibilidade': ', '.join(detalhes.get('Disponibilidade', [])),
            'Módulo': ', '.join(detalhes.get('Modulo', [])),
            'Observações': detalhes.get('Observações', ''),
            'Nome do Preenchendor': nome_usuario,
            'Data': data
        }
        registros.append(registro)
    return pd.DataFrame(registros)

if st.button("Salvar Dados"):
    df_disponibilidade = converter_para_dataframe(st.session_state.disponibilidade, nome_preenchedor, data_modificada_formatada)
    salvar_dados(df_disponibilidade)
    st.success("Dados salvos com sucesso!")

if st.button("Deletar Dados"):
    index = st.number_input("Digite o índice da linha a ser deletada", min_value=0, max_value=len(st.session_state.df_disponibilidade)-1)
    deletar_linha(index)

# Display the saved data
st.subheader("Dados Salvos")
st.write(st.session_state.df_disponibilidade)
