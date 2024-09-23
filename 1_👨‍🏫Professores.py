import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

st.set_page_config(layout="wide")

# Função para carregar os dados de um arquivo CSV
def carregar_dados():
    if os.path.exists("disponibilidade.csv"):
        return pd.read_csv("disponibilidade.csv")
    else:
        return pd.DataFrame(columns=['Professor', 'Unidades', 'Carro', 'Máquinas', 'Disponibilidade', 'Módulo', 'Idioma', 'Observações', 'Nome do Preenchendor', 'Data'])

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

# Define a largura das colunas
col_widths = [1, 1, 1, 1, 1, 1, 1, 1]

# Adicionando CSS para melhorar a visualização e adicionar scroll
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
    .scrollable-container {
        max-height: 500px;
        overflow-y: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

for i, nome_inicial in enumerate(nomes_iniciais):
    # Primeira linha com "Nome do professor", "Unidades", "Carro" e "Máquina"
    cols1 = st.columns([2, 1, 1, 1])  # Ajusta a largura das colunas para a primeira linha

    with cols1[0]:
        nome_professor = st.text_input(f"Nome do professor", nome_inicial, key=f"nome_{i}")

    # Atualiza o nome do professor no session state
    if nome_professor != nome_inicial:
        st.session_state.disponibilidade[nome_professor] = st.session_state.disponibilidade.pop(nome_inicial, {})

    # Atualiza o dicionário com base no session state
    if nome_professor not in st.session_state.disponibilidade:
        st.session_state.disponibilidade[nome_professor] = {}

    with cols1[1]:
        st.write("Unidades")
        for unidade in unidades:
            st.session_state.disponibilidade[nome_professor][unidade] = st.checkbox(f"{unidade}", 
                value=st.session_state.disponibilidade[nome_professor].get(unidade, False), 
                key=f"{nome_professor}_{unidade}")

    with cols1[2]:
        st.write("Carro")
        st.session_state.disponibilidade[nome_professor]['Carro'] = st.checkbox("Tem carro", 
            value=st.session_state.disponibilidade[nome_professor].get('Carro', False), 
            key=f"{nome_professor}_carro")

    with cols1[3]:
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

    # Segunda linha com "Disponibilidade", "Módulo", "Idioma" e "Observações"
    cols2 = st.columns([1, 1, 1, 2])  # Ajusta a largura das colunas para a segunda linha

    with cols2[0]:
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

    with cols2[1]:
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
            modulo_opcoes['Kids'] = st.checkbox("Kids", 
                value='Kids' in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                key=f"{nome_professor}_kids")
            modulo_opcoes['In-Company'] = st.checkbox("In-Company", 
                value='In-Company' in st.session_state.disponibilidade[nome_professor].get('Modulo', []), 
                key=f"{nome_professor}_incompany")
            st.markdown('</div>', unsafe_allow_html=True)
        st.session_state.disponibilidade[nome_professor]['Modulo'] = [key for key, value in modulo_opcoes.items() if value]

    with cols2[2]:
        st.write("Idioma")
        idioma_opcoes = {}
        with st.container():
            st.markdown('<div class="checkbox-no-wrap">', unsafe_allow_html=True)
            idioma_opcoes['Inglês'] = st.checkbox("Inglês", 
                value='Inglês' in st.session_state.disponibilidade[nome_professor].get('Idioma', []), 
                key=f"{nome_professor}_ingles")
            idioma_opcoes['Espanhol'] = st.checkbox("Espanhol", 
                value='Espanhol' in st.session_state.disponibilidade[nome_professor].get('Idioma', []), 
                key=f"{nome_professor}_espanhol")
            st.markdown('</div>', unsafe_allow_html=True)
        st.session_state.disponibilidade[nome_professor]['Idioma'] = [key for key, value in idioma_opcoes.items() if value]

    with cols2[3]:
        st.session_state.disponibilidade[nome_professor]['Observações'] = st.text_area("Observações", 
            value=st.session_state.disponibilidade[nome_professor].get('Observações', ''), 
            key=f"{nome_professor}_observacoes")

# Função para converter os dados para DataFrame
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
            'Idioma': ', '.join(detalhes.get('Idioma', [])),  # Adicionando a coluna de Idioma
            'Observações': detalhes.get('Observações', ''),
            'Nome do Preenchendor': nome_usuario,
            'Data': data.strftime('%Y-%m-%d')  # Garantindo que a data seja formatada sem hora
        }
        registros.append(registro)
    return pd.DataFrame(registros)

# Converter os dados coletados para um DataFrame
df_novo = converter_para_dataframe(st.session_state.disponibilidade, nome_preenchedor, data_modificacao)

# Adiciona uma variável no session_state para controlar o salvamento
if 'save_button_clicked' not in st.session_state:
    st.session_state.save_button_clicked = False

# Botão para salvar os dados na tabela em tempo real
if st.button("Salvar dados"):
    st.session_state.save_button_clicked = True

    
# Somente salva os dados se o botão foi clicado
if st.session_state.save_button_clicked:
    df_novo = converter_para_dataframe(st.session_state.disponibilidade, nome_preenchedor, data_modificacao)
    st.session_state.df_disponibilidade = pd.concat([st.session_state.df_disponibilidade, df_novo], ignore_index=True)
    salvar_dados(st.session_state.df_disponibilidade)
    st.success("Dados salvos com sucesso!")
    st.session_state.save_button_clicked = False  # Reseta o estado do botão

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
            file_name="PROFESSORES.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
