# CC5232-Projeto de Banco de Dados — SISTEMA DE SERVIÇOS

## Integrantes do Grupo

- Vitor Monteiro Vianna — RA: 22.223.085-6
- Hugo Emílio Nomura — RA: 22.123.051-9
- Danilo Henrique de Paulo — RA: 22.222.008-9

## 📚 Descrição do Projeto

Este projeto simula um sistema de serviços, com foco na modelagem e manipulação de banco de dados. Ele contém:

- Modelo relacional e entidade-relacionamento
- Scripts SQL para criação das tabelas e execução de queries (pasta `sql_structure` e `queries`)
- Scripts Python para inserção de dados fictícios e verificação de integridade dos dados

## 🚀 Como Executar o Projeto

1. **Crie e ative o ambiente virtual:**

   No Linux/macOS:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   No Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Crie um arquivo `.env` na raiz do projeto** com as variáveis de conexão:

   Exemplo:
   ```
   user=postgres.erdikmrhnakmlwrzftrc
   password=senha_do_banco
   host=aws-0-sa-east-1.pooler.supabase.com
   port=5432
   dbname=postgres
   ```

4. **Execute os scripts:**

   - Para inserir dados fictícios:

     ```bash
     python script_insert.py
     ```

   - Para verificar a integridade dos dados:

     ```bash
     python script_db_verification.py
     ```

## 📊 Diagramas

![image](https://github.com/user-attachments/assets/188f34d9-15c8-447b-9999-c590708cbc38)
![image (2)](https://github.com/user-attachments/assets/4af86bc6-ab7c-48fe-8d37-3f9302710f01)