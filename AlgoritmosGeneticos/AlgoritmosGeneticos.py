from random import random as ran
import matplotlib.pyplot as plt

#Classe produto
class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor

#### INICIO - Classe Individuo ####
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
       # print ("Antes %s" %self.cromossomo)
        for i in range (len(self.cromossomo)):
            if ran() < taxa_mutacao:
                if self.cromossomo[i] == "1":
                    self.cromossomo[i] = "0"
                else:
                    self.cromossomo[i] = "1"
       # print ("Depois %s" %self.cromossomo)
        return self
### FIM - Classe Individuos ###
    
    
### INICIO - Classe AlgoritmoGenetico ###
class AlgoritmoGenetico():
    def __init__(self, tamanho_populacao):
        self.tamanho_populacao = tamanho_populacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0
        self.lista_solucoes = []
        
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
    
    def selecionaPai(self, somatotal):
        pai = -1
        valor_sorteado = ran() * somatotal
        soma = 0
        i = 0
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai+=1
            i+=1
        return pai
    
    def visualizaMelhor(self):
        melhor = self.populacao[0]
        print ("G: %s \n Valor: %s \n Espaco: %s \n Cromossomo: %s" % (melhor.geracao,
                                                                      melhor.nota_avaliacao,
                                                                      melhor.espaco_usado,
                                                                      melhor.cromossomo))
    
    def resolver(self, taxa_mutacao, numero_geracoes, espacos, valores, limite_espacos):
        ##Inicializa a população aleatoriamente
        self.inicializaPopulacao(espacos, valores, limite_espacos)
        
        ##Avalia os individuos
        for individuo in self.populacao:
            individuo.avaliacao()
        ##Ordena, do melho para o pior e imprime o melhor    
        self.ordenaPopulacao()
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        self.visualizaMelhor()
        
        ##Gerando novas geracoes
        for geracao in range(numero_geracoes):
            soma_avaliacao = self.somaAvaliacoes()
            nova_populacao = []
            ##Seleciona os pais para as proximas geracoes
            for individuos in range(0, self.tamanho_populacao, 2):
                pai1 = self.selecionaPai(soma_avaliacao)
                pai2 = self.selecionaPai(soma_avaliacao)
                
                ##Gera os filhos atraves do crossover
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])
                
                ##Aplica mutacao aos filhos
                nova_populacao.append(filhos[0].mutacao(taxa_mutacao))
                nova_populacao.append(filhos[1].mutacao(taxa_mutacao))
            
            ##Descarta-se a antiga populacao e passa a nova
            self.populacao = list(nova_populacao)
            
            ##Avalia novamente cada individuo
            for individuo in self.populacao:
                individuo.avaliacao()
            ##Ordena a populacao
            self.ordenaPopulacao()
            #Visualiza o melhor entre todas as geracoes
            self.visualizaMelhor()
            ##Separa o melhor individuo
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            
            self.melhorIndividuo(melhor)
            
        print("\nMelhor solucao  -> G: %s -> Valor: %s -> Espaco: %s => CROMOSSOMO: %s" % 
              (self.melhor_solucao.geracao,
               self.melhor_solucao.nota_avaliacao,
               self.melhor_solucao.espaco_usado,
               self.melhor_solucao.cromossomo))
            
        return self.melhor_solucao.cromossomo
            
            
            
if __name__ == '__main__':

    lista_produtos = []
    
    '''conexao = pymysql.connect(host='localhost', user='root', passwd='', db='produtos')
    bdCursor = conexao.cursor()
    bdCursor.execute('select nome, espaco, valor, quantidade from produtos')
    for produto in bdCursor:
        for i in range(produto[3]):
            lista_produtos.append(Produto(produto[0], produto[1], produto[2]))
    
    bdCursor.close()
    conexao.close()'''
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
    ### Taxa mutacão
    taxa_mutacao = 0.01
    ### Numero de gerações
    numero_geracoes = 1000
    ag = AlgoritmoGenetico(tamanho_pop)
    
    resultado = ag.resolver(taxa_mutacao, numero_geracoes, espacos, valores, limite)
    
    for i in range(len(lista_produtos)):
        if resultado[i] == "1":
            print("Nome: %s Valor: %s" % (lista_produtos[i].nome, lista_produtos[i].valor))
            
    plt.plot(ag.lista_solucoes)
    plt.title("Valores ")
    plt.show()