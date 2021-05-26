# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 01:33:42 2017

@author: miguelrocha
"""

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
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)  
        if d not in self.graph[o]:
            self.graph[o].append(d)

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        return list(self.graph[v])     # needed to avoid list being overwritten of result of the function is used           
             
    def get_predecessors(self, v):
        res = []
        for k in self.graph.keys(): 
            if v in self.graph[k]: 
                res.append(k)
        return res
    
    def get_adjacents(self, v):
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc: 
            if p not in res: res.append(p)
        return res
        
    ## degrees    
    
    def out_degree(self, v):
        return len(self.graph[v])
    
    def in_degree(self, v):
        return len(self.get_predecessors(v))
        
    def degree(self, v):
        return len(self.get_adjacents(v))
        
    def all_degrees(self, deg_type = "inout"):
        ''' Computes the degree (of a given type) for all nodes.
        deg_type can be "in", "out", or "inout" '''
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout":
                degs[v] = len(self.graph[v])
            else: degs[v] = 0
        if deg_type == "in" or deg_type == "inout":
            for v in self.graph.keys():
                for d in self.graph[v]:
                    if deg_type == "in" or v not in self.graph[d]:
                        degs[d] = degs[d] + 1
        return degs
    
    def highest_degrees(self, all_deg= None, deg_type = "inout", top= 10):
        if all_deg is None: 
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()), key=lambda x : x[1], reverse = True)
        return list(map(lambda x:x[0], ord_deg[:top]))
        
    
    ## topological metrics over degrees

    def mean_degree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))
        
    def prob_degree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            if degs[k] in res.keys():
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degs))
        return res    
    
    
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v):
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
        l = [(s,0)]
        visited = [s]
        while len(l) > 0:
            node, dist = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return dist + 1
                elif elem not in visited: 
                    l.append((elem,dist+1))
                    visited.append(elem)
        return None
        
    def shortest_path(self, s, d):
        if s == d: return []
        l = [(s,[])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d: return preds+[node,elem]
                elif elem not in visited: 
                    l.append((elem,preds+[node]))
                    visited.append(elem)
        return None
        
    def reachable_with_dist(self, s):
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res
 
    ## mean distances ignoring unreachable nodes
    def mean_distances(self):
        tot = 0
        num_reachable = 0
        for k in self.graph.keys(): 
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk)
        meandist = float(tot) / num_reachable
        n = len(self.get_nodes())
        return meandist, float(num_reachable)/((n-1)*n)  
    
    def closeness_centrality(self, node):
        dist = self.reachable_with_dist(node)
        if len(dist)==0: return 0.0
        s = 0.0
        for d in dist: s += d[1]
        return len(dist) / s
        
    
    def highest_closeness(self, top = 10): 
        cc = {}
        for k in self.graph.keys():
            cc[k] = self.closeness_centrality(k)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True)
        return list(map(lambda x:x[0], ord_cl[:top]))
            
    
    def betweenness_centrality(self, node):
        total_sp = 0
        sps_with_node = 0
        for s in self.graph.keys(): 
            for t in self.graph.keys(): 
                if s != t and s != node and t != node:
                    sp = self.shortest_path(s, t)
                    if sp is not None:
                        total_sp += 1
                        if node in sp: sps_with_node += 1 
        return sps_with_node / total_sp

    def all_betweenness_centrality(self):
        Bc = {}
        for k in self.graph.keys():
            Bc[k] = self.betweenness_centrality(k)
        ord_cl = sorted(list(Bc.items()), key=lambda x: x[1], reverse=True)
        return list(map(ord_cl))
                    
    
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

    ## clustering
        
    def clustering_coef(self, v):
        adjs = self.get_adjacents(v)
        if len(adjs) <=1: return 0.0
        ligs = 0
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph[i] or i in self.graph[j]: 
                        ligs = ligs + 1
        return float(ligs)/(len(adjs)*(len(adjs)-1))
        
    def all_clustering_coefs(self):
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs
        
    def mean_clustering_coef(self):
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))
            
    def mean_clustering_perdegree(self, deg_type = "inout"):
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}
        for k in degs.keys():
            if degs[k] in degs_k.keys(): degs_k[degs[k]].append(k)
            else: degs_k[degs[k]] = [k]
        ck = {}
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]: tot += ccs[v]
            ck[k] = float(tot) / len(degs_k[k])
        return ck

    ## Hamiltonian

    def check_if_valid_path(self, p):
        if p[0] not in self.graph.keys(): return False
        for i in range(1,len(p)):
            if p[i] not in self.graph.keys() or p[i] not in self.graph[p[i-1]]:
                return False
        return True
        
    def check_if_hamiltonian_path(self, p):
        if not self.check_if_valid_path(p): return False
        to_visit = list(self.get_nodes())
        if len(p) != len(to_visit): return False
        for i in range(len(p)):
            if p[i] in to_visit: to_visit.remove(p[i])
            else: return False
        if not to_visit: return True
        else: return False
    
    def search_hamiltonian_path(self):
        for ke in self.graph.keys():
            p = self.search_hamiltonian_path_from_node(ke)
            if p != None:
                return p
        return None
    
    def search_hamiltonian_path_from_node(self, start):
        current = start
        visited = {start:0}
        path = [start]
        while len(path) < len(self.get_nodes()):
            nxt_index = visited[current]
            if len(self.graph[current]) > nxt_index:
                nxtnode = self.graph[current][nxt_index]
                visited[current] += 1
                if nxtnode not in path:
                    path.append(nxtnode)
                    visited[nxtnode] = 0                    
                    current = nxtnode      
            else: 
                if len(path) > 1: 
                    rmvnode = path.pop()
                    del visited[rmvnode]
                    current = path[-1]
                else: return None
        return path

    # Eulerian

    def check_balanced_node(self,node):  # vai ver se o node é balanceado se o numero de entradas for igual ao numero de saidas
        return self.in_degree(node) == self.out_degree(node)

    def check_balanced_graph(self):  # vai ver se o grafo é balanceado EM TODOS OS NOS
        for n in self.graph.keys():
            if not self.check_balanced_node(n): return False
        return True

    def check_nearly_balanced_graph(self):  # vai encontrar quase um grapho balanceado sendo que pode ocorrer apensas 2 vértices um comuma diferença de in out de 1 e outro com uma de -1
        res = None, None
        for n in self.graph.keys():
            indeg = self.in_degree(n)
            outdeg = self.out_degree(n)
            if indeg - outdeg == 1 and res[1] is None:
                res = res[0], n
            elif indeg - outdeg == -1 and res[0] is None:
                res = n, res[1]
            elif indeg == outdeg:
                pass
            else:
                return None, None
        return res

    def is_connected(self):  # vai ver se todos os vértices do grafo estão conectados a partir de qualquer vértice
        total = len(self.graph.keys()) - 1
        for v in self.graph.keys():
            reachable_v = self.reachable_bfs(v)
            if (len(reachable_v) < total): return False
        return True

    def eulerian_cycle(self):
        from random import randint
        if not self.is_connected() or not self.check_balanced_graph(): return None
        edges_visit = list(self.get_edges()) # Cria uma lista com todos os Nodes-ligação
        vi = edges_visit[randint(0,len(edges_visit)-1)] # escolhe aleatoriamente um node
        res = [vi] #adiciona à lista o node inicial
        edges_visit.pop(edges_visit.index(vi)) #retira da lista de caminho o selecionado (pop list) edges_visit.index(vi), numero do local
        match = False # verificar se existe outros caminhos quando o ciclo terminar
        while edges_visit:
            for i in edges_visit: # correr todos os caminhos existentes
                if i[0] == vi[1]: # verificar se node destino i[0] = node inicial vi[0]
                    vi = i #definir o proximo caminho
                    res.append(vi) #adicionar o novo caminho à lista Node-ligação (o novo vi)
                    edges_visit.pop(edges_visit.index(vi)) #retirar o caminho adicionado
                    break #parar ciclo for
            for h in edges_visit: #edges_visit agora sem o vi
                if vi[1] == h[0]: #verificar se existe outro caminho alternativo
                    match = False # caso exista segue
                    break
                else:
                    match = True
            if match == True and edges_visit != []: #caso existam caminhos (nodes-caminho) restantes e não ocorra match entre caminhos
                for j in edges_visit:
                    for m in res:
                        if j[0] == m[0]: # encontrar caminhos alternativos, j[0](node em falta) == m[0]
                            pos = res.index(m) #verifcar a posição do caminho onde se encontra esse vertice
                            newpath = res[pos:] # reorganizar os caminhos começando naquele com caminhos alternativos
                            newpath.extend(res[:pos]) # adicionar os caminhos que se encontravam antes do caminho selecionado
                            res = newpath # definir a nossa lista de caminhos por aquela reorganizada
                            vi = res[len(res)-1] # definir o nosso novo caminho, sendo esse caminho o ultimo da lista
                            match = False
                            break
        path = [] #lista que vai guardar os primeiros vertices de cada caminho
        for k in res:
            path.append(k[0]) #adiciona o vertice à lista
        path.append(res[-1][1]) #adiciona o vertice final que corresponde ao local onde se iniciou o ciclo
        return path

    def eulerian_path(self):  # vamos criar um eurelian path para um grapho quase balanceado
        unb = self.check_nearly_balanced_graph()
        if unb[0] is None or unb[1] is None: return None
        self.graph[unb[1]].append(unb[0])  # criar um caminho de um vértice ao outro para ficarem balanceados
        cycle = self.eulerian_cycle()
        for i in range(len(cycle) - 1):
            if cycle[i] == unb[1] and cycle[i + 1] == unb[0]:
                break
        path = cycle[i+1:] + cycle[1:i+1]
        return path

    def graph_components(self):
        if not self.is_connected() or not self.check_balanced_graph():
            return None
        edges_visit = list(self.get_edges())  # lista com os arcos do grafo
        res = []  # abrir lista para ciclo
        while edges_visit:  # enquanto o edges_visit tiver elementos(??)
            pair = edges_visit[0]  # primeiro arco
            i = 1  # contagem
            if res != []:  # se o res nao estiver vazio
                while pair[0] not in res[
                    len(res) - 1]:  # se o primeiro arco nao estiver em res (ou seja, nao estiver 'coberto')
                    pair = edges_visit[i]  # vai buscar o arco i
                    i = i + 1  # somar 1 ao i
            edges_visit.remove(pair)  # remover o arco
            start, nxt = pair
            cycle = [start, nxt]
            while nxt != start:  # constroi os varios ciclos
                for suc in self.graph[nxt]:
                    if (nxt, suc) in edges_visit:
                        pair = (nxt, suc)
                        nxt = suc
                        cycle.append(nxt)
                        edges_visit.remove(pair)
            res.append(cycle)
        return res

    def graph_components_cenas(self):
        components = self.graph_components()
        organizes_components = sorted(components, key=len, reverse=True)
        for i in organizes_components:
            m = tries_DeBruijn(i)
            if m == None:
                pass
            else:
                return m

def is_in_tuple_list(tl, val):
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
    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print (gr.reachable_with_dist(1))
    print (gr.reachable_with_dist(3))

    
    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
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

def test6():
    gr = MyGraph()
    gr.add_vertex(1)
    gr.add_vertex(2)
    gr.add_vertex(3)
    gr.add_vertex(4)
    gr.add_edge(1,2)
    gr.add_edge(2,3)
    gr.add_edge(3,2)
    gr.add_edge(3,4)
    gr.add_edge(4,2)
    gr.print_graph()
    print(gr.size())
    
    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))
    
    print(gr.all_degrees("inout"))
    print(gr.all_degrees("in"))
    print(gr.all_degrees("out"))
    
    gr2 = MyGraph({1:[2,3,4], 2:[5,6],3:[6,8],4:[8],5:[7],6:[],7:[],8:[]})
    print(gr2.reachable_bfs(1))
    print(gr2.reachable_dfs(1))
    
    print(gr2.distance(1,7))
    print(gr2.shortest_path(1,7))
    print(gr2.distance(1,8))
    print(gr2.shortest_path(1,8))
    print(gr2.distance(6,1))
    print(gr2.shortest_path(6,1))
    
    print(gr2.reachable_with_dist(1))
    
    print(gr.has_cycle())
    print(gr2.has_cycle())
    
    print(gr.mean_degree())
    print(gr.prob_degree())
    print(gr.mean_distances())
    print (gr.clustering_coef(1))
    print (gr.clustering_coef(2))

if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()
    #test5()
    #test6()
    
    
