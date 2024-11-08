import re # para validações regex
from tkinter import *

def validarCpf(cpf):
    digit1 = digit2 = 0 # variaveis auxiliaries que receberão o digito valido
    if len(cpf) != 11 or not cpf.isdigit(): # se array tem 11 digitos numericos
        return False # retorna invalido
    
    # verificando o primeiro digito
    for i in range(9): # laço que percorre a array multiplicando cada digito pela sequencia decrescente de 10 à 2 e somando o resultado
        digit1 = int(cpf[i]) * (10 - i) + digit1
    digit1 = digit1 % 11
    if digit1 < 2:
        digit1 = 0
    else:
        digit1 = abs(digit1 - 11) # retorna o valor absoluto, evitando numeros negativos
    if digit1 != int(cpf[9]):
        return False # retorna invalido
    
    # verificando o segundo digito
    for i in range(10): # laço que percorre a array multiplicando cada digito pela sequencia decrescente de 11 à 2 e somando o resultado
        digit2 = int(cpf[i]) * (11 - i) + digit2
    digit2 = digit2 % 11
    if digit2 < 2:
        digit2 = 0
    else:
        digit2 = abs(digit2 - 11) # retorna o valor absoluto, evitando numeros negativos
    if digit2 != int(cpf[10]):
        return False # retorna invalido
    
    return True # passou em todas as validações
    
def validarEmail(email):
    return bool(re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def validarNome(nome):
    return bool(re.fullmatch(r'^[A-Za-zÀ-ÖØ-öø-ÿ]+(?: [A-Za-zÀ-ÖØ-öø-ÿ]+)*$', nome))

def verificar():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    email = entry_email.get()

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

    entry_nome.delete(0,END)
    entry_cpf.delete(0,END)
    entry_email.delete(0,END)

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
label_val_nome = Label(janela, width=20, height=20, image=certo)
label_val_nome.place(x=470, y=70)

label_cpf = Label(janela, width=10, height=1, text="CPF: ", font=("Arial 12"))
label_cpf.place(x=5, y=100)
entry_cpf = Entry(janela, width=50, font=("Arial 10"))
entry_cpf.place(x=110, y=102)
label_val_cpf = Label(janela, width=20, height=20, image=certo)
label_val_cpf.place(x=470, y=100)

label_email = Label(janela, width=10, height=1, text="Email: ", font=("Arial 12"))
label_email.place(x=5, y=130)
entry_email = Entry(janela, width=50, font=("Arial 10"))
entry_email.place(x=110, y=132)
label_val_email = Label(janela, width=20, height=20, image=certo)
label_val_email.place(x=470, y=130)

botao = Button(janela, command=verificar, width=7, height=1, text="Verificar", font=("Arial 9"), relief="raised")
botao.place(x=5, y=160)

label_val_cpf.image = certo
janela.mainloop()