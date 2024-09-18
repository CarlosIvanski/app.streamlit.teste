import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# Função para carregar os dados de um arquivo CSV
def carregar_dados():
    if os.path.exists("disponibilidade.csv"):
        return pd.read_csv("disponibilidade.csv")
    else:
        return pd.DataFrame(columns=['Professor', 'Unidades', 'Carro', 'Máquinas', 'Disponibilidade', 'Módulo', 'Observações', 'Nome do Preenchendor', 'Data'])

# Função para salvar dados em um arquivo CSV
def salvar_dados(df):
    df.to_csv("disponibilidade.csv", index=False)

# Função para deletar uma linha específica
def deletar_linha(index):
    st.session_state.df_disponibilidade = st.session_state.df_disponibilidade.drop(index).reset_index(drop=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success(f"Linha {index} deletada com sucesso!")

# Carregar os dados salvos (se houver) ao iniciar a aplicação
if 'df_disponibilidade' not in st.session_state:
    st.session_state.df_disponibilidade = carregar_dados()

# Título do dashboard
st.title("Dashboard de Disponibilidade")

# Coletando o nome de quem preencheu o formulário
nome_preenchedor = st.text_input("Digite seu nome:")

# Coleta a data da modificação
data_modificacao = st.date_input("Data da modificação", value=datetime.today())

# Formata a data para DD/MM/YYYY
data_modificada_formatada = data_modificacao.strftime("%d/%m/%Y")
st.write(f"Data selecionada: {data_modificada_formatada}")

# Nomes iniciais dos professores
nomes_iniciais = ['Pessoa A']

# Lista de unidades
unidades = ['Satélite', 'Vicentina', 'Jardim', 'Online']

# Inicializa o session state se não estiver definido
if 'disponibilidade' not in st.session_state:
    st.session_state.disponibilidade = {nome: {} for nome in nomes_iniciais}

# Tabela de disponibilidade e checkboxes por unidade
st.subheader("Tabela de Disponibilidade:")

# Define a largura das colunas e organiza os campos em containers
with st.container():
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])

    for i, nome_inicial in enumerate(nomes_iniciais):
        with col1:
            nome_professor = st.text_input(f"Nome do professor", nome_inicial, key=f"nome_{i}")

        if nome_professor != nome_inicial:
            st.session_state.disponibilidade[nome_professor] = st.session_state.disponibilidade.pop(nome_inicial, {})

        if nome_professor not in st.session_state.disponibilidade:
            st.session_state.disponibilidade[nome_professor] = {}

        with col2:
            st.write("Unidades")
            for unidade in unidades:
                st.session_state.disponibilidade[nome_professor][unidade] = st.checkbox(f"{unidade}", 
                    value=st.session_state.disponibilidade[nome_professor].get(unidade, False), 
                    key=f"{nome_professor}_{unidade}")

        with col3:
            st.write("Carro")
            st.session_state.disponibilidade[nome_professor]['Carro'] = st.checkbox("Tem carro", 
                value=st.session_state.disponibilidade[nome_professor].get('Carro', False), 
                key=f"{nome_professor}_carro")

        with col4:
            st.write("Máquina")
            maquinas = {}
            with st.container():
                st.markdown('<div class="checkbox-no-wrap">', unsafe_allow_html=True)
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

        with col5:
            st.write("Disponibilidade")
            periodos = ['Manhã', 'Tarde', 'Noite', 'Sábado']
            disponibilidade_horarios = {}
            with st.container():
                st.markdown('<div class="checkbox-no-wrap">', unsafe_allow_html=True)
                for periodo in periodos:
                    disponibilidade_horarios[periodo] = st.checkbox(periodo, 
                        value=periodo in st.session_state.disponibilidade[nome_professor].get('Disponibilidade', []), 
                        key=f"{nome_professor}_{periodo}")
                st.markdown('</div>', unsafe_allow_html=True)
            st.session_state.disponibilidade[nome_professor]['Disponibilidade'] = [key for key, value in disponibilidade_horarios.items() if value]

        with col6:
            st.write("Módulo")
            modulo_opcoes = {}
            with st.container():
                st.markdown('<div class="checkbox-no-wrap">', unsafe_allow_html=True)
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

        with col7:
            st.write("Observações")
            observacoes = st.text_area("Observações", 
                value=st.session_state.disponibilidade[nome_professor].get('Observações', ''), 
                key=f"{nome_professor}_observacoes")
            st.session_state.disponibilidade[nome_professor]['Observações'] = observacoes

# Adicionando CSS para melhorar a visualização das tabelas
st.markdown(
    """
    <style>
    .checkbox-no-wrap {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .dataframe {
        border-collapse: collapse;
        width: 100%;
    }
    .dataframe th, .dataframe td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    .dataframe tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .dataframe th {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Função para converter os dados para DataFrame
def converter_para_dataframe(dados, nome_usuario, data):
    registros = []
    for professor, detalhes in dados.items():
        registro = {
            'Professor': professor,
            'Unidades': ', '.join([unidade for unidade, selecionado in detalhes.items() if unidade in unidades and selecionado]),
            'Carro': 'Sim' if detalhes.get('Carro', False) else 'Não',
            'Máquinas': ', '.join(detalhes['Máquina']),
            'Disponibilidade': ', '.join(detalhes['Disponibilidade']),
            'Módulo': ', '.join(detalhes['Modulo']),
            'Observações': detalhes.get('Observações', ''),
            'Nome do Preenchendor': nome_usuario,
            'Data': data.strftime('%Y-%m-%d')  # Garantindo que a data seja formatada sem hora
        }
        registros.append(registro)
    return pd.DataFrame(registros)

# Converter os dados coletados para um DataFrame
df_novo = converter_para_dataframe(st.session_state.disponibilidade, nome_preenchedor, data_modificacao)

# Botão para salvar os dados na tabela em tempo real
if st.button("Salvar dados"):
    st.session_state.df_disponibilidade = pd.concat([st.session_state.df_disponibilidade, df_novo], ignore_index=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success("Dados salvos com sucesso!")

# Exibindo a tabela atualizada
st.subheader("Tabela de Disponibilidade Atualizada:")
st.write(st.session_state.df_disponibilidade)

# Formulário para deletar uma linha existente
st.subheader("Deletar uma linha existente:")
linha_para_deletar = st.number_input("Número da linha a ser deletada:", min_value=0, max_value=len(st.session_state.df_disponibilidade)-1, step=1)
if st.button("Deletar linha"):
    deletar_linha(linha_para_deletar)
