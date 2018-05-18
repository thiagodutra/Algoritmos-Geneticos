from random import random as ran

#Classe produto
class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor

#### INICIO - Classe Individuo ###
class Individuo():
    ##Construtuor do Individuo
    def __init__(self, espacos, valores, limite_espacos, geracao = 0):
        self.espacos = espacos
        self.valores = valores
        self.limite_espacos = limite_espacos
        self.nota_avaliacao = 0
        self.espaco_usado = 0
        self.geracao = geracao
        self.cromossomo = []
        
        #Criando individuo aleatoriamente. NADA DE INTELIGENCIA, AINDA
        for i in range (len(espacos)):
            if ran() < 0.5:
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
    
    #Função avaliacão
    #Se a carga passar dos 3mC, entao recebe nota 1(baixa)
    #Se não passar, recebe a nota igual ao valor dos produtos
    def avaliacao(self):
        nota = 0
        soma_espacos = 0
        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == "1":
                nota += self.valores[i]
                soma_espacos += self.espacos[i]
            if soma_espacos > self.limite_espacos:
                nota = 1
            self.nota_avaliacao = nota
            self.espaco_usado = soma_espacos
                
    ### Funcao de crossover
    def crossover(self, individuo):
        ##Calcula o corte (de um ponto) aleatoriamente
        corte = round(ran() * len(self.cromossomo))
        
        ##Cria os CROMOSSOMOS dos filhos a partir do corte criado
        filho1 = individuo.cromossomo[0:corte] + self.cromossomo[corte::]
        filho2 = self.cromossomo[0:corte] + individuo.cromossomo[corte::]
        
        ##cria os individuos filho
        filhos = [Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1),
                  Individuo(self.espacos, self.valores, self.limite_espacos, self.geracao + 1)]
        
        ##Necessário setar o cromossomo para esses filhos
        filhos[0].cromossomo = filho1
        filhos[1].cromossomo = filho2
        
        return filhos
    
    ### Funcao de mutacao
    def mutacao(self, taxa_mutacao):
        print ("Antes %s" %self.cromossomo)
        for i in range (len(self.cromossomo)):
            if ran() < taxa_mutacao:
                if self.cromossomo[i] == "1":
                    self.cromossomo[i] = "0"
                else:
                    self.cromossomo[i] = "1"
        print ("Depois %s" %self.cromossomo)
        return self
### FIM - Classe Individuos ###
    
    
### INICIO - Classe AlgoritmoGenetico ###
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        
    ### Inicializa a populacao inicial ###    
    def inicializaPopulacao(self, espaco, valores, limite):
        for i in range(self.tamanho_populacao):
            self.populacao.append(Individuo(espaco, valores, limite))
        ### Ainda sem verificar de forma correta o melhor individuo ###
        self.melhor_solucao = self.populacao[0]

    ### Ordena a população, da maior nota de avaliação para a menor ###
    def ordenaPopulacao(self):
        self.populacao = sorted(self.populacao, 
                                key = lambda populacao: populacao.nota_avaliacao,
                                reverse = True)
    ### Função para pegar o melhor individuo ###
    def melhorIndividuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
    
    ### Soma das notas de avaliacao de uma populacao        
    def somaAvaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao
        return soma
    
    
    
    
if __name__ == '__main__':

    lista_produtos = []
    lista_produtos.append(Produto("Geladeira Dako", 0.751, 999.90))
    lista_produtos.append(Produto("Iphone 6", 0.0000899, 2911.12))
    lista_produtos.append(Produto("TV 55' ", 0.400, 4346.99))
    lista_produtos.append(Produto("TV 50' ", 0.290, 3999.90))
    lista_produtos.append(Produto("TV 42' ", 0.200, 2999.00))
    lista_produtos.append(Produto("Notebook Dell", 0.00350, 2499.90))
    lista_produtos.append(Produto("Ventilador Panasonic", 0.496, 199.90))
    lista_produtos.append(Produto("Microondas Electrolux", 0.0424, 308.66))
    lista_produtos.append(Produto("Microondas LG", 0.0544, 429.90))
    lista_produtos.append(Produto("Microondas Panasonic", 0.0319, 299.29))
    lista_produtos.append(Produto("Geladeira Brastemp", 0.635, 849.00))
    lista_produtos.append(Produto("Geladeira Consul", 0.870, 1199.89))
    lista_produtos.append(Produto("Notebook Lenovo", 0.498, 1999.90))
    lista_produtos.append(Produto("Notebook Asus", 0.527, 3999.00))
    
    espacos = []
    valores = []
    nomes = []
    
    for produtos in lista_produtos:
        espacos.append(produtos.espaco)
        valores.append(produtos.valor)
        nomes.append(produtos.nome)
    ### Limite do caminhao em m cubico
    limite = 3
    ### Tamanho populacao incicial
    tamanho_pop = 30
    
    
    ag = AlgoritmoGenetico(tamanho_pop)
    ag.inicializaPopulacao(espacos, valores, limite)
    
    
    for individuos in ag.populacao:
        individuos.avaliacao()
    ag.ordenaPopulacao()
    ag.melhorIndividuo(ag.populacao[0])
    print("*** Melhor Individuo ***\nCromossomo = %s\n" %str(ag.melhor_solucao.cromossomo),
              "Nota = %s" %ag.melhor_solucao.nota_avaliacao)
    
    
    
    
    
    """
    
    Testes de implementação anteriores
    
    ##Inicio Individuo 1
    individuo1 = Individuo(espacos, valores, limite)
    for i in range(len(lista_produtos)):
        if individuo1.cromossomo[i] == "1":
            print("Nome: %s Valor: %s" % (lista_produtos[i].nome, lista_produtos[i].valor))
            
    individuo1.avaliacao()
    print ("Nota = %s" % individuo1.nota_avaliacao)
    print ("Espaco Usado = %s" % individuo1.espaco_usado)
    ### FIM Individuo 1 ###
    
    ##########################
    print("\n Individuo 2 \n")
    
    ### Inicio Individuo 2 ###
    individuo2 = Individuo(espacos, valores, limite)
    for i in range(len(lista_produtos)):
        if individuo1.cromossomo[i] == "1":
            print("Nome: %s Valor: %s" % (lista_produtos[i].nome, lista_produtos[i].valor))
            
    individuo2.avaliacao()
    print ("Nota = %s" % individuo2.nota_avaliacao)
    print ("Espaco Usado = %s" % individuo2.espaco_usado)
    ### FIM Individuo 2 ###
    
    ## Chamada da função crossover ##
    
    filhos = individuo1.crossover(individuo2)
    print ("\nFilhos: \nFilho1 = %s \nFilho2 = %s" % (filhos[0].cromossomo, filhos[1].cromossomo))
    
    ##Mutacao
    print ("\nMutacao: \n Individuo 1\n")
    individuo1.mutacao(0.05)
    print ("\n Individuo 2: \n")
    individuo2.mutacao(0.08)
    
    """