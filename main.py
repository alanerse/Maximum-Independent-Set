arq = open('grafo_modelo.txt', 'r')
texto = []
matriz = []
texto = arq.readlines()
for i in range(len(texto)):
    if(i != 0):
       matriz.append(texto[i].split())

arq.close()
n = i

listaVertices = []
vertice = {
    'valor': None,
    'adjacentes':[],
    'presente':False
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

arqSat = open('grafo_Sat_modelo1.txt', 'r')
textoSat = []
matrizSat = []
matrizGrafoSat= []
matrizAux = []
textoSat = arqSat.readlines()
for i in range(len(textoSat)):
    if(i != 0):
       matrizSat.append(textoSat[i].split())

arqSat.close()
variaveisSat = textoSat[0].split()
variaveisSat = int(variaveisSat[0])
for y in range(len(matrizSat)*variaveisSat):
    linhaAux = []
    matrizGrafoSat.append(linhaAux[:])
for z in range(len(matrizSat)):
    linhaAux = []
    matrizAux.append(linhaAux[:])

i=0
j=0

for i in range(len(matrizSat)):
    for j in range(variaveisSat):
        print(matrizSat[i][j])
        if(matrizSat[i][j] != '2' ):
            matrizAux[i].append('1')
        else:
           matrizAux[i].append('0')
i = 0
j = 0

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

# ATRIBUICAO DAS ADJACENCIAS A PARTIR DO 6
for i in range(len(matrizAux)):
    for j in range(variaveisSat):
        if(matrizAux[i][j] == '1'):
            verticeSat['valor'] = i*variaveisSat+j
            for k in range(variaveisSat):
                if(matrizAux[i][k] == '1' and k!=j):
                    verticeSat['adjacentes'].append(int(k))
                    if(matrizSat[i][j] == '0'):
                        verticeSat['barrado'] = True
            listaSAT[i*variaveisSat+j] = verticeSat
            verticeSat = {
                'valor': None,
                'adjacentes': [],
                'presente': False,
                'barrado': False,
            }


i=0
j=0
for i in range(len(matrizAux)):
    for j in range(len(matrizAux)*variaveisSat):
        if(j%variaveisSat==i):

            if (listaSAT[j]["valor"] != None and len(listaSAT[j])!=0 and i!=j and listaSAT[i]["barrado"] != listaSAT[j]["barrado"]):
                listaSAT[i]["adjacentes"].append(listaSAT[j]["valor"])
                listaSAT[j]["adjacentes"].append(listaSAT[i]["valor"])
i=0

#def eCompleta():
melhor = []
consistente=False
contar = 0
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

solucao = []
j=0
BranchBound(listaSAT, solucao, len(listaSAT), j)
print("Satisfabilidade: ")
solucao = []
j=0

for i in melhor:

    print(i["valor"] , " ")
#for i in listaVertices:
del melhor[:]

# for i in range(n):
#     for j in range(n):
#         if(len(listaVertices[i]['adjacentes']) < len(listaVertices[j]['adjacentes']) ):
#             aux = listaVertices[j]
#             listaVertices[j] = listaVertices[i]
#             listaVertices[i] = aux
j = 0

#solucoes = []
j=0
BranchBound(listaVertices, solucao, n, j)
print("Conjunto independente maximo: ")

for i in melhor:

    print(i["valor"] , " ")

del listaVertices[:]
del melhor[:]
for i in range(n):
    for j in range(n):
        if(i==j) :
            matriz[i][j]='0'
        else:
            if(matriz[i][j]=='1'):
                matriz[i][j]='0'
            else:
                matriz[i][j]='1'

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

j=0
BranchBound(listaVertices, solucao, n, j)
print("Clique maximo: ")

for i in melhor:

    print(i["valor"] , " ")


