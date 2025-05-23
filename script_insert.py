import os
import psycopg2
from faker import Faker
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

# Carregar variáveis de ambiente
load_dotenv()

# Criar conexão com o banco
conn = psycopg2.connect(
    user=os.getenv("user"),
    password=os.getenv("password"),
    host=os.getenv("host"),
    port=os.getenv("port"),
    dbname=os.getenv("dbname")
)
cur = conn.cursor()

# Inicializar Faker para português
fake = Faker('pt_BR')

# Dados hard coded para Avaliacao (boas e ruins) - EXPANDIDO
avaliacoes_hardcoded = [
    # Avaliações negativas
    "Demora no atendimento, muito insatisfeito",
    "Serviço mal executado, não recomendo",
    "Preço acima do esperado, não vale o que cobra",
    "Falta de profissionalismo do prestador",
    "Não cumpriu o prazo acordado",
    "Atendimento ruim e sem educação",
    "Produto entregue com defeito",
    "Falta de comunicação durante o serviço",
    "Cobrança indevida de valores extras",
    "Não resolveu o problema completamente",
    "Chegou embriagado para trabalhar",
    "Quebrou objetos da casa e não assumiu",
    "Usou material de baixa qualidade",
    "Abandonou o serviço no meio",
    "Fez bagunça e não limpou",
    "Cobrou mais do que o combinado",
    "Trabalho ficou torto e mal feito",
    "Não trouxe as ferramentas prometidas",
    "Atrasou uma semana sem avisar",
    "Serviço durou muito mais que o esperado",
    # Avaliações positivas
    "Excelente serviço, muito satisfeito",
    "Profissional competente e pontual",
    "Preço justo e serviço de qualidade",
    "Atendimento cordial e eficiente",
    "Cumpriu todos os prazos acordados",
    "Trabalho impecável, superou expectativas",
    "Muito educado e prestativo",
    "Ótima comunicação durante todo processo",
    "Preço honesto e transparente",
    "Resolveu tudo perfeitamente, recomendo",
    "Chegou no horário e terminou antes",
    "Trabalho de alta qualidade, nota 10",
    "Muito caprichoso e detalhista",
    "Limpou tudo após terminar o serviço",
    "Deu dicas valiosas para manutenção",
    "Preço melhor que a concorrência",
    "Profissional experiente e confiável",
    "Resolveu problemas que nem pedi",
    "Atendimento excepcional do início ao fim",
    "Voltaria a contratar sem dúvida"
]

# Descrições hard coded para Solicitacao - EXPANDIDO
descricoes_solicitacao = [
    # Serviços elétricos
    "Instalação de tomadas e interruptores na sala",
    "Troca de chuveiro elétrico",
    "Instalação de ventilador de teto",
    "Reparo na fiação do quarto",
    "Instalação de lustre na sala de jantar",
    "Troca do disjuntor principal",
    "Instalação de campainha eletrônica",
    "Reparo em tomada que deu curto",
    "Instalação de sensor de presença",
    "Troca de lâmpadas queimadas",
    # Serviços hidráulicos
    "Reparo de vazamento na cozinha",
    "Desentupimento de pia",
    "Conserto de torneira que goteja",
    "Instalação de filtro de água",
    "Troca de registro do banheiro",
    "Reparo no vaso sanitário",
    "Instalação de ducha higiênica",
    "Conserto de vazamento no telhado",
    "Desentupimento de ralo",
    "Troca de mangueira da máquina de lavar",
    # Serviços de pintura
    "Pintura completa do quarto",
    "Pintura da fachada da casa",
    "Pintura de portão de ferro",
    "Pintura do teto da sala",
    "Retoque na pintura da parede",
    "Pintura de grade das janelas",
    "Pintura da garagem",
    "Aplicação de textura na parede",
    "Pintura de muros externos",
    "Pintura de móveis de madeira",
    # Serviços de jardinagem
    "Poda de árvores no jardim",
    "Plantio de grama no jardim",
    "Limpeza e manutenção do jardim",
    "Plantio de flores e arbustos",
    "Corte de grama e limpeza",
    "Poda de cerca viva",
    "Adubação do gramado",
    "Remoção de ervas daninhas",
    "Plantio de árvores frutíferas",
    "Instalação de sistema de irrigação",
    # Serviços de construção
    "Construção de muro no quintal",
    "Reforma do banheiro",
    "Assentamento de piso cerâmico",
    "Construção de churrasqueira",
    "Reforma da cozinha",
    "Construção de garagem",
    "Instalação de portão automático",
    "Construção de piscina",
    "Reforma do telhado",
    "Construção de área de lazer"
]

# Descrições hard coded para Reclamacao - EXPANDIDO
descricoes_reclamacao = [
    "O serviço não foi executado conforme combinado",
    "O prestador chegou com 2 horas de atraso",
    "Cobrança de material não utilizado",
    "Trabalho mal acabado, precisa refazer",
    "Não trouxe as ferramentas necessárias",
    "Deixou sujeira no local após o serviço",
    "Danificou móveis durante a execução",
    "Não cumpriu o prazo de entrega",
    "Atendimento grosseiro e sem educação",
    "Preço final muito diferente do orçamento",
    "Usou material de qualidade inferior ao combinado",
    "Não apareceu no dia marcado sem avisar",
    "Trabalho ficou com acabamento ruim",
    "Cobrou taxa extra não mencionada antes",
    "Deixou ferramentas esquecidas no local",
    "Não limpou a bagunça que fez",
    "Serviço parou no meio sem explicação",
    "Atendeu telefone durante o trabalho",
    "Não seguiu as instruções dadas",
    "Trabalho apresentou defeito no dia seguinte",
    "Chegou em estado inadequado para trabalhar",
    "Não respeitou os horários combinados",
    "Fez serviço diferente do solicitado",
    "Danificou a parede durante a instalação",
    "Não trouxe material suficiente para terminar"
]

# Descrições hard coded para Evidencia - EXPANDIDO
descricoes_evidencia = [
    "Foto mostrando o serviço mal executado",
    "Imagem do vazamento que não foi resolvido",
    "Foto da parede com pintura descascando",
    "Evidência dos danos causados nos móveis",
    "Imagem da sujeira deixada no local",
    "Foto do material cobrado mas não utilizado",
    "Registro do atraso no horário combinado",
    "Imagem comparando antes e depois do serviço",
    "Foto da ferramenta esquecida no local",
    "Evidência da diferença no orçamento",
    "Foto do piso rachado após instalação",
    "Imagem da torneira ainda vazando",
    "Foto da pintura com manchas",
    "Registro da bagunça deixada no quintal",
    "Imagem do portão mal instalado",
    "Foto do fio elétrico mal conectado",
    "Evidência do material de baixa qualidade usado",
    "Imagem do trabalho inacabado",
    "Foto da parede suja após pintura",
    "Registro do horário de chegada atrasado",
    "Imagem do vazamento no teto",
    "Foto da grama mal plantada",
    "Evidência do dano no móvel da sala",
    "Imagem da instalação torta",
    "Foto do entulho deixado no local"
]

# Função para gerar telefone padronizado
def gerar_telefone():
    # Formato: (11) 99999-9999
    ddds = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '21', '22', '24', 
            '27', '28', '31', '32', '33', '34', '35', '37', '38', '41', '42', '43', 
            '44', '45', '46', '47', '48', '49', '51', '53', '54', '55', '61', '62', 
            '63', '64', '65', '66', '67', '68', '69', '71', '73', '74', '75', '77', 
            '79', '81', '82', '83', '84', '85', '86', '87', '88', '89', '91', '92', 
            '93', '94', '95', '96', '97', '98', '99']
    ddd = random.choice(ddds)
    numero = f"9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    return f"({ddd}) {numero}"

# Função para inserir dados na tabela Cliente
def inserir_clientes(n):
    for _ in range(n):
        nome = fake.name()
        email = fake.email()
        telefone = gerar_telefone()
        cur.execute("INSERT INTO Cliente (nome, email, telefone) VALUES (%s, %s, %s) RETURNING id", (nome, email, telefone))
    conn.commit()

# Função para inserir dados na tabela Prestador
def inserir_prestadores(n):
    for _ in range(n):
        nome = fake.name()
        email = fake.email()
        telefone = gerar_telefone()
        cur.execute("INSERT INTO Prestador (nome, email, telefone) VALUES (%s, %s, %s) RETURNING id", (nome, email, telefone))
    conn.commit()

# Função para inserir dados na tabela Solicitacao
def inserir_solicitacoes(n, clientes_ids, prestadores_ids):
    status_options = ['Aberto', 'Em andamento', 'Concluído', 'Cancelado', 'Aguardando pagamento', 'Em análise']
    for _ in range(n):
        id_cliente = random.choice(clientes_ids)
        id_prestador = random.choice(prestadores_ids)
        descricao = random.choice(descricoes_solicitacao)
        valor = round(random.uniform(50, 1500), 2)
        data_criacao = fake.date_between(start_date='-1y', end_date='today')
        status = random.choice(status_options)
        cur.execute("INSERT INTO Solicitacao (id_cliente, id_prestador, descricao, valor, data_criacao, status) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id", 
                    (id_cliente, id_prestador, descricao, valor, data_criacao, status))
    conn.commit()

# Função para inserir dados na tabela Reclamacao
def inserir_reclamacoes(n, solicitacoes_ids):
    status_options = ['Aberto', 'Em análise', 'Resolvido', 'Fechado', 'Aguardando resposta', 'Em mediação']
    for _ in range(n):
        id_solicitacao = random.choice(solicitacoes_ids)
        descricao = random.choice(descricoes_reclamacao)
        status = random.choice(status_options)
        cur.execute("INSERT INTO Reclamacao (id_solicitacao, descricao, status) VALUES (%s, %s, %s) RETURNING id", 
                    (id_solicitacao, descricao, status))
    conn.commit()

# Função para inserir dados na tabela evidencia
def inserir_evidencias(n, reclamacoes_ids):
    for _ in range(n):
        id_reclamacao = random.choice(reclamacoes_ids)
        descricao = random.choice(descricoes_evidencia)
        data_envio = fake.date_between(start_date='-1y', end_date='today')
        foto = f"evidencia_{random.randint(1000, 9999)}.jpg"
        cur.execute("INSERT INTO evidencia (id_reclamacao, descricao, data_envio, foto) VALUES (%s, %s, %s, %s)", 
                    (id_reclamacao, descricao, data_envio, foto))
    conn.commit()

# Função para inserir dados na tabela pagamento
def inserir_pagamentos(n, solicitacoes_ids):
    status_options = ['Pendente', 'Pago', 'Cancelado', 'Estornado', 'Em processamento', 'Vencido']
    for _ in range(n):
        id_solicitacao = random.choice(solicitacoes_ids)
        valor = round(random.uniform(50, 1500), 2)
        status = random.choice(status_options)
        data_pagamento = fake.date_between(start_date='-1y', end_date='today')
        cur.execute("INSERT INTO pagamento (id_solicitacao, valor, status, data_pagamento) VALUES (%s, %s, %s, %s)", 
                    (id_solicitacao, valor, status, data_pagamento))
    conn.commit()

# Função para inserir dados na tabela Avaliacao
def inserir_avaliacoes(n, clientes_ids, prestadores_ids):
    estrelas_options = ['1', '2', '3', '4', '5']
    for _ in range(n):
        id_cliente = random.choice(clientes_ids)
        id_prestador = random.choice(prestadores_ids)
        qtd_estrelas = random.choice(estrelas_options)
        comentario = random.choice(avaliacoes_hardcoded)
        data_avaliacao = fake.date_between(start_date='-1y', end_date='today')
        cur.execute("INSERT INTO Avalicao (id_cliente, id_prestador, qtd_estrelas, comentario, data_avaliacao) VALUES (%s, %s, %s, %s, %s)", 
                    (id_cliente, id_prestador, qtd_estrelas, comentario, data_avaliacao))
    conn.commit()

# Função para inserir dados na tabela Especialidade
def inserir_especialidades(especialidades):
    for nome in especialidades:
        cur.execute("INSERT INTO Especialidade (nome) VALUES (%s) RETURNING id", (nome,))
    conn.commit()

# Função para inserir dados na tabela Prestador_especialidade
def inserir_prestador_especialidade(prestadores_ids, especialidades_ids):
    for id_prestador in prestadores_ids:
        # Cada prestador pode ter 1-3 especialidades
        num_especialidades = random.randint(1, 3)
        especialidades_escolhidas = random.sample(especialidades_ids, min(num_especialidades, len(especialidades_ids)))
        for id_especialidade in especialidades_escolhidas:
            try:
                cur.execute("INSERT INTO Prestador_especialidade (id_prestador, id_especialidade) VALUES (%s, %s)", (id_prestador, id_especialidade))
            except:
                # Ignora se já existe a combinação
                pass
    conn.commit()

# Exemplo de uso das funções para popular o banco
print("Inserindo clientes...")
inserir_clientes(25)

print("Inserindo prestadores...")
inserir_prestadores(15)

# Obter ids de clientes e prestadores
cur.execute("SELECT id FROM Cliente")
clientes_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT id FROM Prestador")
prestadores_ids = [row[0] for row in cur.fetchall()]

print("Inserindo solicitações...")
inserir_solicitacoes(50, clientes_ids, prestadores_ids)

# Obter ids de solicitações
cur.execute("SELECT id FROM Solicitacao")
solicitacoes_ids = [row[0] for row in cur.fetchall()]

print("Inserindo reclamações...")
inserir_reclamacoes(25, solicitacoes_ids)

# Obter ids de reclamações
cur.execute("SELECT id FROM Reclamacao")
reclamacoes_ids = [row[0] for row in cur.fetchall()]

print("Inserindo evidências...")
inserir_evidencias(30, reclamacoes_ids)

print("Inserindo pagamentos...")
inserir_pagamentos(40, solicitacoes_ids)

print("Inserindo avaliações...")
inserir_avaliacoes(35, clientes_ids, prestadores_ids)

# Inserir especialidades expandidas
especialidades = [
    'Eletricista', 'Encanador', 'Pintor', 'Jardineiro', 'Pedreiro',
    'Marceneiro', 'Serralheiro', 'Vidraceiro', 'Gesseiro', 'Azulejista',
    'Piscineiro', 'Soldador', 'Carpinteiro', 'Tapeceiro', 'Chaveiro'
]
print("Inserindo especialidades...")
inserir_especialidades(especialidades)

# Obter ids de especialidades
cur.execute("SELECT id FROM Especialidade")
especialidades_ids = [row[0] for row in cur.fetchall()]

print("Associando prestadores às especialidades...")
inserir_prestador_especialidade(prestadores_ids, especialidades_ids)

# Fechar conexão
cur.close()
conn.close()
