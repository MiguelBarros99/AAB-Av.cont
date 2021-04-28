# -*- coding: utf-8 -*-

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g    

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d))
        return edges
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    
    
    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []
        
    def add_edge(self, o, d):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys():#verifica se ha o vertice o senao adiciona ao dicionario
            self.add_vertex(o)
        if d not in self.graph.keys():#verifica se ha d vertice o senao adiciona ao dicionario
            self.add_vertex(d)
        if d not in self.graph[o]:
            #verifica se ha ligação entre os dois vertices, caso contrario adiciona o vertice d à lista do vertice o
            self.graph[o].append(d)

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        return list(self.graph[v])     # needed to avoid list being overwritten of result of the function is used

    def get_predecessors(self, v):
        lista = []
        for i in self.graph.keys():
            if v in self.graph[i]:
                lista.append(i)
        return lista

    def get_adjacents(self, v):
        suc = self.get_successors(v) #buscar os sucessores
        pred = self.get_predecessors(v) #buscar os predecessores
        res = pred
        for p in suc: #adcionar os sucessores não presentes na lista
            if p not in res:
                res.append(p)
        return res

    ## degrees    
    
    def out_degree(self, v):
        li = self.get_successors(v)
        return len(li)

    def in_degree(self, v):
        li = self.get_predecessors(v)
        return len(li)

    def degree(self, v):
        li = self.get_adjacents(v)
        return len(li)
    
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v):
        l = [v] #sitio onde tou a começar, lista de coisas a começar, ou seja começa pelo no de origem
        res = [] #a lista do resultado de nos atingiveis
        while len(l) > 0: #enquanto ha elementos na lista l (lista de queue)
            node = l.pop(0) #isolar o 1º no na queue
            if node != v: #se o v não entra na lista de nos acessiveis e for diferente é adiciona a lista
                res.append(node) #controi o resultado sempre a colocar no fim, ou seja os primeiros ficam para ultimo
            for elem in self.graph[node]: #correr os nos no node a pesquisar
                if elem not in res and elem not in l and elem != node: #adicionar á queue
                    l.append(elem)
        return res
        
    def reachable_dfs(self, v):
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
        else:
            l = [(s,0)]  # sitio onde tou a começar, lista de coisas a começar, ou seja começa pelo no de origem
            vis = [s]  # a lista do resultado de nos atingiveis
            while len(l) > 0 :  # enquanto ha elementos na lista l (lista de queue)
                node,dist = l.pop(0)  # isolar o 1º no na queue
                for elem in self.graph[node]:  # correr os nos no node a pesquisar
                    if elem == d:
                        return dist + 1
                    if elem not in vis and elem not in l and elem != node:  # adicionar á queue
                        l.append((elem,dist + 1))
                        vis.append(node)
            return None
        
    def shortest_path(self, s, d):
        if s == d: return [s,d]
        else:
            l = [(s,[])]  # sitio onde tou a começar, lista de coisas a começar, ou seja começa pelo no de origem
            vis = [s]  # a lista do resultado de nos atingiveis
            while len(l) > 0:  # enquanto ha elementos na lista l (lista de queue)
                node, preds = l.pop(0)  # isolar o 1º no na queue
                for elem in self.graph[node]:  # correr os nos no node a pesquisar
                    if elem == d:
                        return preds + [(node, elem)]
                    if elem not in vis and elem not in l and elem != node:  # adicionar á queue
                        l.append((elem, preds + [(node,elem)]))
                        vis.append(node)
            return None
        
    def reachable_with_dist(self, s): #travessia total do grafo mas com as distancias associadas, faz a travessia sobre todos os pontos
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): #juntar sempre a distancia ao registro dos elementos nos grafos
                    l.append((elem,dist+1))
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
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )  #criar o grafo
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
    #test1()
    #test2()
    #test3()
    test4()
    #test5()
