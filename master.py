import webbrowser
import re
from tkinter import *
import requests
from bs4 import BeautifulSoup

def validarCpf(cpf):
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    digit1 = digit2 = 0 # variaveis auxiliaries que receberão o digito valido
    if len(cpf_limpo) != 11 or not cpf_limpo.isdigit(): # se array tem 11 digitos numericos
        return False # retorna invalido
    
    # verificando o primeiro digito
    for i in range(9): # laço que percorre a array multiplicando cada digito pela sequencia decrescente de 10 à 2 e somando o resultado
        digit1 = int(cpf_limpo[i]) * (10 - i) + digit1
    digit1 = digit1 % 11
    if digit1 < 2:
        digit1 = 0
    else:
        digit1 = abs(digit1 - 11) # retorna o valor absoluto, evitando numeros negativos
    if digit1 != int(cpf_limpo[9]):
        return False # retorna invalido
    
    # verificando o segundo digito
    for i in range(10): # laço que percorre a array multiplicando cada digito pela sequencia decrescente de 11 à 2 e somando o resultado
        digit2 = int(cpf_limpo[i]) * (11 - i) + digit2
    digit2 = digit2 % 11
    if digit2 < 2:
        digit2 = 0
    else:
        digit2 = abs(digit2 - 11) # retorna o valor absoluto, evitando numeros negativos
    if digit2 != int(cpf_limpo[10]):
        return False # retorna invalido
    
    return True # passou em todas as validações
    
def validarEmail(email):
    return bool(re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def validarNome(nome):
    return bool(re.fullmatch(r'^[A-Za-zÀ-ÖØ-öø-ÿ]+(?: [A-Za-zÀ-ÖØ-öø-ÿ]+)*$', nome))

def validarTel(tel):
    numero = ''.join(filter(str.isdigit, tel))
    if len(numero) > 11 or len(numero) < 10 or not numero.isdigit(): # se array tem de 10 a 11 digitos numericos
        return False # retorna invalido
    return True

def verificar():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    email = entry_email.get()
    tel = entry_tel.get()

    if validarNome(nome):
        label_val_nome["image"] = certo
    else:
        label_val_nome["image"] = errado

    if validarCpf(cpf):
        label_val_cpf["image"] = certo
    else:
        label_val_cpf["image"] = errado

    if validarEmail(email):
        label_val_email["image"] = certo
    else:
        label_val_email["image"] = errado

    if validarTel(tel):
        label_val_tel["image"] = certo
    else:
        label_val_tel["image"] = errado

    entry_nome.delete(0,END)
    entry_cpf.delete(0,END)
    entry_email.delete(0,END)
    entry_tel.delete(0,END)

def buscar():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    link = "https://www.magazineluiza.com.br/busca/"
    procura = entry_pesquisa.get()
    linkFormatado = link+procura
    requisicao = requests.get(linkFormatado, headers=headers)

    site = BeautifulSoup(requisicao.text, "html.parser")
    produto = site.select('h2[data-testid="product-title"]')
    link2 = site.select('a[data-testid="product-card-container"]')
    preco = site.select('p[data-testid="installment"]')

    menorValor = float(10000)
    indice = 0
    for i, elemento in enumerate(preco):
        precoTexto = elemento.get_text()
        match = re.search(r"R\$\s*([\d,.]+)", precoTexto)
        if match:
            precoUnico = float(match.group(1).replace('.', '').replace(',', '.'))
            if precoUnico < menorValor:
                menorValor = precoUnico
                indice = i
        else:
            print("ERROR 1")

    label_nome_produto["text"] = produto[indice].get_text()
    label_link_produto["text"] = f"magazineluiza.com.br{link2[indice]["href"]}"
    label_preco_produto["text"] = f"R$ {menorValor:.2f}"

def abriLink(event):
    url = label_link_produto.cget("text")
    webbrowser.open(url)

janela = Tk()
janela.title("Webscraping Cost")
janela.geometry("500x600")
janela.config(bg="#cccccc")
janela.iconphoto(False, PhotoImage(file="logo.png"))
janela.resizable(width=False, height=False)

certo = PhotoImage(file="right.png")
errado = PhotoImage(file="wrong.png")

label_saud = Label(janela, width=100, height=2, text="BEM VINDO", font=("Arial 18 bold"), bg="#ffac12")
label_saud.pack()

label_nome = Label(janela, width=10, height=1, text="Nome: ", font=("Arial 12"))
label_nome.place(x=5, y=70)
entry_nome = Entry(janela, width=50, font=("Arial 10"))
entry_nome.place(x=110, y=72)
label_val_nome = Label(janela, width=20, height=20, image=certo, bg="#cccccc")
label_val_nome.place(x=470, y=70)

label_cpf = Label(janela, width=10, height=1, text="CPF: ", font=("Arial 12"))
label_cpf.place(x=5, y=100)
entry_cpf = Entry(janela, width=50, font=("Arial 10"))
entry_cpf.place(x=110, y=102)
label_val_cpf = Label(janela, width=20, height=20, image=certo, bg="#cccccc")
label_val_cpf.place(x=470, y=100)

label_email = Label(janela, width=10, height=1, text="Email: ", font=("Arial 12"))
label_email.place(x=5, y=130)
entry_email = Entry(janela, width=50, font=("Arial 10"))
entry_email.place(x=110, y=132)
label_val_email = Label(janela, width=20, height=20, image=certo, bg="#cccccc")
label_val_email.place(x=470, y=130)

label_tel = Label(janela, width=10, height=1, text="Telefone:", font=("Arial 12"))
label_tel.place(x=5, y=160)
entry_tel = Entry(janela, width=50, font=("Arial 10"))
entry_tel.place(x=110, y=162)
label_val_tel = Label(janela, width=20, height=20, image=certo, bg="#cccccc")
label_val_tel.place(x=470, y=160)

botao = Button(janela, command=verificar, width=7, height=1, text="Verificar", font=("Arial 9"), relief="raised")
botao.place(x=5, y=190)

label_pesquisa = Label(janela, width=10, height=1, text="Buscar:", font=("Arial 12"))
label_pesquisa.place(x=5, y=250)
entry_pesquisa = Entry(janela, width=50, font=("Arial 10"))
entry_pesquisa.insert(0, "Teclado Yamaha PSR-E473")
entry_pesquisa.config(state="readonly")
entry_pesquisa.place(x=110, y=252)

botao_buscar = Button(janela, command=buscar, width=12, height=1, text="Procurar Custo", font=("Arial 9"), relief="raised")
botao_buscar.place(x=5, y=280)

label_nome_produto = Label(janela, width=60, text="",  wraplength=450, font=("Arial 10"))
label_nome_produto.place(x=5, y=310)
label_preco_produto = Label(janela, width=60, text="",  wraplength=450, font=("Arial 10"))
label_preco_produto.place(x=5, y=350)
label_link_produto = Label(janela, width=60, text="", fg="blue", cursor="hand2", wraplength=450, font=("Arial 10"))
label_link_produto.place(x=5, y=390)
label_link_produto.bind("<Button-1>", abriLink)

label_val_cpf.image = certo
janela.mainloop()