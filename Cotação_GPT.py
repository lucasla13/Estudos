import tkinter as tk  # Importa a biblioteca tkinter para a criação da interface gráfica
from tkinter import messagebox  # Importa o módulo de caixas de mensagem do tkinter
import openpyxl  # Biblioteca para ler e manipular arquivos Excel
import requests  # Biblioteca para fazer requisições HTTP (utilizada para interagir com a API do ChatGPT)
import json  # Biblioteca para manipular dados JSON

# Função que realiza a consulta à API do ChatGPT
def query_chatgpt(prompt):
    # Cabeçalhos para autenticação na API do OpenAI (substitua pelo seu próprio token de autenticação)
    headers = {
        "Authorization": "KEY"
    }
    
    # Dados enviados para a API: inclui o modelo GPT e o prompt de consulta
    data = {
        "model": "gpt-3.5-turbo",  # Especifica o modelo da IA (GPT-3.5, pode ser alterado para o modelo desejado)
        "messages": [{"role": "user", "content": prompt}],  # Passa o prompt como mensagem do usuário
    }
    
    url = "https://api.openai.com/v1/chat/completions"  # URL da API do ChatGPT
    
    try:
        # Envia uma requisição POST para a API com os dados e cabeçalhos definidos
        response = requests.post(url, headers=headers, json=data)
        
        # Verifica se a resposta foi bem-sucedida (código 200)
        if response.status_code != 200:
            print(f"Erro na API: {response.status_code}")  # Exibe o código de erro se a requisição falhar
            print(response.text)  # Exibe o texto da resposta de erro
            return None
        
        # Converte a resposta para um formato JSON
        response_json = response.json()
        print(response_json)  # Exibe a resposta completa para depuração
        
        # Retorna o conteúdo da resposta (preço de cada fornecedor)
        return response_json['choices'][0]['message']['content'].strip()
    
    # Captura erros caso falhe ao processar a resposta JSON
    except KeyError as e:
        print(f"Erro na resposta: {e}")
        print(f"Resposta completa: {response.json()}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")  # Captura qualquer outro erro não esperado
        return None

# Função chamada ao pressionar o botão "Executar" da interface gráfica
def execute():
    # Obtém os valores inseridos nos campos de entrada da interface gráfica
    produto = produto_entry.get()
    quantidade = quantidade_entry.get()
    
    # Valida se ambos os campos foram preenchidos
    if not produto or not quantidade:
        messagebox.showerror("Erro", "Por favor, preencha ambos os campos de produto e quantidade.")
        return
    
    # Valida se a quantidade inserida é um número inteiro
    try:
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.")
        return
    
    try:
        # Abre o arquivo Excel com a lista de fornecedores
        wb = openpyxl.load_workbook(r"C:\Users\vendas\OPTEC CONSULT\FILE SERVER - Documentos\Comercial\15 - FUNÇÕES\BackOffice\Python\Projeto\CIA\fornecedores.xlsx")
        sheet = wb.active  # Acessa a planilha ativa do arquivo
        fornecedores = [cell.value for cell in sheet['A'] if cell.value]  # Lê as URLs dos fornecedores na coluna A
        
        # Se não houver fornecedores no arquivo, exibe um erro
        if not fornecedores:
            messagebox.showerror("Erro", "Nenhum fornecedor encontrado no arquivo.")
            return

        # Cria o prompt que será enviado ao ChatGPT, pedindo para cotar o preço do produto multiplicado pela quantidade
        prompt = "Por favor, cotar:\n"
        for site in fornecedores:
            prompt += f"o preço de {produto} no {site}, retornando o preço multiplicado pela {quantidade}.\n"
        
        # Adiciona instrução para retornar as 3 melhores ofertas
        prompt += "\nE separar as 3 melhores ofertas."

        # Chama a função query_chatgpt para obter a resposta da IA
        resposta = query_chatgpt(prompt)
        
        # Se a resposta foi recebida com sucesso
        if resposta:
            # Inicializa uma lista para armazenar os resultados extraídos da resposta
            resultados = []
            
            # Divide a resposta em linhas e tenta extrair site e preço de cada linha
            linhas = resposta.split("\n")
            for linha in linhas:
                if linha.strip():  # Ignora linhas vazias
                    partes = linha.split(" - ")  # Divide a linha em "site - preço"
                    if len(partes) == 2:
                        site, preco = partes  # Atribui o site e o preço
                        resultados.append((site.strip(), preco.strip()))  # Adiciona o par site-preço à lista

            # Limita os resultados às 3 melhores ofertas
            melhores_resultados = resultados[:3]

            # Se houver resultados, cria uma tabela para mostrar as ofertas
            if melhores_resultados:
                tabela = "Fornecedor | Preço\n"
                tabela += "----------------------\n"
                for site, preco in melhores_resultados:
                    tabela += f"{site} | {preco}\n"
                
                # Chama a função para gerar o PDF com a tabela
                gerar_pdf(tabela)
                messagebox.showinfo("Sucesso", "Tabela gerada com sucesso!")  # Informa que a tabela foi gerada com sucesso
            else:
                messagebox.showerror("Erro", "Não foi possível obter as melhores ofertas.")
        else:
            messagebox.showerror("Erro", "Não foi possível obter preços para o produto.")

    # Captura erros inesperados durante a execução do processo
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função para gerar o PDF com a tabela de cotações
def gerar_pdf(tabela):
    from fpdf import FPDF  # Importa a biblioteca FPDF para criar o PDF

    # Cria uma nova instância do objeto FPDF (criação do PDF)
    pdf = FPDF()
    pdf.add_page()  # Adiciona uma página ao PDF
    
    # Adiciona um título no PDF
    pdf.set_font("Arial", size=16, style='B')  # Define a fonte e o tamanho
    pdf.cell(200, 10, txt="Tabela de Cotações", ln=True, align='C')  # Título centralizado
    
    # Adiciona o conteúdo da tabela
    pdf.ln(10)  # Adiciona uma linha em branco
    pdf.set_font("Arial", size=12)  # Define a fonte para o corpo do texto
    pdf.multi_cell(0, 10, tabela)  # Adiciona o texto da tabela (com quebra de linha automática)
    
    # Salva o PDF no caminho especificado
    pdf_output_path = r"C:\Users\vendas\OPTEC CONSULT\FILE SERVER - Documentos\Comercial\15 - FUNÇÕES\BackOffice\Python\Projeto\CIA\tabela_cotacoes.pdf"
    pdf.output(pdf_output_path)  # Salva o PDF no arquivo
    print(f"PDF gerado em: {pdf_output_path}")  # Exibe o caminho onde o PDF foi salvo

# Configuração da interface gráfica (Tkinter)
root = tk.Tk()  # Cria a janela principal
root.title("Cotação por IA")  # Define o título da janela

# Criação de widgets (elementos da interface gráfica)
produto_label = tk.Label(root, text="Produto:")  # Label para o campo de produto
produto_label.pack()  # Adiciona o label à interface
produto_entry = tk.Entry(root)  # Campo de entrada para o produto
produto_entry.pack()  # Adiciona o campo de entrada à interface

quantidade_label = tk.Label(root, text="Quantidade:")  # Label para o campo de quantidade
quantidade_label.pack()  # Adiciona o label à interface
quantidade_entry = tk.Entry(root)  # Campo de entrada para a quantidade
quantidade_entry.pack()  # Adiciona o campo de entrada à interface

# Criação dos botões
cancelar_button = tk.Button(root, text="Cancelar", command=root.quit)  # Botão para cancelar
cancelar_button.pack()  # Adiciona o botão à interface

executar_button = tk.Button(root, text="Executar", command=execute)  # Botão para executar a cotação
executar_button.pack()  # Adiciona o botão à interface

# Inicia o loop da interface gráfica (exibe a janela)
root.mainloop()