import os

# Arquivos txt:
ARQ_USUARIOS  = "usuarios.txt"
ARQ_FILMES    = "filmes.txt"
ARQ_CURTIDAS  = "curtidas.txt"
ARQ_FAVORITOS = "favoritos.txt"


# Dicionário de usuários:
USUARIOS = {
    "ID"   : [],
    "NOME" : [],
    "SENHA": []
}


# Criar arquivos caso não existam:
def criar_arquivos():

    if not os.path.exists(ARQ_USUARIOS):
        open(ARQ_USUARIOS,  "w").close()

    if not os.path.exists(ARQ_CURTIDAS):
        open(ARQ_CURTIDAS,  "w").close()

    if not os.path.exists(ARQ_FAVORITOS):
        open(ARQ_FAVORITOS, "w").close()


# Carrega os usuários do arquivo para o dicionário na memória:
def carregar_usuarios():

    arquivo = open(ARQ_USUARIOS, "r")

    while True:
        id_usuario = arquivo.readline()
        if id_usuario == "":
            break
        Nome  = arquivo.readline()
        Senha = arquivo.readline()

        USUARIOS["ID"].append(id_usuario[:-1])
        USUARIOS["NOME"].append(Nome[:-1])
        USUARIOS["SENHA"].append(Senha[:-1])

    arquivo.close()


# Salva o dicionário de usuários no arquivo:
def salvar_usuarios():

    arquivo = open(ARQ_USUARIOS, "w")

    i = 0
    while i < len(USUARIOS["ID"]):
        arquivo.write(USUARIOS["ID"][i]    + "\n")
        arquivo.write(USUARIOS["NOME"][i]  + "\n")
        arquivo.write(USUARIOS["SENHA"][i] + "\n")
        i += 1

    arquivo.close()


# Cadastro de novo usuário:
def cadastrar():

    print("\n |CADASTRO|")

    Nome  = input("|Digite um nome de usuário: ").upper()
    Senha = input("|Crie uma senha: ")

    # Verifica se o usuário já existe
    i = 0
    while i < len(USUARIOS["NOME"]):
        if USUARIOS["NOME"][i] == Nome:
            print("|Este usuário já existe!|")
            return
        i += 1

    novo_id = str(len(USUARIOS["ID"]) + 1)

    USUARIOS["ID"].append(novo_id)
    USUARIOS["NOME"].append(Nome)
    USUARIOS["SENHA"].append(Senha)

    salvar_usuarios()

    print("|Usuário cadastrado com sucesso! Bem-vindo(a) ao FEI TV ;)|")


# Login:
def login():

    print("\n |LOGIN|")

    Nome  = input("|Digite seu usuário: ").upper()
    Senha = input("|Digite sua senha: ")

    # Verifica se o usuário e senha correspondem a algum registro
    i = 0
    while i < len(USUARIOS["NOME"]):
        if USUARIOS["NOME"][i] == Nome and USUARIOS["SENHA"][i] == Senha:
            print("|Login realizado com sucesso!!|")
            return Nome
        i += 1

    print("|Usuário ou senha incorretos.|")
    return None


# Conta quantas curtidas um filme tem pelo ID:
def contar_curtidas(id_filme):

    arquivo = open(ARQ_CURTIDAS, "r")

    total = 0
    while True:
        usuario_lido = arquivo.readline()
        if usuario_lido == "":
            break
        id_lido = arquivo.readline()
        if id_lido[:-1] == id_filme:
            total += 1

    arquivo.close()
    return total


# Lista todos os filmes disponíveis:
def listar_filmes():

    print("\n |LISTA DE FILMES|")

    arquivo = open(ARQ_FILMES, "r")

    while True:
        id_filme = arquivo.readline()
        if id_filme == "":
            break
        Titulo   = arquivo.readline()
        Genero   = arquivo.readline()
        Ano      = arquivo.readline()
        curtidas = contar_curtidas(id_filme[:-1])

        print("______________________")
        print(f"|ID: {id_filme[:-1]}")
        print(f"|Título: {Titulo[:-1]}")
        print(f"|Gênero: {Genero[:-1]}")
        print(f"|Ano: {Ano[:-1]}")
        print(f"|Curtidas: {curtidas}")

    arquivo.close()


# Busca o ID de um filme pelo nome exato:
def buscar_id_por_nome(Nome_filme):

    arquivo = open(ARQ_FILMES, "r")

    while True:
        id_filme = arquivo.readline()
        if id_filme == "":
            break
        Titulo = arquivo.readline()
        Genero = arquivo.readline()
        Ano    = arquivo.readline()

        if Titulo[:-1] == Nome_filme:
            arquivo.close()
            return id_filme[:-1]

    arquivo.close()
    return None


# Curtir um filme pelo nome:
def curtir_filme(usuario):

    print("\n |CURTIR FILME|")

    listar_filmes()
    Nome_filme = input("|Digite o nome do filme: ")

    # Busca o ID do filme pelo nome
    id_filme = buscar_id_por_nome(Nome_filme)

    if id_filme == None:
        print("|Filme não encontrado.|")
        return

    # Verifica se o usuário já curtiu esse filme
    arquivo = open(ARQ_CURTIDAS, "r")

    while True:
        usuario_lido = arquivo.readline()
        if usuario_lido == "":
            break
        id_lido = arquivo.readline()
        if usuario_lido[:-1] == usuario and id_lido[:-1] == id_filme:
            arquivo.close()
            print("|Este filme já foi curtido!|")
            return

    arquivo.close()

    # Se não curtiu ainda, adiciona a curtida
    arquivo = open(ARQ_CURTIDAS, "a")
    arquivo.write(usuario  + "\n")
    arquivo.write(id_filme + "\n")
    arquivo.close()

    print("|Filme curtido com sucesso!!|")


# Descurtir um filme pelo nome:
def descurtir_filme(usuario):

    print("\n |DESCURTIR FILME|")

    listar_filmes()
    Nome_filme = input("|Digite o nome do filme: ")

    # Busca o ID do filme pelo nome
    id_filme = buscar_id_por_nome(Nome_filme)

    if id_filme == None:
        print("|Filme não encontrado.|")
        return

    # Lê todas as curtidas e guarda as que não são do filme escolhido
    arquivo = open(ARQ_CURTIDAS, "r")
    usuarios_salvos = []
    ids_salvos      = []
    removido        = False

    while True:
        usuario_lido = arquivo.readline()
        if usuario_lido == "":
            break
        id_lido = arquivo.readline()
        if usuario_lido[:-1] == usuario and id_lido[:-1] == id_filme:
            removido = True
        else:
            usuarios_salvos.append(usuario_lido[:-1])
            ids_salvos.append(id_lido[:-1])

    arquivo.close()

    # Reescreve o arquivo sem a curtida removida
    arquivo = open(ARQ_CURTIDAS, "w")
    i = 0
    while i < len(usuarios_salvos):
        arquivo.write(usuarios_salvos[i] + "\n")
        arquivo.write(ids_salvos[i]      + "\n")
        i += 1
    arquivo.close()

    if removido:
        print("|Curtida removida com sucesso!|")
    else:
        print("|Este filme não foi curtido.|")


# Adicionar um filme aos favoritos pelo nome:
def adicionar_favorito(usuario):

    print("\n |ADICIONAR AOS FAVORITOS|")

    listar_filmes()
    Nome_filme = input("|Digite o nome do filme: ")

    # Busca o ID do filme pelo nome
    id_filme = buscar_id_por_nome(Nome_filme)

    if id_filme == None:
        print("\n |Filme não encontrado.|")
        return

    # Verifica se o filme já está nos favoritos
    arquivo = open(ARQ_FAVORITOS, "r")

    while True:
        usuario_lido = arquivo.readline()
        if usuario_lido == "":
            break
        id_lido = arquivo.readline()
        if usuario_lido[:-1] == usuario and id_lido[:-1] == id_filme:
            arquivo.close()
            print("|Este filme já está nos favoritos!|")
            return

    arquivo.close()

    # Se não está, adiciona
    arquivo = open(ARQ_FAVORITOS, "a")
    arquivo.write(usuario  + "\n")
    arquivo.write(id_filme + "\n")
    arquivo.close()

    print("|Filme adicionado aos favoritos com sucesso!!|")


# Remover um filme dos favoritos pelo nome:
def remover_favorito(usuario):

    print("\n |REMOVER DOS FAVORITOS|")

    listar_filmes()
    Nome_filme = input("|Digite o nome do filme: ")

    # Busca o ID do filme pelo nome
    id_filme = buscar_id_por_nome(Nome_filme)

    if id_filme == None:
        print("|Filme não encontrado.|")
        return

    # Lê todos os favoritos e guarda os que não são do filme escolhido
    arquivo = open(ARQ_FAVORITOS, "r")
    usuarios_salvos = []
    ids_salvos      = []
    removido        = False

    while True:
        usuario_lido = arquivo.readline()
        if usuario_lido == "":
            break
        id_lido = arquivo.readline()
        if usuario_lido[:-1] == usuario and id_lido[:-1] == id_filme:
            removido = True
        else:
            usuarios_salvos.append(usuario_lido[:-1])
            ids_salvos.append(id_lido[:-1])

    arquivo.close()

    # Reescreve o arquivo sem o favorito removido
    arquivo = open(ARQ_FAVORITOS, "w")
    i = 0
    while i < len(usuarios_salvos):
        arquivo.write(usuarios_salvos[i] + "\n")
        arquivo.write(ids_salvos[i]      + "\n")
        i += 1
    arquivo.close()

    if removido:
        print("|Filme removido dos favoritos com sucesso!!|")
    else:
        print("|Este filme não foi encontrado na lista de favoritos. ------|")


# Ver filmes favoritos do usuário:
def ver_favorito(usuario):

    print("\n |MEUS FAVORITOS|")

    # Coleta os IDs dos filmes favoritos do usuário
    arquivo = open(ARQ_FAVORITOS, "r")
    ids_favoritos = []

    while True:
        usuario_lido = arquivo.readline()
        if usuario_lido == "":
            break
        id_lido = arquivo.readline()
        if usuario_lido[:-1] == usuario:
            ids_favoritos.append(id_lido[:-1])

    arquivo.close()

    if len(ids_favoritos) == 0:
        print("|Nenhum favorito encontrado :( |")
        return

    # Abre o arquivo de filmes e exibe apenas os que estão na lista de favoritos
    arquivo = open(ARQ_FILMES, "r")
    while True:
        id_filme = arquivo.readline()
        if id_filme == "":
            break
        Titulo = arquivo.readline()
        Genero = arquivo.readline()
        Ano    = arquivo.readline()

        i = 0
        while i < len(ids_favoritos):
            if ids_favoritos[i] == id_filme[:-1]:
                print("________________________")
                print(f"|ID: {id_filme[:-1]}")
                print(f"|Título: {Titulo[:-1]}")
                print(f"|Gênero: {Genero[:-1]}")
                print(f"|Ano: {Ano[:-1]}")
            i += 1

    arquivo.close()


# Menu do usuário logado:
def menu_usuario(usuario):

    while True:
        print("\n |FEI TV|")
        print(f"|Usuário: {usuario}")
        print("|[1] Listar filmes")
        print("|[2] Curtir filme")
        print("|[3] Descurtir filme")
        print("|[4] Adicionar aos favoritos")
        print("|[5] Remover dos favoritos")
        print("|[6] Ver favoritos")
        print("|[7] Logout")
        opcao = input("|Selecione uma opção de 1 a 7: ")

        if opcao == "1":
            listar_filmes()

        elif opcao == "2":
            curtir_filme(usuario)

        elif opcao == "3":
            descurtir_filme(usuario)

        elif opcao == "4":
            adicionar_favorito(usuario)

        elif opcao == "5":
            remover_favorito(usuario)

        elif opcao == "6":
            ver_favorito(usuario)

        elif opcao == "7":
            print("|Logout realizado, obrigada por usar este programa ;) |")
            break

        else:
            print("|Opção inválida!|")

# Menu principal:
def menu_principal():

    criar_arquivos()
    carregar_usuarios()

    while True:
        print("\n |Bem Vindo(a) ao FEI TV |")
        print("|[1] Cadastrar usuário")
        print("|[2] Login")
        print("|[3] Sair")

        opcao = input("|Selecione uma opção de 1 a 3: ")

        if opcao == "1":
            cadastrar()

        elif opcao == "2":
            usuario = login()
            if usuario != None:
                menu_usuario(usuario)

        elif opcao == "3":
            print("\n |FEI TV encerrado!!|")
            break

        else:
            print("\n |Opção inválida!|")

menu_principal()
