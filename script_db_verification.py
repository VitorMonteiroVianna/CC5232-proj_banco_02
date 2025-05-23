import os
import psycopg2
from dotenv import load_dotenv
import re
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Criar conexão com o banco
def criar_conexao():
    return psycopg2.connect(
        user=os.getenv("user"),
        password=os.getenv("password"),
        host=os.getenv("host"),
        port=os.getenv("port"),
        dbname=os.getenv("dbname")
    )

# ========== VALIDAÇÕES DE FORMATO ==========

def validar_telefone(telefone):
    """Valida formato: (XX) 9XXXX-XXXX"""
    pattern = r"^\(\d{2}\) 9\d{4}-\d{4}$"
    return bool(re.match(pattern, telefone))

def validar_email(email):
    """Valida formato básico de email"""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email))

def validar_qtd_estrelas(qtd):
    """Valida se está entre 1 e 5"""
    return qtd in ['1', '2', '3', '4', '5']

def validar_data(data_str):
    """Valida formato de data"""
    try:
        datetime.strptime(str(data_str), '%Y-%m-%d')
        return True
    except:
        return False

def validar_valor_monetario(valor):
    """Valida se é um valor positivo"""
    try:
        return float(valor) > 0
    except:
        return False

# ========== VALIDAÇÕES POR TABELA ==========

def validar_cliente(row):
    """Valida dados de um cliente"""
    erros = []
    
    if not isinstance(row.get('nome'), str) or len(row['nome'].strip()) == 0:
        erros.append("Nome inválido ou vazio")
    
    if not validar_email(row.get('email', '')):
        erros.append("Email com formato inválido")
    
    if not validar_telefone(row.get('telefone', '')):
        erros.append("Telefone com formato inválido")
    
    return erros

def validar_prestador(row):
    """Valida dados de um prestador"""
    erros = []
    
    if not isinstance(row.get('nome'), str) or len(row['nome'].strip()) == 0:
        erros.append("Nome inválido ou vazio")
    
    if not validar_email(row.get('email', '')):
        erros.append("Email com formato inválido")
    
    if not validar_telefone(row.get('telefone', '')):
        erros.append("Telefone com formato inválido")
    
    return erros

def validar_solicitacao(row):
    """Valida dados de uma solicitação"""
    erros = []
    status_validos = ['Aberto', 'Em andamento', 'Concluído', 'Cancelado', 'Aguardando pagamento', 'Em análise']
    
    if not validar_valor_monetario(row.get('valor')):
        erros.append("Valor deve ser positivo")
    
    if row.get('status') not in status_validos:
        erros.append(f"Status inválido. Deve ser um de: {', '.join(status_validos)}")
    
    if not validar_data(row.get('data_criacao')):
        erros.append("Data de criação inválida")
    
    if not isinstance(row.get('descricao'), str) or len(row['descricao'].strip()) == 0:
        erros.append("Descrição inválida ou vazia")
    
    return erros

def validar_reclamacao(row):
    """Valida dados de uma reclamação"""
    erros = []
    status_validos = ['Aberto', 'Em análise', 'Resolvido', 'Fechado', 'Aguardando resposta', 'Em mediação']
    
    if row.get('status') not in status_validos:
        erros.append(f"Status inválido. Deve ser um de: {', '.join(status_validos)}")
    
    if not isinstance(row.get('descricao'), str) or len(row['descricao'].strip()) == 0:
        erros.append("Descrição inválida ou vazia")
    
    return erros

def validar_evidencia(row):
    """Valida dados de uma evidência"""
    erros = []
    
    if not validar_data(row.get('data_envio')):
        erros.append("Data de envio inválida")
    
    foto = row.get('foto', '')
    if not (foto.endswith('.jpg') or foto.endswith('.png') or foto.endswith('.jpeg')):
        erros.append("Arquivo de foto deve ter extensão .jpg, .jpeg ou .png")
    
    if not isinstance(row.get('descricao'), str) or len(row['descricao'].strip()) == 0:
        erros.append("Descrição inválida ou vazia")
    
    return erros

def validar_pagamento(row):
    """Valida dados de um pagamento"""
    erros = []
    status_validos = ['Pendente', 'Pago', 'Cancelado', 'Estornado', 'Em processamento', 'Vencido']
    
    if row.get('status') not in status_validos:
        erros.append(f"Status inválido. Deve ser um de: {', '.join(status_validos)}")
    
    if not validar_valor_monetario(row.get('valor')):
        erros.append("Valor deve ser positivo")
    
    if not validar_data(row.get('data_pagamento')):
        erros.append("Data de pagamento inválida")
    
    return erros

def validar_avaliacao(row):
    """Valida dados de uma avaliação"""
    erros = []
    
    if not validar_qtd_estrelas(row.get('qtd_estrelas')):
        erros.append("Quantidade de estrelas deve ser entre 1 e 5")
    
    if not isinstance(row.get('comentario'), str) or len(row['comentario'].strip()) == 0:
        erros.append("Comentário inválido ou vazio")
    
    if not validar_data(row.get('data_avaliacao')):
        erros.append("Data de avaliação inválida")
    
    return erros

def validar_especialidade(row):
    """Valida dados de uma especialidade"""
    erros = []
    
    if not isinstance(row.get('nome'), str) or len(row['nome'].strip()) == 0:
        erros.append("Nome da especialidade inválido ou vazio")
    
    return erros

# ========== VALIDAÇÕES DE REGRAS DE NEGÓCIO ==========

def validar_integridade_referencial(conn):
    """Valida integridade referencial entre tabelas"""
    cur = conn.cursor()
    erros = []
    
    # Verificar se todas as solicitações têm cliente e prestador válidos
    cur.execute("""
        SELECT s.id, s.id_cliente, s.id_prestador 
        FROM Solicitacao s 
        LEFT JOIN Cliente c ON s.id_cliente = c.id 
        LEFT JOIN Prestador p ON s.id_prestador = p.id 
        WHERE c.id IS NULL OR p.id IS NULL
    """)
    solicitacoes_invalidas = cur.fetchall()
    if solicitacoes_invalidas:
        erros.append(f"Solicitações com cliente/prestador inválido: {solicitacoes_invalidas}")
    
    # Verificar se todas as reclamações têm solicitação válida
    cur.execute("""
        SELECT r.id, r.id_solicitacao 
        FROM Reclamacao r 
        LEFT JOIN Solicitacao s ON r.id_solicitacao = s.id 
        WHERE s.id IS NULL
    """)
    reclamacoes_invalidas = cur.fetchall()
    if reclamacoes_invalidas:
        erros.append(f"Reclamações sem solicitação válida: {reclamacoes_invalidas}")
    
    # Verificar se todas as evidências têm reclamação válida
    cur.execute("""
        SELECT e.id, e.id_reclamacao 
        FROM evidencia e 
        LEFT JOIN Reclamacao r ON e.id_reclamacao = r.id 
        WHERE r.id IS NULL
    """)
    evidencias_invalidas = cur.fetchall()
    if evidencias_invalidas:
        erros.append(f"Evidências sem reclamação válida: {evidencias_invalidas}")
    
    # Verificar se todos os pagamentos têm solicitação válida
    cur.execute("""
        SELECT p.id, p.id_solicitacao 
        FROM pagamento p 
        LEFT JOIN Solicitacao s ON p.id_solicitacao = s.id 
        WHERE s.id IS NULL
    """)
    pagamentos_invalidos = cur.fetchall()
    if pagamentos_invalidos:
        erros.append(f"Pagamentos sem solicitação válida: {pagamentos_invalidos}")
    
    # Verificar se todas as avaliações têm cliente e prestador válidos
    cur.execute("""
        SELECT a.id, a.id_cliente, a.id_prestador 
        FROM Avalicao a 
        LEFT JOIN Cliente c ON a.id_cliente = c.id 
        LEFT JOIN Prestador p ON a.id_prestador = p.id 
        WHERE c.id IS NULL OR p.id IS NULL
    """)
    avaliacoes_invalidas = cur.fetchall()
    if avaliacoes_invalidas:
        erros.append(f"Avaliações com cliente/prestador inválido: {avaliacoes_invalidas}")
    
    # Verificar se prestador_especialidade tem prestador e especialidade válidos
    cur.execute("""
        SELECT pe.id_prestador, pe.id_especialidade 
        FROM Prestador_especialidade pe 
        LEFT JOIN Prestador p ON pe.id_prestador = p.id 
        LEFT JOIN Especialidade e ON pe.id_especialidade = e.id 
        WHERE p.id IS NULL OR e.id IS NULL
    """)
    pe_invalidas = cur.fetchall()
    if pe_invalidas:
        erros.append(f"Prestador_especialidade inválidas: {pe_invalidas}")
    
    cur.close()
    return erros

def validar_regras_negocio_especificas(conn):
    """Valida regras de negócio específicas"""
    cur = conn.cursor()
    erros = []
    
    # Verificar se há pagamentos com valor diferente da solicitação
    cur.execute("""
        SELECT p.id, p.valor as valor_pagamento, s.valor as valor_solicitacao 
        FROM pagamento p 
        JOIN Solicitacao s ON p.id_solicitacao = s.id 
        WHERE p.valor != s.valor AND p.status = 'Pago'
    """)
    pagamentos_divergentes = cur.fetchall()
    if pagamentos_divergentes:
        erros.append(f"Pagamentos com valor divergente da solicitação: {pagamentos_divergentes}")
    
    # Verificar se há reclamações para solicitações não concluídas
    cur.execute("""
        SELECT r.id, s.status 
        FROM Reclamacao r 
        JOIN Solicitacao s ON r.id_solicitacao = s.id 
        WHERE s.status NOT IN ('Concluído', 'Cancelado')
    """)
    reclamacoes_prematuras = cur.fetchall()
    if reclamacoes_prematuras:
        erros.append(f"Reclamações para solicitações não finalizadas: {reclamacoes_prematuras}")
    
    # Verificar se há avaliações duplicadas (mesmo cliente para mesmo prestador)
    cur.execute("""
        SELECT id_cliente, id_prestador, COUNT(*) 
        FROM Avalicao 
        GROUP BY id_cliente, id_prestador 
        HAVING COUNT(*) > 1
    """)
    avaliacoes_duplicadas = cur.fetchall()
    if avaliacoes_duplicadas:
        erros.append(f"Avaliações duplicadas (cliente-prestador): {avaliacoes_duplicadas}")
    
    # Verificar emails duplicados em clientes
    cur.execute("""
        SELECT email, COUNT(*) 
        FROM Cliente 
        GROUP BY email 
        HAVING COUNT(*) > 1
    """)
    emails_duplicados_cliente = cur.fetchall()
    if emails_duplicados_cliente:
        erros.append(f"Emails duplicados em clientes: {emails_duplicados_cliente}")
    
    # Verificar emails duplicados em prestadores
    cur.execute("""
        SELECT email, COUNT(*) 
        FROM Prestador 
        GROUP BY email 
        HAVING COUNT(*) > 1
    """)
    emails_duplicados_prestador = cur.fetchall()
    if emails_duplicados_prestador:
        erros.append(f"Emails duplicados em prestadores: {emails_duplicados_prestador}")
    
    cur.close()
    return erros

# ========== VALIDAÇÃO DE DADOS EM TABELAS ==========

def validar_dados_tabela(conn, tabela, funcao_validacao):
    """Valida todos os dados de uma tabela"""
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {tabela}")
    colunas = [desc[0] for desc in cur.description]
    linhas = cur.fetchall()
    
    erros_tabela = []
    for i, linha in enumerate(linhas):
        row_dict = dict(zip(colunas, linha))
        erros_linha = funcao_validacao(row_dict)
        if erros_linha:
            erros_tabela.append(f"Linha {i+1} (ID: {row_dict.get('id', 'N/A')}): {'; '.join(erros_linha)}")
    
    cur.close()
    return erros_tabela

# ========== VERIFICAÇÃO DE QUERIES SQL ==========

def verificar_queries_sql(caminho_pasta, conn):
    """Executa todas as queries .sql da pasta e verifica erros"""
    erros = {}
    
    if not os.path.exists(caminho_pasta):
        return {"erro_pasta": f"Pasta '{caminho_pasta}' não encontrada"}
    
    cur = conn.cursor()
    arquivos_sql = [f for f in os.listdir(caminho_pasta) if f.endswith('.sql')]
    
    if not arquivos_sql:
        return {"aviso": "Nenhum arquivo .sql encontrado na pasta"}
    
    for arquivo in arquivos_sql:
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as file:
                query = file.read().strip()
            
            if query:  # Só executa se não estiver vazio
                cur.execute(query)
                conn.commit()
        except Exception as e:
            erros[arquivo] = str(e)
            conn.rollback()  # Desfaz mudanças em caso de erro
    
    cur.close()
    return erros

# ========== FUNÇÃO PRINCIPAL DE VALIDAÇÃO ==========

def executar_validacao_completa(caminho_queries="queries"):
    """Executa todas as validações do sistema"""
    print("=== INICIANDO VALIDAÇÃO COMPLETA DO SISTEMA ===\n")
    
    try:
        conn = criar_conexao()
        print("✓ Conexão com banco estabelecida\n")
    except Exception as e:
        print(f"✗ Erro na conexão: {e}")
        return
    
    relatorio = {
        "validacao_formato": {},
        "integridade_referencial": [],
        "regras_negocio": [],
        "queries_sql": {}
    }
    
    # 1. Validação de formato dos dados
    print("1. VALIDANDO FORMATO DOS DADOS")
    print("-" * 40)
    
    tabelas_validacao = {
        "Cliente": validar_cliente,
        "Prestador": validar_prestador,
        "Solicitacao": validar_solicitacao,
        "Reclamacao": validar_reclamacao,
        "evidencia": validar_evidencia,
        "pagamento": validar_pagamento,
        "Avalicao": validar_avaliacao,
        "Especialidade": validar_especialidade
    }
    
    for tabela, funcao in tabelas_validacao.items():
        print(f"Validando {tabela}...")
        erros = validar_dados_tabela(conn, tabela, funcao)
        relatorio["validacao_formato"][tabela] = erros
        if erros:
            print(f"  ✗ {len(erros)} erro(s) encontrado(s)")
        else:
            print(f"  ✓ Sem erros")
    
    # 2. Validação de integridade referencial
    print(f"\n2. VALIDANDO INTEGRIDADE REFERENCIAL")
    print("-" * 40)
    erros_integridade = validar_integridade_referencial(conn)
    relatorio["integridade_referencial"] = erros_integridade
    if erros_integridade:
        print(f"✗ {len(erros_integridade)} erro(s) de integridade encontrado(s)")
        for erro in erros_integridade:
            print(f"  - {erro}")
    else:
        print("✓ Integridade referencial OK")
    
    # 3. Validação de regras de negócio
    print(f"\n3. VALIDANDO REGRAS DE NEGÓCIO")
    print("-" * 40)
    erros_negocio = validar_regras_negocio_especificas(conn)
    relatorio["regras_negocio"] = erros_negocio
    if erros_negocio:
        print(f"✗ {len(erros_negocio)} erro(s) de regra de negócio encontrado(s)")
        for erro in erros_negocio:
            print(f"  - {erro}")
    else:
        print("✓ Regras de negócio OK")
    
    # 4. Verificação de queries SQL
    print(f"\n4. VERIFICANDO QUERIES SQL")
    print("-" * 40)
    erros_queries = verificar_queries_sql(caminho_queries, conn)
    relatorio["queries_sql"] = erros_queries
    if erros_queries:
        if "erro_pasta" in erros_queries:
            print(f"✗ {erros_queries['erro_pasta']}")
        elif "aviso" in erros_queries:
            print(f"⚠ {erros_queries['aviso']}")
        else:
            print(f"✗ {len(erros_queries)} arquivo(s) com erro")
            for arquivo, erro in erros_queries.items():
                print(f"  - {arquivo}: {erro}")
    else:
        print("✓ Todas as queries executaram com sucesso")
    
    conn.close()
    
    # Resumo final
    print(f"\n=== RESUMO DA VALIDAÇÃO ===")
    total_erros_formato = sum(len(erros) for erros in relatorio["validacao_formato"].values())
    total_erros = (total_erros_formato + 
                   len(relatorio["integridade_referencial"]) + 
                   len(relatorio["regras_negocio"]) + 
                   len([e for e in relatorio["queries_sql"] if not e.startswith("aviso")]))
    
    if total_erros == 0:
        print("✓ SISTEMA VALIDADO COM SUCESSO - Nenhum erro encontrado!")
    else:
        print(f"✗ VALIDAÇÃO CONCLUÍDA - {total_erros} erro(s) encontrado(s)")
        print("Verifique os detalhes acima para correção.")
    
    return relatorio

# ========== EXECUÇÃO ==========

if __name__ == "__main__":
    # Executar validação completa
    resultado = executar_validacao_completa()
    
    # Opcional: Salvar relatório em arquivo
    # import json
    # with open('relatorio_validacao.json', 'w', encoding='utf-8') as f:
    #     json.dump(resultado, f, indent=2, ensure_ascii=False)
