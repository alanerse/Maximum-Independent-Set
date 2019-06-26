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
                # for k in aux["adjacentes"]:
                #     listaVertices[k]["presente"]=False
            j = j+1

            if (eCompleta(j, tam)):
                contar = contar + 1

                if (len(solucao) >= len(melhor)):
                    melhor = solucao[:]

def eCompleta(j,tam):

    if(j==tam):
        return True
    return False

def ePromissor(listaVertices,solucao,melhor):

    cont = 0
    for a in listaVertices:

        if(a["presente"]==False):
            cont = cont + 1
    if(len(melhor)< len(solucao)+cont-1):
        return True
    else:
        return False

def eConsistente(solucao,inserido,listaVertices):
    if (inserido['presente'] == 'True' or inserido['valor'] == None):
        return False
    for i in solucao:
        for j in i['adjacentes']:
            if (j == inserido['valor']):
                return False
    listaVertices[inserido['valor']]['presente'] = True
    # for j in inserido['adjacentes']:
    #     listaVertices[j]['presente'] = True
    # listaVertices[inserido[]]
    return True

def criaListaAdjacencias(listaVertices, matriz,n):
    vertice = {
        'valor': None,
        'adjacentes': [],
        'presente': False
    }
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

    for i in range(n):
        for j in range(n):
            if (i == j):
                matriz[i][j] = '0'
            else:
                if (matriz[i][j] == '1'):
                    matriz[i][j] = '0'
                else:
                    matriz[i][j] = '1'

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
    melhor = []
    BranchBound(listaVertices, solucao, n, j)
    print("Clique maximo: ")

    for i in melhor:
        print(i["valor"], " ")

def sat(nome):
    global melhor
    matrizSat = []
    leArquivo(nome,matrizSat)
    matrizGrafoSat= []
    matrizAux = []
    variaveisSat = len(matrizSat[0])
    #Cria a matrizGrafosat
    for y in range(len(matrizSat)*variaveisSat):
        linhaAux = []
        matrizGrafoSat.append(linhaAux[:])
    #Cria a matrizAux
    for z in range(len(matrizSat)):
        linhaAux = []
        matrizAux.append(linhaAux[:])

    for i in range(len(matrizSat)):
        for j in range(variaveisSat):
            if(matrizSat[i][j] != '2' ):
                matrizAux[i].append('1')
            else:
               matrizAux[i].append('0')

    listaSAT = []
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

    for i in range(len(matrizAux)):
        for j in range(variaveisSat):
            if(matrizAux[i][j] == '1'):
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

    for i in range(len(matrizAux)*variaveisSat):
        for j in range(len(matrizAux)*variaveisSat):
            if(j>i and listaSAT[i]["valor"]!=None and j%variaveisSat==(listaSAT[i]["valor"]%variaveisSat)):

                if (listaSAT[j]["valor"] != None and len(listaSAT[j])!=0 and i!=j and listaSAT[i]["barrado"] != listaSAT[j]["barrado"]):
                    listaSAT[i]["adjacentes"].append(listaSAT[j]["valor"])
                    listaSAT[j]["adjacentes"].append(listaSAT[i]["valor"])

    solucao = []
    melhor = []
    BranchBound(listaSAT, solucao, len(listaSAT), 0)
    print("Satisfabilidade: ")
    solucao = []

    valorVariavelSat=[]
    for j in range(variaveisSat):
        listaux = []
        valorVariavelSat.append(listaux)

    for j in range(len(melhor)):
        valorVariavelSat[melhor[j]['valor']%variaveisSat].append(melhor[j]['barrado'])


    contar = 0
    temSolucao = True
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

    melhor = []
    BranchBound(listaVertices, solucao, n, 0)
    print("Conjunto independente maximo: ")

    for i in melhor:
        print(i["valor"], " ")


conjuntoIndependenteMaximo("grafo_modelo.txt")
sat("grafo_Sat_modelo1.txt")
clique("grafo_modelo.txt")
