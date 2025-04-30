# -- IMPORTAÇÕES --
import os
import statistics as stats
import time
import csv

# -- ADICIONAR PESSOA --
def coletar_pessoa(dados: dict[str, dict]) -> dict[str, dict]:
    nome = input('Nome: ') # Input recebe uma entrada do usuario em string
    idade = input('Idade: ')
    telefone = input('Telefone: ')
    email = input('E-mail: ')
    cidade = input('Cidade (opcional): ')

    # Validação do e-mail
    if "@" not in email: #Uso de 'not in' para validar se é um dominio de e-mail, ou seja, possui '@'
        print("Insira um e-mail válido")
        return dados

    # Validação da idade
    try:
        idade = int(idade) #Atualiza a idade para um valor inteiro
    except ValueError: #Retorna uma ação, caso a ação não seja executada corretamente
        print('Idade inválida')
        return dados #Retorna o parametro a ser utilizado em outras def

    # Montar o dicionário com os dados válidos que podem ser referenciados em outras def
    dados[nome] = {
        "idade": idade,
        "telefone": telefone,
        "email": email,
        "cidade": cidade or None  # Aceita a ausência de entrada para cidade
    }

    return dados

# -- BUSCAR PESSOA --
def buscar_pessoa(dados: dict) -> dict:
    nome = input("Informe o nome que deseja buscar: ")

    if nome in dados: # Se o 'nome' estiver no parametro 'dados', executa:
        print(f"Os dados de {nome} são: {dados[nome]}") # O parametro 'dados' retorna o dict da chave 'nome'
    else:
        print("Nome não encontrado")
    return dados

# -- ATUALIZAR OS DADOS --
def atualizar_pessoa(dados: dict) -> dict:
    nome = input("Informe o nome que deseja atualizar: ")

    if nome in dados:
        print("\nQual dado deseja alterar?\n" \
              "1. Idade\n" \
              "2. Telefone\n" \
              "3. E-mail\n" \
              "4. Cidade")
        opcao = input('Escolha uma opção: ')
        if opcao == "1": # Se a variavel 'opcao' for igual a string 1, executa:
            idade = input("Nova idade: ")
            try:
                idade = int(idade)
                dados[nome]["idade"] = idade # Atualiza a variavel 'idade' no dict do 'nome' inserido, com a nova variavel 'idade'
            except ValueError:
                print("Idade inválida")
        elif opcao == "2":
            telefone = input("Novo telefone: ")
            dados[nome]["telefone"] = telefone
        elif opcao == "3":
            email = input("Novo e-mail: ")
            dados[nome]["email"] = email
        elif opcao == "4":
            cidade = input("Nova cidade: ")
            dados[nome]["cidade"] = cidade or None
        else:
            print("Opção inválida")
    else:
        print("Nome não encontrado")

    return dados

# -- REMOVER PESSOA --
def remover_pessoa(dados: dict) -> dict:
    nome = input("Informe o nome que deseja remover: ")

    if nome in dados:
        del dados[nome] # Executa a ação de deletar o dict da chave 'nome' inserida
        print(f"{nome} removido com sucesso")
    else:
        print("Nome não encontrado")
    return dados

# -- ORDENAR POR IDADE --
def ordenar_idade(dados: dict) -> dict:
    dados_ordenado = dict(sorted(dados.items(), key=lambda item: item[1]["idade"])) # A variavel retorna uma lista de tuplas 'chave : valor', ordenando de maneira ascendente.
    # lambda item: item[1]["idade"] significa item é cada tupla, item[1] é o valor, ou seja, o dicionario. Sendo que ordenamento esta ocorrendo com base na idade ["idade"].
    # dict no começo faz a lista de tuplas retornar como um dicionario ao final.
    print(dados_ordenado)
    return dados_ordenado

# -- FILTRO DE IDADE --
def filtro_idade(dados: dict[str, dict]) -> dict[str, dict]:
    try:
        idade_max = int(input("Informe a idade máxima: ")) # Recebe o input já convertendo para inteiro.
        idade_min = int(input("Informe a idade mínima: "))
    except ValueError:
        print("Idade inválida")
        return dados

    intervalo = range(idade_min, idade_max + 1) # Cria uma faixa de número inteiros partindo do incio até um antes do fim, por isso o +1, englopbando o valor final no intervalo.

    dados_filtrados = {nome: info for nome, info in dados.items() if info["idade"] in intervalo} # Filtra os dados pegando só quem tem idade dentro do intervalo, criando um novo dicionário só com esses casos.
    # A chave 'nome' retorna uma 'info', para cada 'nome, info' na lista de tuplas 'dados.items'. Sendo info = a 'idade' e estando presente na variavel intervalo 'range'.

    print(dados_filtrados)
    return dados_filtrados

# -- CÁLCULOS --
def estatisticas(dados: dict[str, dict]):
    idades = [pessoa["idade"] for pessoa in dados.values()] # 'Pessoa' esta como um nome de variavel apenas para o contexto dessa def
    # Define uma nova variavel que ira apenas retornar a 'idade', chamando de 'pessoa' cada um desses no dicionario.

    if not idades:
        print("Nenhuma idade cadastrada.")
        return {}

    def calcular_media() -> float:
        return stats.mean(idades) # Chama o modulo stats para executar a média

    def calcular_mediana() -> float:
        return stats.median(idades) # Chama o modulo stats para executar a mediana

    def mais_velhos() -> list[str]:
        return [nome for nome, info in dados.items() if info["idade"] >= 18] 
    # Para cada par nome e info dentro do dicionário dados (ou seja, para cada pessoa com suas informações), verifique se a idade dentro de info é maior ou igual a 18. Se for, coloque esse nome na lista final que será retornada.

    def mais_jovens() -> list[str]:
        return [nome for nome, info in dados.items() if info["idade"] < 18]

    return {
        'media': calcular_media(),
        'mediana': calcular_mediana(),
        'mais_velho': mais_velhos(),
        'mais_jovens': mais_jovens()
    }

# -- MENU --
def menu(dados):
    print("\n-- MENU --")
    print(f"Total de pessoas cadastradas: {len(dados)}")
    print("1 - Adicionar pessoa")
    print("2 - Mostrar estatísticas")
    print("3 - Buscar pessoa")
    print("4 - Atualizar dados")
    print("5 - Remover pessoa")
    print("6 - Listar ordenado por idade")
    print("7 - Filtrar por faixa etária")
    print("8 - Sair")

    opcao = input('Escolha uma opção: ')
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa o terminal
    return opcao

# -- PRINCIPAL --
def main(): # Executa as def
    dados = carregar_csv("dados.csv")

    while True:
        opcao = menu(dados)
        if opcao == "1":
            dados = coletar_pessoa(dados)

        elif opcao == "2":
            if dados:
                resultados = estatisticas(dados)
                if resultados:
                    print("\n -- ESTATÍSTICAS --")
                    print(f"Média: {resultados['media']:.2f}")
                    print(f"Mediana: {resultados['mediana']}")
                    print(f"Mais velho(s): {resultados['mais_velho']}")
                    print(f"Mais jovem(s): {resultados['mais_jovens']}")
            else:
                print("Nenhum dado disponível ainda.")

        elif opcao == "3":
            buscar_pessoa(dados)

        elif opcao == "4":
            atualizar_pessoa(dados)

        elif opcao == "5":
            remover_pessoa(dados)

        elif opcao == "6":
            ordenar_idade(dados)

        elif opcao == "7":
            filtro_idade(dados)

        elif opcao == "8":
            salvar_csv(dados)
            print("Finalizando programa...")
            time.sleep(2) # Tempo de espera em segundos
            os.system('cls' if os.name == 'nt' else 'clear')
            break

        else:
            print("Opção inválida")

# -- EXPORTAR CSV --
def salvar_csv(dados: dict, nome_arquivo: str = "dados.csv"):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo: # Abre ou cria um arquivo com o nome 'nome_arquivo'.
        #mode= 'w' abre o arquivo no modo escrita.
        #newline='' evita que linhas em branco extras apareçam ao salvar CSV.
        #encoding='utf-8' define a codificação do texto,garantindo a compatibilidade com acentos e caracteres especiais.
        #as arquivo o arquivo aberto será acessado por essa variável (arquivo) dentro do bloco with.
        writer = csv.writer(arquivo) # csv é o modulo que ajuda na escrita e leitura de csv
        writer.writerow(["Nome", "Idade", "Telefone", "E-mail", "Cidade"])
        for nome, info in dados.items():
            writer.writerow([nome, info["idade"], info["telefone"], info["email"], info["cidade"] or ""])
    print(f"Dados salvos em {nome_arquivo}")

# -- CARREGAR CSV --
def carregar_csv(nome_arquivo: str) -> dict:
    dados = {} #Cria um dicionario vazio para ser preenchido com os dados lidos no arquivo CSV
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, mode='r', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo)
            next(reader)
            for row in reader:
                nome, idade, telefone, email, cidade = row
                dados[nome] = {
                    "idade": int(idade),
                    "telefone": telefone,
                    "email": email,
                    "cidade": cidade or None
                }
    else:
        print(f"Arquivo {nome_arquivo} não encontrado. Será criado ao salvar.")
    return dados

# -- EXECUÇÃO --
if __name__ == "__main__":
    main()