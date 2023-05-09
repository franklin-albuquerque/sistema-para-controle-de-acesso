from bcrypt import checkpw, hashpw, gensalt
from dotenv import dotenv_values
from os import path
from psycopg2 import connect, DatabaseError

def criptografar(senha):
    # Cria um salt aleatório com fator de complexidade 13
    salt = gensalt(13)

    # Cria um hash da senha usando o salt gerado
    senha_criptografada = hashpw(senha.encode('utf-8'), salt)

    # Retorna a senha criptografada como um conjunto de bytes
    return senha_criptografada

def criar_tabela():
    # Estabelece uma conexão com o banco de dados
    conexao = conectar_ao_banco()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Define uma consulta SQL para criar a tabela 'usuarios', se ela não existir
    consulta = '''CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL
    )'''

    # Executa a consulta SQL e confirma as alterações no banco de dados
    cursor.execute(consulta)
    conexao.commit()

    # Fecha o cursor e a conexão com o banco de dados
    cursor.close()
    conexao.close()

def conectar_ao_banco():
    # Inicializa a variável de conexão com o valor 'None'
    conexao = None

    # Verifica se o arquivo 'credenciais.env' existe
    if path.exists('credenciais.env'):
        # Carrega as configurações do banco de dados do arquivo 'credenciais.env'
        config = dotenv_values('credenciais.env', encoding='utf-16')

        # Estalece uma conexão com o banco de dados utilizando as credenciais carregadas
        conexao = connect(database = config['BANCO_DE_DADOS'],
                          host = config['HOST'],
                          user = config['USUARIO'],
                          password = config['SENHA'])
    else:
        # Exibe uma mensagem de erro caso o arquivo 'credenciais.env' não exista
        print('Não foi possível conectar ao banco de dados')

    # Retorna a conexão estabelecida, se houver, ou 'None' caso contrário
    return conexao

def inserir_na_tabela(nome, email, senha):
    # Estabelece uma conexão com o banco de dados
    conexao = conectar_ao_banco()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Consulta a tabela para inserir os dados do usuário
    try:
        # Define a consulta SQL para inserir os dados do usuário
        consulta = f"INSERT INTO usuarios (nome, email, senha) VALUES ('{nome}', '{email}', '{senha}')"

        # Executa a consulta SQL e confirma as alterações no banco de dados
        cursor.execute(consulta)
        conexao.commit()

        print('Usuário registrado com sucesso')

    # Se não for possível inserir os dados na tabela, exibe uma mensagem de erro
    except (Exception, DatabaseError) as erro:
        print(f'Erro: {erro}')

        # Reverte as últimas alterações feitas no banco
        conexao.rollback()

    finally:
        # Fecha o cursor e a conexão com o banco de dados
        cursor.close()
        conexao.close()

def obter_dados():
    # Estabelece uma conexão com o banco de dados
    conexao = conectar_ao_banco()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Define uma consulta SQL para selecionar os endereços de e-mail e senhas de todos os usuários
    consulta = "SELECT email, senha FROM usuarios"

    # Realiza a consulta SQL utilizando o cursor
    cursor.execute(consulta)

    # Armazena os daddos resultantes da consulta em uma variável chamada 'dados'
    dados = cursor.fetchall()

    # Retorna os dados obtidos na consulta
    return dados

def acessar_sistema():
    email = input('Digite seu endereço de e-mail: ')
    senha = input('Digite sua senha: ')

    try:
        # Estabelece uma conexão com o banco de dados
        conexao = conectar_ao_banco()
        cursor = conexao.cursor()

        # Executa uma consulta SQL para buscar os dados de e-amil e senha da tabela dos usuários
        consulta = "SELECT email, senha FROM usuarios"
        cursor.execute(consulta)
        dados = cursor.fetchall()

        # Itera sobre os resultados da consulta
        for info in dados:
            email_ = info[0]
            senha_ = info[1]

            # Compara se o email cadastrada corresponde algum usuário cadastrado
            if email_ == email:
                # Verifica se a senha digitada corresponde à senha cadastrada
                if checkpw(senha.encode('utf-8'), senha_.encode('utf-8')):
                    print('Acesso autorizado')
                else:
                    print('Senha incorreta')
                break
        else:
            # Exibe uma mensagem de erro, caso o e-mail digitado não corresponda a nenhum dos cadastrados
            print('Seu endereço de e-mail não está cadastrado no sistema')
    except:
        # Exibe uma mensagem de erro se não for possível acessar ao banco de dados
        print('Desculpe, não foi possível acessar o banco de dados')
    finally:
        # Fecha o cursor e a conexão com o banco de dados
        cursor.close()
        conexao.close()

def consultar_tabela(email):
    # Inicializa a variável 'resultado' como 'None'
    resultado = None

    # Conecta ao banco de dados e cria um cursor para executar consultas
    conexao = conectar_ao_banco()
    cursor = conexao.cursor()

    try:
        # Define a consulta para selecionar todos os e-mail da tabela 'usuarios'
        consulta = "SELECT email FROM usuarios"
        cursor.execute(consulta)

        # Armazena todos os resultados da consulta em 'dados'
        dados = cursor.fetchall()

        # Intera sobre os resultados da consulta
        for info in dados:
            # Armazena o e-mail do resultado atual em 'email_'
            email_ = info[0]

            # Verifica se o email digitado corresponde a algum e-mail cadastrado
            if email_ == email:
                resultado = True
                break

    finally:
        # Fecha o cursor e a conexão com o banco de dados
        cursor.close()
        conexao.close()

    return resultado

def cadastrar_usuario():
    # Solicita ao usuário que informe o nome, o endereço de e-mail e a senha dele
    nome = input('Digite seu nome: ')
    email = input('Digite seu endereço de e-mail: ')
    senha = criptografar(input('Digite sua senha: ')).decode('utf-8')

    try:
        # Tenta criar um tabela para armazenar os dados do usuário no banco de dados
        criar_tabela()

        # Verifica se o usuário já está cadastrado no sistema
        if consultar_tabela(email):
            print('O usuário já está cadastrado no sistema')

        else:
            # Insere os dados fornecidos na tabela dos usuários
            inserir_na_tabela(nome, email, senha)
    except:
        # Caso ocorra algum erro no cadastramento, apresenta uma mensagem de erro
        print('Ocorreu um erro no cadastro')

def opcoes(entrada):
    # Cria um dicionário que associa cada opção do menu a uma função
    funcoes = {1: acessar_sistema, 2: cadastrar_usuario}

    try:
        # Tenta executar a função correspondente à entrada fornecida pelo usuário
        funcoes[entrada]()
    except KeyError:
        print('Opção inválida')

def menu():
    # Apresenta as opções disponível para o usuário na tela
    print('1 - Acessar o sistema\n2 - Cadastrar novo usuário')

    try:
        # Solicita ao usuário que informe o número da opção desejada
        entrada = int(input('Digite o número da opção desejada: '))
        opcoes(entrada)
    except ValueError:
        print('Erro de tipo de valor')

if __name__ == '__main__':
    menu()
