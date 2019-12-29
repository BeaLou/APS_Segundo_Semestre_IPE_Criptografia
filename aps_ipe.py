from random import randrange, getrandbits
from tkinter import *

root = Tk()
root.geometry('1050x640')
root.resizable(0, 0)
root.title("Criptografia RSA - APS segundo semestre v2")

topFrame = Frame(root) 
topFrame.pack(side=TOP)

bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

leftFrame = Frame(root)
leftFrame.pack(side=LEFT)

rightFrame = Frame(root)
rightFrame.pack(side=RIGHT)

lblTitulo = Label(topFrame, text="CRIPTOGRAFIA RSA", foreground="black") #cabeçalho do form
lblTitulo.pack()
lblTitulo.configure(relief="ridge", font="Arial 24", border = 0)

class GeradorNumeroPrimo:
    def __init__(self):
        self.numero_primo = self.gerar_numero_primo()

    def teste_miller_rabin(self,n, k=128):
        """ Testa se o número é primo
            Param:
                n - número testado
                k - número de testes
            return True if n is prime
        """
        if n < 6:  # válida alguns casos
            return [False, False, True, True, False, True][n]
        # Testa se n é par
        if n <= 1 or n % 2 == 0:
            return False
        # encontra r e s
        s = 0
        r = n - 1
        while r & 1 == 0:
            s += 1
            r //= 2
        # executa k testes
        for _ in range(k):
            a = randrange(2, n - 1)
            x = pow(a, r, n)
            if x != 1 and x != n - 1:
                j = 1
                while j < s and x != n - 1:
                    x = pow(x, 2, n)
                    if x == 1:
                        return False
                    j += 1
                if x != n - 1:
                    return False
        return True
    def tentativa_de_numero(self,length):
        """ Gera um número primo inteiro aleatório.
                retorna o número
        """
        # gera bits aleatórios
        self.numero_primo = getrandbits(length)
        # aplica uma mascara para determinar valor 1 para MSB e LSB
        self.numero_primo |= (1 << length - 1) | 1
        return self.numero_primo
    def gerar_numero_primo(self,length=5):
        ''' Cria um número primo testado
            parâmetros: 
                length - tamanho em bits
        '''
        self.numero_primo  = 4
        # Continua enquanto o teste falha
        while not self.teste_miller_rabin(self.numero_primo, 128):
            self.numero_primo  = self.tentativa_de_numero(length)
        return self.numero_primo

#classes estanciadas e métodos chamados
p = GeradorNumeroPrimo() 
numero_p = p.numero_primo
q = GeradorNumeroPrimo()
numero_q = q.numero_primo

#exibindo os numeros publicos
lbl = Label(topFrame,text="-------------------------------------------------------------------", foreground="black") #exibindo o resultado
lbl.pack()
lbl.configure(relief="ridge", font="Arial 16 ", border= 0)

lblPrimoP = Label(topFrame,text="Número primo (P): " + str(numero_p )  , foreground="black") #exibindo o resultado
lblPrimoP.pack()
lblPrimoP.configure(relief="ridge", font="Arial 16 ", border= 0)

lblPrimoQ = Label(topFrame,text="Número primo (Q): " + str(numero_q )  , foreground="black")
lblPrimoQ.pack()
lblPrimoQ.configure(relief="ridge", font="Arial 16 ", border= 0)

lbl2 = Label(topFrame,text="-------------------------------------------------------------------", foreground="black") #exibindo o resultado
lbl2.pack()
lbl2.configure(relief="ridge", font="Arial 16 ", border= 0)

#entrada da mensagem que será criptografada
lblChavePublicaR = Label(leftFrame, text= "Escolha sua chave pública:" , foreground="black")
lblChavePublicaR.pack()
lblChavePublicaR.configure(relief="ridge", font="Arial 16 ", border= 0)

global txtChavePublicaR
txtChavePublicaR = Entry(leftFrame,font="Arial 16")
txtChavePublicaR.pack()

lblMsg = Label(leftFrame, text="Insira a mensagem: ", foreground="black")
lblMsg.pack()
lblMsg.configure(relief="ridge", font="Arial 16 ", border= 0)

global txtMsg
txtMsg = Entry(leftFrame,font="Arial 16")
txtMsg.pack()


lblInter = Label(rightFrame, text="Insira a mensagem a ser interpretada: ", foreground="black")
lblInter.pack()
lblInter.configure(relief="ridge", font="Arial 16 ", border= 0)

global txtInter
txtInter = Entry(rightFrame,font="Arial 16")
txtInter.pack()
#entrada das chaves públicas - input das chaves
    
lblChavePublicaE = Label(leftFrame, text= "Insira a primeira chave pública (E):" , foreground="black")
lblChavePublicaE.pack()
lblChavePublicaE.configure(relief="ridge", font="Arial 16 ", border= 0)

global txtChavePublicaE
txtChavePublicaE = Entry(leftFrame,font="Arial 16")
txtChavePublicaE.pack()

lblChavePublicaN = Label(leftFrame, text="Insira a segunda chave pública (N): ", foreground="black")
lblChavePublicaN.pack()
lblChavePublicaN.configure(relief="ridge", font="Arial 16 ", border= 0)

global txtChavePublicaN
txtChavePublicaN = Entry(leftFrame,font="Arial 16")
txtChavePublicaN.pack()


#entrada das chaves privadas - input das chaves

lblChavePrivadaD = Label(rightFrame, text= "Insira a primeira chave privada (D):" , foreground="black")
lblChavePrivadaD.pack()
lblChavePrivadaD.configure(relief="ridge", font="Arial 16 ", border= 0)

txtChavePrivadaD = Entry(rightFrame,font="Arial 16")
txtChavePrivadaD.pack()

lblChavePrivadaN = Label(rightFrame, text= "Insira a segunda chave privada (N): ", foreground="black")
lblChavePrivadaN.pack()
lblChavePrivadaN.configure(relief="ridge", font="Arial 16 ", border= 0)

txtChavePrivadaN = Entry(rightFrame,font="Arial 16")
txtChavePrivadaN.pack()

class Criptografia(object):
#calculos usados para cifrar e decifrar as mensagens
    def criptografia(self, m, e, n):
        c = (m**e) % n
        return c

    def descriptografia(self, c, d, n):
        m = c**d % n
        return m

    def encripta_mensagem(self):
        s = txtMsg.get()

        # aqui, é validada se as entradas são numericas ou não
        if(str(txtChavePublicaE.get()).isnumeric() and str(txtChavePublicaN.get()).isnumeric()): 
            e = int(txtChavePublicaE.get())
            n = int(txtChavePublicaN.get()) 
            enc = ''.join(chr(self.criptografia(ord(x), e, n)) for x in s)
            print(enc)
            lblEnc["text"] = enc
        else:
            lblEnc["text"] = "Insira apenas números inteiros!!"
        return lblEnc

    def decripta_mensagem(self):
        s = txtInter.get()
        # aqui, é validada se as entradas são numericas ou não
        
        if(str(txtChavePrivadaD.get()).isnumeric() and str(txtChavePrivadaN.get()).isnumeric()):
            d = int(txtChavePrivadaD.get())
            n = int(txtChavePrivadaN.get()) 
            dec = ''.join(chr(self.descriptografia(ord(x), d, n)) for x in s)
            lblDec["text"] = dec
        else:
            lblDec["text"] = "Insira apenas números inteiros!!"
        return lblDec

# labels que exibirão o resultado da criptografia / descriptografia    
lblEncCabecalho = Label(leftFrame,text="O texto criptografado é: ", foreground="black")#tenho q retornar a porra do bagui cripto...
lblEncCabecalho.pack()
lblEncCabecalho.configure(relief="ridge", font="Arial 16 ", border= 0)

lblEnc = Label(leftFrame,text="-------------", foreground="black")#tenho q retornar a porra do bagui cripto...
lblEnc.pack()
lblEnc.configure(relief="ridge", font="Arial 16 ", border= 0)

lblEncCabecalho2 = Label(rightFrame,text="O texto descriptografado é: ", foreground="black")#tenho q retornar a porra do bagui cripto...
lblEncCabecalho2.pack()
lblEncCabecalho2.configure(relief="ridge", font="Arial 16 ", border= 0)

lblDec = Label(rightFrame,text="--------------", foreground="black")#tenho q retornar a porra do bagui cripto...
lblDec.pack()
lblDec.configure(relief="ridge", font="Arial 16 ", border= 0)

class Chaves(Criptografia):

    def __init__(self, p, q):
        self.p = p
        self.q = q

        n=self.p*self.q
        phi=(self.p-1)*(self.q-1)  # Função totiente de Euler ou função Phi
        lblEscolherChave["text"]  = str(self.coprimos(phi)) + "\n"  # calculo da chave pública mdc(phi(N), E) == 1

    def gerar_chaves(self):
        n=self.p*self.q
        phi=(self.p-1)*(self.q-1)  # Função totiente de Euler ou função Phi

        # aqui, é validada se as entradas são numericas ou não
        if(str(txtChavePublicaR.get()).isnumeric()):
            e= int(txtChavePublicaR.get())
            d=self.inverso_modular(e,phi) # calculo da chave privada d*e = 1 mod(φ(n))
            lblChave["text"] = "\nChaves públicas (e=" + str(e) + ", n=" + str(n) + ")" + "\nChaves privadas (d="+ str(d)  + ", n=" + str(n) + ")\n"
        else:
            lblChave["text"] = "Insira apenas números inteiros!"
        return lblChave
    
    def mdc(self, a, b):
        while a != 0:
            a, b = b % a, a
        return b

    def inverso_modular(self, a, m): 
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None
        
    def coprimos(self, a):
        l = []
        for x in range(2, a): 
            if self.mdc(a, x) == 1 and self.inverso_modular(x,a) != None: #  MDC(φ(n), e) = 1
                l.append(x)
        for x in l:
            if x == self.inverso_modular(x,a):
                l.remove(x)
        return l
 
#exibição das chaves - essas labels exibem as chaves que estão disponiveis para a escolha e as chaves que serão usadas
#em na criptografia que será executada no momento
lblEscolherChave = Label(topFrame,text="escolherchave" ,foreground="black")
lblEscolherChave.pack()
lblEscolherChave.configure(relief="ridge", font="Arial 16 ", border= 0)

lbl3 = Label(topFrame,text="-------------------------------------------------------------------", foreground="black") #exibindo o resultado
lbl3.pack()
lbl3.configure(relief="ridge", font="Arial 16 ", border= 0)

lblChave = Label(topFrame,text="chave que serão usadas" ,foreground="black")
lblChave.pack()
lblChave.configure(relief="ridge", font="Arial 16 ", border= 0)

#botões - aqui, os botões são definidos e as funções são chamadas. Sempre que o botão for clicado, ele executa a função
# que está no command

criptografia = Criptografia()
chaves = Chaves(numero_p, numero_q)
btnCripto = Button(leftFrame, text="Gerar Chaves", fg="green", command = chaves.gerar_chaves)
btnCripto.pack() # gera as chaves que serão usadas na criptografia do texto inputado

btnCripto = Button(leftFrame, text="Criptografar", fg="green", command = criptografia.encripta_mensagem)
btnCripto.pack() #criptografa o texto inputado

btnDescripto = Button(rightFrame, text="Descriptografar", fg="green", command = chaves.decripta_mensagem)
btnDescripto.pack() #descriptografa o texto inputado

btnQuit = Button(rightFrame, text="Sair", fg="red",font=" arial",command=quit)
btnQuit.pack() # fecha o programa
        
root.mainloop() #finaliza o form
