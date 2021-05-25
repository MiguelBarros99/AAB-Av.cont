# -*- coding: utf-8 -*-

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:

    def __init__(self, g={}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g  # unico atributo (g = dicionario)

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():  # para cada key no dicionario (vertice)
            print(v, " -> ", self.graph[v])  # para cada key no dicionario (vertice)

    def get_nodes(self):  # vai buscar os vetices(nos)
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())  # devolve uma lista com os vertices

    def get_edges(self):  # buscar as arestas(pares de vertices, ou seja, uma aresta liga dois vertices)
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():  # para cada key v
            for d in self.graph[v]:  # para cada value de v
                edges.append((v, d))  # acrescentar a lista as arestas (vertice v que se ligou ao vertice x)
        return edges  # devolver a lista

    def size(self):  ##tamanho do grafo
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())  # usa o get_nodes e o get_edges para ter o tamanho do grafo

    ## add nodes and edges

    def add_vertex(self, v):  # adicionar vertice(no)
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []  # adicionar uma key ao dicitionary

    def add_edge(self, o, d):  # (o,d) vertices
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph '''
        if o not in self.graph.keys():  # confirmar se os vertices o e d nao estao no dicionario
            self.add_vertex(o)  # adicionar vertice o
        if d not in self.graph.keys():
            self.add_vertex(d)  # adicionar vertice d
        if d not in self.graph[o]:  # confirmar se d e um value de o
            self.graph[o].append(d)  # adicionar o value d ao o

    ## successors, predecessors, adjacent nodes

    def get_successors(self, v):
        return list(
            self.graph[v])  # needed to avoid list being overwritten of result of the function is used

    def get_predecessors(self, v):
        pre = []  # abrir lista de antecessor
        for k in self.graph.keys():  # percorrer as keys do dicionario
            if v in self.graph[k]:  # OU if self.graph[i]==v:  #verificar se v e um value de i
                pre.append(k)  # adicionar a key com value v a lista
        return pre  # retornar a lista com os antecessor

    def get_adjacents(self, v):
        '''Da lista de vertices(nos) adjacentes do vertice(no) v ->dois vertices sao adjacentes se um e sucessor do outro'''
        suc = self.get_successors(v)  # buscar os sucessores de v
        pred = self.get_predecessors(v)  # buscar os antecessor de v
        res = pred  # res e igual a lista de antecessores (podia ser ao contrario)
        for p in suc:  # percorrer a lista de sucessores
            if p not in res:  # verificar se nao esta na lista
                res.append(p)  # adicionar todos os sucessores de v a lista de antecessores se nao estiver na lista
        return res  # retornar res

    ## degrees

    def out_degree(self, v):  # calcula grau de saída do vertice(no) v
        # self.get_successors(v) -> lista de todos os arcos que saiem do vertice v
        return len(self.graph[v])  # contagem de todos os arcos que saiem do vertice v

    def in_degree(self, v):  # calcula grau de entrada do vertice(no) v
        # self.get_predecessors(v) -> lista de todos os arcos que entram do vertice v
        return len(self.get_predecessors(v))

    def degree(self, v):  # O grau de um vértice e dado pelo numero de arestas que lhe sao incidentes
        # self.get_adjacents(v) -> ver os sucessores e os predecessores para dar lsita de arestas
        return len(self.get_adjacents(v))  # contar as arestas da lista

    def all_degrees(self, deg_type="inout"):  # tudo o que sai e tudo o que entra
        ''' Cálculo de graus de entrada e saída (ou ambos) para todos os nós da rede.
        deg_type can be "in", "out", or "inout" '''
        degs = {}
        for v in self.graph.keys():  # para cada key no grafo
            if deg_type == "out" or deg_type == "inout":  # se for graus de saida ou de entrada e saida
                degs[v] = len(self.graph[v])  # inicializar o número do dicionario com o valor de graus de saida
            else:
                degs[v] = 0
        if deg_type == "in" or deg_type == "inout":  # se for graus de entrada ou de entrada e saida
            for v in self.graph.keys():  # para cada key (metabolito ou reação) no grafo
                for d in self.graph[v]:  # para cada value de v
                    if deg_type == "in" or v not in self.graph[d]:  # se for in ou v, não for um value de d no grafo
                        degs[d] = degs[d] + 1  # adicionar + 1 ao value de d no dicionario degs
        return degs

    ## BFS and DFS searches

    def reachable_bfs(self, v):
        '''de cima para baixo'''
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res

    def reachable_dfs(self, v):
        '''da esqueda para a direita'''
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res

    def distance(self, s, d):
        if s == d: return 0
        l = [(s, 0)]
        visited = [s]
        while len(l) > 0:
            node, dist = l.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return dist + 1
                elif elem not in visited:
                    l.append((elem, dist + 1))
                    visited.append(elem)
        return None

    def shortest_path(self, s, d):
        if s == d: return 0
        l = [(s, [])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return preds + [node, elem]
                elif elem not in visited:
                    l.append((elem, preds + [node]))
                    visited.append(elem)
        return None

    def reachable_with_dist(self, s):
        # na primeira iteracao faz o for logo
        res = []
        l = [(s, 0)]  # lista com tuplo com s e a distancia de s a s (0)
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s:
                res.append((node, dist))  # nao conta o s
            for elem in self.graph[node]:  # vai ver onde e que o node s se esta a ligar
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res,
                                                                          elem):  # vai ver se o p se encontra dentro de l ou em res
                    l.append((elem, dist + 1))  # adiciona o vertice a que se liga
        return res

## cycles
    def node_has_cycle (self, v):
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res


def is_in_tuple_list (tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res


def test1():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print (gr.get_nodes())
    print (gr.get_edges())
    

def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()

    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))

def test4():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    
    print (gr.distance(1,4))
    print (gr.distance(4,3))

    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print (gr.reachable_with_dist(1))
    print (gr.reachable_with_dist(3))

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    
    print (gr2.distance(2,1))
    print (gr2.distance(1,5))
    
    print (gr2.shortest_path(1,5))
    print (gr2.shortest_path(2,1))

    print (gr2.reachable_with_dist(1))
    print (gr2.reachable_with_dist(5))

def test5():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.node_has_cycle(2))
    print (gr. node_has_cycle(1))
    print (gr.has_cycle())

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2. node_has_cycle(1))
    print (gr2.has_cycle())


if __name__ == "__main__":
    test1()
    #test2()
    #test3()
    #test4()
    #test5()
