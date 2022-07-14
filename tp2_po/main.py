import numpy as np
import sys

pth = "input.txt"

def preProcess(entradas):
  n,m = entradas[0]
  n = int(n)
  m = int(m)
  mat = np.zeros([2*n,m])
  for i in range(1, (2*n)+1):
    for j in range(0, m):
      mat[i-1][j] = int(entradas[i][j])
  c = np.zeros([1, m])
  for i in range(m):
    c[0][i] = int(entradas[-1][i])
  return n, m, mat, c

def lerEntrada(pth):
    file = open(pth, "r")
    lista_entradas = []
    for linha in file:
        entradas = linha.split()
        lista_entradas.append(entradas)

    file.close()

    return lista_entradas


class Fila:
  def __init__(self):
    self.fila = []

  def remove(self):
    head = self.fila[0]
    self.fila.pop(0)
    return head

  def adiciona(self, e):
    self.fila.append(e)
  
  def size(self):
    return len(self.fila)
  
def map(x):
  return chr(x+65)


def bfs(mi, c, h, y, menor):
  n,m = mi.shape
  x = np.zeros([1,mi.shape[1]])
  memory = np.zeros(mi.shape[0])
  result = []
  for its in range(n):
    fila = Fila()
    if memory[its] == 0:
      fila.adiciona(its)
    while(fila.size() != 0):
      vertice = fila.remove()
      memory[vertice] = 1
      for j in range(m):
        if mi[vertice][j] == 1:
         for i in range(vertice+1, n):
            if mi[i][j] == 1:
              if menor == c[0][j]:
                h[vertice][j] = 1
                h[i][j] = 1
                x[0][j] = 1
              ##print("[ {} -> {} ]".format(map(vertice), map(i)))
                fila.adiciona(i)
              break
  return h, x

def bfss(n, m, mi, v, y):
  memory = np.zeros(2*n)
  p = np.zeros([1, m])
  noFlag = False
  folhas = []
  fila = Fila()
  fila.adiciona(v)
  #print("vertice", v)
  while fila.size() != 0:
    vertice = fila.remove()
    noFlag = False
    #print("vertice:", vertice)
    memory[vertice] = 1
    if vertice < n:
      for j in range(m):
        if mi[vertice][j] == 1:
          for i in range(2*n):
            if mi[i][j] == 1 and i != vertice and memory[i] == 0:
              #print("[ {} -> {} ]".format(map(vertice), map(i)))
              fila.adiciona(i)
              p[0][j] = 1
              noFlag = True
    else:
      for j in range(m):
        if mi[vertice][j] == 1 and y[0][j] == 1:
          for i in range(2*n):
            if mi[i][j] == 1 and i != vertice and memory[i] == 0:
              #print("[ {} -> {} ]".format(map(vertice), map(i)))
              fila.adiciona(i)
              p[0][j] = 1
              noFlag = True
    if not noFlag:
      folhas.append(vertice)
  return p, folhas
    #print(map(vertice))

def encontrarVizinhos(n, m, mat, v):
  #vizinhos = np.zeros([1, 2*n])
  vizinhos = []
  arestas = []
  for j in range(m):
    if mat[v][j] == 1:
      for i in range(2*n):
        if mat[i][j] == 1 and i != v:
          vizinhos.append(int(i))
          arestas.append(int(j))
          break
  return vizinhos, arestas

def inverte(m, y, p):
  for i in range(m):
    aux = abs(y[0][i]-p[0][i])
    y[0][i] = aux
  return y

def confereTodosVizinhosEmparelhados(n, M, vizinhos):
  for i in vizinhos:
    if M[0][i] == 0:
      return False
  return True

def emparelhamento(n, m, mat):
  v = 0
  yv = np.ones([n, m])
  Mv = np.zeros([1, 2*n])         #M vazio
  y = np.zeros([1, m])            #M vazio
  for vv in range(n):
    if Mv[0][vv] == 0:
      v = vv
      it = 0                 
      vizinhos, arestas = encontrarVizinhos(n, m, mat, v)
      for vvv in range(len(vizinhos)):
        if Mv[0][vizinhos[vvv]] == 0:
          Mv[0][v] = 1
          Mv[0][vizinhos[vvv]] = 1
          y[0][arestas[vvv]] = 1
          break
  for i in range(n):                    #confere se tem um vértice de A não emparelhado
    if Mv[0][i] == 0:
      vizinhos, arestas = encontrarVizinhos(n, m, mat, i)
      if len(vizinhos) == 0:
        return False, Mv, y
      #print("2:", vizinhos)
      if confereTodosVizinhosEmparelhados(n, Mv, vizinhos):
        v = i
        Mv[0][i] = 1
        #print("Mv:", Mv)
        #print("vertice in:",i )
        p, folhas = bfss(n, m, mat, v, y)
        print(p)
        #print(folhas)
        for folha in folhas:
          if folha > n:
            Mv[0][folha] = 1
            y = inverte(m, y, p)
          else:
             return False, Mv, y
  return True, Mv, y

def atualizaH(n, m, mat, math, y, c):
  for i in range(n):
    vizinhos, arestas = encontrarVizinhos(n, m, mat, i)
    for idx in range(len(vizinhos)):
      if c[0][arestas[idx]] == y[0][i]+y[0][vizinhos[idx]]:
        math[i][arestas[idx]] = 1
        math[vizinhos[idx]][arestas[idx]] = 1
  return math

def rers(n, m, c):
  fila = Fila()


def retornaMenor(m, c, piso):
  menor = np.inf
  idx = -1
  for i in range(m):
    if c[0][i] < menor and c[0][i] > piso:
      menor = c[0][i]
      idx = i
  return menor, idx
  
def atualizaY(n, m, c, piso, yv, mat):
  menor, idx = retornaMenor(m, c, piso)
  for i in range(n):
    if mat[i][idx] == 1:      
      for k in range(n, 2*n):
        if mat[k][idx] == 1:
          eps = menor - (yv[0][k]+yv[0][i])
          yv[0][i] += eps
          yv[0][k] -= eps
  return menor, yv
  
def main(pth):
  entradas = lerEntrada(pth)
  n, m, mat, c = preProcess(entradas)
  emp, mv, ma = emparelhamento(n, m, mat)
  h = np.zeros([2*n, m])
  if not emp:
    print(-1)
    print(mv[0][:n].squeeze())
    print(mv[0][n:].squeeze())
    return 0
  else:
    menor, idx = retornaMenor(m, c, 0)
    memory = np.zeros([m])
    yv = (np.ones([1, 2*n])*menor)/2
    h, x = bfs(mat, c, h, yv, menor)
    emp, mv, ma = emparelhamento(n, m, h)
    while(not emp):
      menor, yv = atualizaY(n, m, c, menor, yv, mat)
      h, x = bfs(mat, c, h, yv, menor)
      emp, mv, ma = emparelhamento(n, m, h)
      if emp:
        print((ma@c.T).squeeze())
        print(ma.squeeze())
        print(yv)
        return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        main(pth)
    else:
        main(sys.argv[1])
