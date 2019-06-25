arq = open('grafo_modelo2.txt', 'r')
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
    if (inserido['presente'] == 'True'):
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
#for i in listaVertices:


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
print("Conjunto independente máximo: ")

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
print("Clique máximo: ")

for i in melhor:

    print(i["valor"] , " ")
