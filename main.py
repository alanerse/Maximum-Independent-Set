import time
#variaveis globais
melhor = []
consistente=False
contar = 0

def leArquivo(nome, matriz):

    arq = open(nome, 'r')
    texto = []
    texto = arq.readlines()
    for i in range(len(texto)):
        if(i != 0):
           matriz.append(texto[i].split())

    arq.close()

def solucaoInicial(listaVertices):
    inicial = []
    #percorremos a lista e inserimos na solucao quando eConsistente retornar verdadeiro
    for i in range(len(listaVertices)):
        inicial.append(listaVertices[i])
        if (eConsistente(inicial,listaVertices[i],listaVertices)!=True):
            inicial.pop()
    return inicial

def BranchBound(listaVertices, solucao, tam, j):
    global melhor
    global consistente
    global contar

    if(eCompleta(j,tam)):
        contar = contar + 1

        if(len(solucao) >= len(melhor)):
            melhor = solucao[:]

    else:

        while (j < tam):
            solucao.append(listaVertices[j])
            if(ePromissor(listaVertices,solucao,melhor)):
                consistente = eConsistente(solucao,listaVertices[j],listaVertices)
                if(consistente):
                    BranchBound(listaVertices,solucao,tam, j+1)

            aux = solucao.pop()

            if(aux["valor"]!= None):
                listaVertices[aux["valor"]]["presente"]=False

            j = j+1

            if (eCompleta(j, tam)):
                contar = contar + 1
                #se a quantidade de vertices da solucao atual for melhor q a quantidade de vertices da melhor solucao
                #atualiza se a melhor solucao
                if (len(solucao) >= len(melhor)):
                    melhor = solucao[:]

def eCompleta(j,tam):
    #se o j for igual ao tamanho quer dizer q ja percorri toda a lista verificando se eConsistente e se ePromissor
    #sendo assim nao tem mais ninguem para inserir e a solucao e Completa
    if(j==tam):
        return True
    return False

def ePromissor(listaVertices,solucao,melhor):

    cont = 0
    #verificamos se na solucao atual e possivel inserir mais vertices do que a melhor solucao
    for a in listaVertices:
        if(a["presente"]==False):
            cont = cont + 1
    if(len(melhor)< len(solucao)+cont-1):
        return True
    else:
        return False

def eConsistente(solucao,inserido,listaVertices):
    #se o vertice a ser inserido ja esta na solucao, entao nao e consistente
    if (inserido['presente'] == 'True' or inserido['valor'] == None):
        return False
    #verificacao se o vertice a ser inserido tem adjacencia com alguem q ja esta na solucao
    for i in solucao:
        for j in i['adjacentes']:
            if (j == inserido['valor']):
                return False
    listaVertices[inserido['valor']]['presente'] = True

    return True

def criaListaAdjacencias(listaVertices, matriz,n):
    vertice = {
        'valor': None,
        'adjacentes': [],
        'presente': False
    }
    #cria a lista de adjacencias
    for i in range(n):
        vertice['valor'] = i
        for j in range(n):
            if(matriz[i][j] == '1'):
                vertice['adjacentes'].append(j)
        listaVertices.append(vertice)
        vertice = {
            'valor': None,
            'adjacentes': [],
            'presente':False

        }

def clique(nome):
    global melhor
    matriz = []
    leArquivo(nome, matriz)
    n = len(matriz)

    listaVertices = []
    # criaListaAdjacencias(listaVertices, matriz,n)

    vertice = {
        'valor': None,
        'adjacentes': [],
        'presente': False

    }
    #criando o grafo complemento, sem arestas do vertice para ele mesmo
    for i in range(n):
        for j in range(n):
            if (i == j):
                matriz[i][j] = '0'
            else:
                if (matriz[i][j] == '1'):
                    matriz[i][j] = '0'
                else:
                    matriz[i][j] = '1'
    #criacao da lista de adjacencias
    for i in range(n):
        vertice['valor'] = i
        for j in range(n):
            if (matriz[i][j] == '1'):
                vertice['adjacentes'].append(j)
        listaVertices.append(vertice)
        vertice = {
            'valor': None,
            'adjacentes': [],
            'presente': False

        }

    j = 0
    solucao = []
    melhor = solucaoInicial(listaVertices)
    BranchBound(listaVertices, solucao, n, j)
    print("Clique maximo: ")
    #impressao do clique maximo
    for i in melhor:
        print(i["valor"], " ")

def sat(nome):
    global melhor
    matrizSat = [] #matriz no formato da entrada do arquivo
    leArquivo(nome,matrizSat)
    matrizAux = [] #matriz para saber quais sao os grafos completos
    variaveisSat = len(matrizSat[0])

    #Cria a matrizAux
    for z in range(len(matrizSat)):
        linhaAux = []
        matrizAux.append(linhaAux[:])

    #Leitura do arquivo
    for i in range(len(matrizSat)):
        for j in range(variaveisSat):
            if(matrizSat[i][j] != '2' ):
                matrizAux[i].append('1')
            else:
               matrizAux[i].append('0')

    listaSAT = []

    #Alocação do meu dicionario na listaSat
    for y in range(len(matrizSat)*variaveisSat):
        verticeSatAux = {
            'valor': None,
            'adjacentes': [],
            'presente': False,
            'barrado': False,
        }
        listaSAT.append(verticeSatAux)

    verticeSat = {
        'valor': None,
        'adjacentes':[],
        'presente':False,
        'barrado':False,
    }
    # so estou testando
    #Criação dos grafos completos para cada clausula
    for i in range(len(matrizAux)):
        for j in range(variaveisSat):
            if(matrizAux[i][j] == '1'):
                # usamos esse calculo para poder definir os valores dos vertices, sendo util para poder repetir vertices
                verticeSat['valor'] = i*variaveisSat+j
                for k in range(variaveisSat):
                    if(matrizAux[i][k] == '1' and k!=j):
                        verticeSat['adjacentes'].append(int(i*variaveisSat+k))
                        if(matrizSat[i][j] == '0'):
                            verticeSat['barrado'] = True
                listaSAT[i*variaveisSat+j] = verticeSat
                verticeSat = {
                    'valor': None,
                    'adjacentes': [],
                    'presente': False,
                    'barrado': False,
                }

    #adicionar as arestas que estavam faltando no grafo
    for i in range(len(matrizAux)*variaveisSat):
        for j in range(len(matrizAux)*variaveisSat):
            if(j>i and listaSAT[i]["valor"]!=None and j%variaveisSat==(listaSAT[i]["valor"]%variaveisSat)):

                if (listaSAT[j]["valor"] != None and len(listaSAT[j])!=0 and i!=j and listaSAT[i]["barrado"] != listaSAT[j]["barrado"]):
                    listaSAT[i]["adjacentes"].append(listaSAT[j]["valor"])
                    listaSAT[j]["adjacentes"].append(listaSAT[i]["valor"])

    solucao = []

    melhor = solucaoInicial(listaSAT)
    #Chamamos o BranchBound para retornar o conjunto independente maximo.
    BranchBound(listaSAT, solucao, len(listaSAT), 0)
    print("Satisfabilidade: ")
    solucao = []

    valorVariavelSat=[]
    #alocacao do vetor de lista
    for j in range(variaveisSat):
        listaux = []
        valorVariavelSat.append(listaux)
    #Adicionando o valor da variavel (barrado ou nao barrado)
    for j in range(len(melhor)):
        valorVariavelSat[melhor[j]['valor']%variaveisSat].append(melhor[j]['barrado'])


    contar = 0
    temSolucao = True
    #verificacao se tem ou se nao tem resposta factivel (verificador para sat)
    for i in range(len(matrizSat)):
        for j in range(variaveisSat):
            if(len(valorVariavelSat[j]) != 0):
                if(valorVariavelSat[j][0]== True):
                    if(matrizSat[i][j] == '0'):
                        matrizSat[i][j] = '1'
                    else:
                        matrizSat[i][j] = '0'
            if(matrizSat[i][j]=='2'):
                matrizSat[i][j] = '0'
            if(matrizSat[i][j] == '1'):
                contar = contar + 1

        if(contar==0):
            print('Nao tem respostar factivel para esta expressao')
            temSolucao = False
            break
            #return false
        contar=0

    if(temSolucao):
        #impressao da solucao
        for i in range(len(valorVariavelSat)):

            if(len(valorVariavelSat[i]) > 0):

                if(valorVariavelSat[i][0] == True):
                    print("Variavel "+ str(i) + " tem que ser falsa ")
                else:
                    print("Variavel "+ str(i) + " tem que ser verdadeira")

            else:
                print("Variavel "+ str(i) + " pode ser verdadeira ou falsa")

def conjuntoIndependenteMaximo(nome):
    global melhor
    matriz = []
    solucao = []
    leArquivo(nome, matriz)
    n = len(matriz)

    listaVertices = []
    criaListaAdjacencias(listaVertices, matriz, n)

    melhor = solucaoInicial(listaVertices)
    print(melhor)
    BranchBound(listaVertices, solucao, n, 0)
    print("Conjunto independente maximo: ")

    #impressao do conjunto independente maximo
    for i in melhor:
        print(i["valor"], " ")

segundos = time.time()
conjuntoIndependenteMaximo("grafo.txt")
print("Tempo gasto:" + str(time.time()-segundos))
segundos = time.time()
clique("grafo.txt")
print("Tempo gasto:" + str(time.time()-segundos))
segundos = time.time()
sat("entradaSat.txt")
print("Tempo gasto:" + str(time.time()-segundos))
