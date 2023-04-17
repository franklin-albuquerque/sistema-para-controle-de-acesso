from ast import literal_eval
from bcrypt import hashpw, gensalt
from os import path

def acessar_sistema():
    email = input('Digite seu endereço de e-mail: ')
    senha = input('Digite sua senha: ')

    try:
        with open('banco_de_dados.db', 'r') as arquivo:
            for linha in arquivo:
                usuario = literal_eval(linha)
                for email_, senha_ in usuario.items():
                    if email_ == email:
                        if senha_ == hashpw(senha.encode('utf-8'), senha_):
                            print('Acesso autorizado')
                        else:
                            print('Acesso negado')
                        return
            else:
                print('Não há nenhuma conta associada ao endereço de e-mail')

    except FileNotFoundError:
        print('Banco de dados não encontrado')

def criptografar(senha):
    return hashpw(senha.encode('utf-8'), gensalt(13))

def cadastrar_usuario():
    email = input('Digite seu endereço de e-mail: ')
    senha = criptografar(input('Digite sua senha: '))

    usuario = {email: senha}

    if path.exists('banco_de_dados.db'):
        with open('banco_de_dados.db', 'r') as arquivo:
            for linha in arquivo:
                usuario_banco = literal_eval(linha)

                for email_, _ in usuario_banco.items():
                    if email_ == email:
                        print('Já existe uma conta associada ao e-mail informado')
                        return
            else:
                with open('banco_de_dados.db', 'a+') as arquivo:
                    arquivo.write(f'{usuario}\n')
                print('Cadastrado com sucesso', end='\n')
                return
    else:
        with open('banco_de_dados.db', 'a+') as arquivo:
            arquivo.write(f'{usuario}\n')
        print('Cadastrado com sucesso', end='\n')

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
