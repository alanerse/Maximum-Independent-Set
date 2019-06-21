arq = open('grafo.txt', 'r')
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


def BranchBound(listaVertices, solucao, tam, j):
    if(eCompleta(listaVertices)):
        return solucao
    else:

        while (j < tam):
            solucao.append(listaVertices[j])
            if(ePromissor(listaVertices[j]) & eConsistente(solucao,listaVertices[j],listaVertices)):
                BranchBound(listaVertices,solucao,tam, j+1)
            else:
                solucao.pop()
                j = j+1



def eCompleta(listaVertices):
    for i in listaVertices:
        if(i['presente'] == False):
            return False
    return True

def ePromissor(inserido):
    if(inserido['presente'] == 'True'):
        return False
    return True

def eConsistente(solucao,inserido,listaVertices):
    for i in solucao:
        for j in i['adjacentes']:
            if(j == inserido['valor']):
                return False
    listaVertices[inserido['valor']]['presente'] = True
    for j in inserido['adjacentes']:
        listaVertices[j]['presente'] = True
    #listaVertices[inserido[]]
    return True
solucao = []
#for i in listaVertices:
for i in range(n):
    for j in range(n):
        if(len(listaVertices[i]['adjacentes']) < len(listaVertices[j]['adjacentes']) ):
            aux = listaVertices[j]
            listaVertices[j] = listaVertices[i]
            listaVertices[i] = aux
j = 0
BranchBound(listaVertices, solucao, n, j)