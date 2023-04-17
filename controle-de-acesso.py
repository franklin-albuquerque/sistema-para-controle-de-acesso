from bcrypt import hashpw, gensalt

def verificar_senha():
    senha = input('Digite sua senha: ')

    with open('banco_de_dados.db', 'r') as arquivo:
        hash = arquivo.read().encode('utf-8')

    if hashpw(senha.encode('utf-8'), hash) == hash:
        print('Acesso autorizado')
    else:
        print('Acesso negado')

def criptografar():
    senha = input('Digite sua senha: ')
    resultado = hashpw(senha.encode('utf-8'), gensalt(13))

    print("Cadastrando no sistema...")
    with open('banco_de_dados.db', 'w') as arquivo:
        arquivo.write(resultado.decode('utf-8'))
    print('Registrado com sucesso', end='\n')

    return resultado

def main():
    print('''1 - Registrar senha\n2 - Verificar senha''')
    opcao = int(input('Informe a opção desejada: '))

    if opcao == 1:
        criptografar()
    elif opcao == 2:
        verificar_senha()
    else:
        print('Opção invalida')

if __name__ == '__main__':
    main()
