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

# Reestruturando a tabela de disponibilidade para ser exibida horizontalmente
st.subheader("Tabela de Disponibilidade:")

# Adicionando CSS para melhorar a visualização
st.markdown(
    """
    <style>
    .table-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .table-container div {
        display: flex;
        gap: 10px;
    }
    .table-container div:nth-child(odd) {
        background-color: #f2f2f2;
    }
    .table-container div:nth-child(even) {
        background-color: #ffffff;
    }
    .table-label {
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Exibindo a tabela com professores nas colunas e dados nas linhas
with st.container():
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    
    # Exibindo os cabeçalhos
    st.markdown('<div class="table-label">Unidades</div>', unsafe_allow_html=True)
    for unidade in unidades:
        st.markdown(f'<div class="table-label">{unidade}</div>', unsafe_allow_html=True)
    
    # Iterando pelos professores e suas informações
    for nome_professor in st.session_state.disponibilidade:
        st.markdown('<div>', unsafe_allow_html=True)
        
        with st.container():
            # Unidades
            for unidade in unidades:
                st.checkbox(f"{unidade}", 
                            value=st.session_state.disponibilidade[nome_professor].get(unidade, False), 
                            key=f"{nome_professor}_{unidade}")
        
        # Carro
        st.markdown(f'<div class="table-label">Carro</div>', unsafe_allow_html=True)
        st.checkbox("Tem carro", 
                    value=st.session_state.disponibilidade[nome_professor].get('Carro', False), 
                    key=f"{nome_professor}_carro")

        # Máquinas
        st.markdown(f'<div class="table-label">Máquinas</div>', unsafe_allow_html=True)
        maquinas = ['Notebook', 'Computador', 'NDA']
        for maquina in maquinas:
            st.checkbox(maquina, 
                        value=maquina in st.session_state.disponibilidade[nome_professor].get('Máquina', []), 
                        key=f"{nome_professor}_{maquina.lower()}")
        
        # Disponibilidade
        st.markdown(f'<div class="table-label">Disponibilidade</div>', unsafe_allow_html=True)
        periodos = ['Manhã', 'Tarde', 'Noite', 'Sábado']
        for periodo in periodos:
            st.checkbox(periodo, 
                        value=periodo in st.session_state.disponibilidade[nome_professor].get('Disponibilidade', []), 
                        key=f"{nome_professor}_{periodo.lower()}")
        
        # Módulo
        st.markdown(f'<div class="table-label">Módulo</div>', unsafe_allow_html=True)
        modulos = ['Stage 1', 'VIP', 'CONVERSATION', 'MBA']
        for modulo in modulos:
            st.checkbox(modulo, 
                        value=modulo in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                        key=f"{nome_professor}_{modulo.lower()}")
        
        # Observações
        st.markdown(f'<div class="table-label">Observações</div>', unsafe_allow_html=True)
        st.text_area("Observações", 
                     value=st.session_state.disponibilidade[nome_professor].get('Observações', ''), 
                     key=f"{nome_professor}_observacoes")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Função para converter os dados para DataFrame
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

# Converter os dados coletados para um DataFrame
df_novo = converter_para_dataframe(st.session_state.disponibilidade, nome_preenchedor, data_modificacao)

# Botão para salvar os dados na tabela em tempo real
if st.button("Salvar dados"):
    st.session_state.df_disponibilidade = pd.concat([st.session_state.df_disponibilidade, df_novo], ignore_index=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success("Dados salvos com sucesso!")

# Definir uma lista de usuários com permissões especiais
usuarios_superadmin = ["BrunoMorgilloCoordenadorSUPERADMIN_123456", "LuizaDiretoraSUPERADMIN", "EleyneDiretoraSUPERADMIN"]

# Verificar se o nome do preenchedor está na lista de usuários com permissões especiais
if nome_preenchedor in usuarios_superadmin:
    st.subheader("Tabela Atualizada de Disponibilidade")

    # Iterar sobre as linhas do DataFrame e exibir as informações com botões de deletar
    for i, row in st.session_state.df_disponibilidade.iterrows():
        cols = st.columns(len(row) + 1)  # +1 para o botão de deletar
        for j, value in enumerate(row):
            cols[j].write(value)
        
        # Exibir o botão de deletar apenas se o nome do preenchedor estiver na lista de permissões
        if cols[len(row)].button("Deletar", key=f"delete_{i}"):
            deletar_linha(i)

    # Botão para exportar os dados para Excel, visível para todos os usuários na lista de permissões especiais
    st.subheader("Exportar Dados para Excel")
    if st.button("Exportar para Excel"):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.df_disponibilidade.to_excel(writer, index=False, sheet_name='Disponibilidade')
        buffer.seek(0)
        
        st.download_button(
            label="Baixar Excel",
            data=buffer,
            file_name="disponibilidade_professores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
