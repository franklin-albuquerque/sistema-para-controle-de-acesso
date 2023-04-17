from ast import literal_eval
from bcrypt import hashpw, gensalt

def acessar_sistema():
    email_ = input('Digite seu endereço de e-mail: ')
    senha_ = input('Digite sua senha: ')

    try:
        with open('banco_de_dados.db', 'r') as arquivo:
            for linha in arquivo:
                usuario = literal_eval(linha)

                for email, senha in usuario.items():
                    if email == email_ and senha == hashpw(senha_.encode('utf-8'), senha):
                        print('Acesso autorizado')
                    else:
                        print('Acesso negado')

    except FileNotFoundError:
        print('Banco de dados não encontrado')

def criptografar(senha):
    return hashpw(senha.encode('utf-8'), gensalt(13))

def cadastrar_usuario():
    email = input('Digite seu endereço de e-mail: ')
    senha = criptografar(input('Digite sua senha: '))

    usuario = {email: senha}
    
    with open('banco_de_dados.db', 'w') as arquivo:
        arquivo.write(str(usuario))
    print('Cadastrado com sucesso', end='\n')

def main():
    print('1 - Cadastrar usuário\n2 - Acessar sistema')
    opcao = int(input('Informe a opção desejada: '))

    if opcao == 1:
        cadastrar_usuario()
    elif opcao == 2:
        acessar_sistema()
    else:
        print('Opção invalida')

if __name__ == '__main__':
    main()
