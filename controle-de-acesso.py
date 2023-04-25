from ast import literal_eval
from bcrypt import checkpw, hashpw, gensalt
from os import path
from psycopg2 import connect, DatabaseError
from dotenv import dotenv_values

def criptografar(senha):
    return hashpw(senha.encode('utf-8'), gensalt(13))

def criar_bd():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL
    )'''

    cursor.execute(sql)
    conexao.commit()
    cursor.close()
    conexao.close()

def conectar_bd():
    conexao = None

    if path.exists('.env'):
        config = dotenv_values('.env', encoding='utf-16')
        conexao = connect(host=config['host'],
                          database=config['banco_de_dados'],
                          user=config['usuario'],
                          password=config['senha'])
    else:
        print('Não foi possível conectar ao banco de dados')

    return conexao

def inserir_bd(nome, email, senha):
    conexao = conectar_bd()
    cursor = conexao.cursor()

    try:
        sql = f"INSERT INTO usuarios (nome, email, senha) VALUES ('{nome}', '{email}', '{senha}')"
        cursor.execute(sql)
        conexao.commit()
        print('Usuário registrado com sucesso')
    except (Exception, DatabaseError) as erro:
        print(f'Erro: {erro}')
        conexao.rollback()
    finally:
        cursor.close()
        conexao.close()

def acessar_sistema():
    email = input('Digite seu endereço de e-mail: ')
    senha = input('Digite sua senha: ')

    conexao = conectar_bd()
    cursor = conexao.cursor()

    try:
        consulta = "SELECT email, senha FROM usuarios"
        cursor.execute(consulta)
        linhas = cursor.fetchall()

        for linha in linhas:
            email_ = linha[0]
            senha_ = linha[1]

            if email_ == email:
                if checkpw(senha.encode('utf-8'), senha_.encode('utf-8')):
                    print('Acesso autorizado')
                else:
                    print('Senha incorreta')
                break
        else:
            print('Seu endereço de e-mail não está registrado no sistema')
    except:
        print('Não foi possível acessar o banco de dados')
    finally:
        cursor.close()
        conexao.close()

def consultar_bd(email):
    resultado = None

    conexao = conectar_bd()
    cursor = conexao.cursor()

    try:
        consulta = "SELECT email FROM usuarios"
        cursor.execute(consulta)
        linhas = cursor.fetchall()

        for linha in linhas:
            email_ = linha[0]

            if email_ == email:
                resultado = True
                break
    finally:
        cursor.close()
        conexao.close()

    return resultado

def cadastrar_usuario():
    nome = input('Digite seu nome: ')
    email = input('Digite seu endereço de e-mail: ')
    senha = criptografar(input('Digite sua senha: ')).decode('utf-8')

    try:
        criar_bd()

        if consultar_bd(email):
            print('O usuário já está cadastrado no sistema')
        else:
            inserir_bd(nome, email, senha)
    except:
        print('Erro no cadastramento')

def opcoes(entrada):
    if entrada == 1:
        cadastrar_usuario()
    elif entrada == 2:
        acessar_sistema()
    else:
        print('Opção inválida')

def main():
    print('1 - Cadastrar novo usuário\n2 - Acessar o sistema')

    try:
        entrada = int(input('Digite o número da opção desejada: '))
        opcoes(entrada)
    except ValueError:
        print('Erro de tipo de valor')

if __name__ == '__main__':
    main()
