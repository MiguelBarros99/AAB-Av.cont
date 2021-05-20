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
        self.graph = g  #unico atributo (g = dicionario)  

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():#para cada key no dicionario (vertice)
            print (v, " -> ", self.graph[v])#para cada key no dicionario (vertice)

    ## get basic info

    def get_nodes(self):#vai buscar os vetices(nos)
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())#devolve uma lista com os vertices
        
    def get_edges(self): #buscar as arestas(pares de vertices, ou seja, uma aresta liga dois vertices)
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():#para cada key v
            for d in self.graph[v]:#para cada value de v
                edges.append((v,d))#acrescentar a lista as arestas (vertice v que se ligou ao vertice x)
        return edges#devolver a lista
      
    def size(self):##tamanho do grafo
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())#usa o get_nodes e o get_edges para ter o tamanho do grafo
      
    ## add nodes and edges    
    
    def add_vertex(self, v):#adicionar vertice(no)
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = []#adicionar uma key ao dicitionary
        
    def add_edge(self, o, d):#(o,d) vertices
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys():#confirmar se os vertices o e d nao estao no dicionario
            self.add_vertex(o) #adicionar vertice o
        if d not in self.graph.keys():
            self.add_vertex(d) #adicionar vertice d
        if d not in self.graph[o]:#confirmar se d e um value de o
            self.graph[o].append(d) #adicionar o value d ao o

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        return list(self.graph[v])     # needed to avoid list being overwritten of result of the function is used           
             
    def get_predecessors(self, v):
        pre = []#abrir lista de antecessor
        for k in self.graph.keys(): #percorrer as keys do dicionario
            if v in self.graph[k]: #OU if self.graph[i]==v:  #verificar se v e um value de i
                pre.append(k)#adicionar a key com value v a lista
        return pre #retornar a lista com os antecessor 
    
    def get_adjacents(self, v):
        '''Da lista de vertices(nos) adjacentes do vertice(no) v ->dois vertices sao adjacentes se um e sucessor do outro'''
        suc = self.get_successors(v)#buscar os sucessores de v
        pred = self.get_predecessors(v)#buscar os antecessor de v
        res = pred#res e igual a lista de antecessores (podia ser ao contrario)
        for p in suc: #percorrer a lista de sucessores
            if p not in res: #verificar se nao esta na lista
                res.append(p)#adicionar todos os sucessores de v a lista de antecessores se nao estiver na lista
        return res#retornar res 
        
    ## degrees    
    
    def out_degree(self, v):#calcula grau de saída do vertice(no) v
        #self.get_successors(v) -> lista de todos os arcos que saiem do vertice v
        return len(self.graph[v])#contagem de todos os arcos que saiem do vertice v
    
    def in_degree(self, v):#calcula grau de entrada do vertice(no) v
        #self.get_predecessors(v) -> lista de todos os arcos que entram do vertice v
        return len(self.get_predecessors(v))
        
    def degree(self, v):#O grau de um vértice e dado pelo numero de arestas que lhe sao incidentes
        #self.get_adjacents(v) -> ver os sucessores e os predecessores para dar lsita de arestas
        return len(self.get_adjacents(v))#contar as arestas da lista
        
    def all_degrees(self, deg_type = "inout"):#tudo o que sai e tudo o que entra
        ''' Cálculo de graus de entrada e saída (ou ambos) para todos os nós da rede.
        deg_type can be "in", "out", or "inout" '''
        degs = {}
        for v in self.graph.keys():#para cada key no grafo
            if deg_type == "out" or deg_type == "inout":#se for graus de saida ou de entrada e saida
                degs[v] = len(self.graph[v])#inicializar o número do dicionario com o valor de graus de saida
            else: degs[v] = 0
        if deg_type == "in" or deg_type == "inout":#se for graus de entrada ou de entrada e saida
            for v in self.graph.keys():#para cada key (metabolito ou reação) no grafo
                for d in self.graph[v]:#para cada value de v
                    if deg_type == "in" or v not in self.graph[d]:#se for in ou v, não for um value de d no grafo
                        degs[d] = degs[d] + 1 #adicionar + 1 ao value de d no dicionario degs
        return degs
    
    def highest_degrees(self, all_deg= None, deg_type = "inout", top= 10):#vai ver o top 10
        '''Vai buscar o top 10 de nos com maior grau'''
        if all_deg is None: #percorrer todos graus
            all_deg = self.all_degrees(deg_type)#ir buscar o dicionario a all_degrees
        ord_deg = sorted(list(all_deg.items()), key=lambda x : x[1], reverse = True)#por por ordem o dicionario do mais pequeno para o maior, neste caso trasnforma em lista .items para por em tuplo (key,value) so assim consegue por por ordem
        #por por ordem os graus
        return list(map(lambda x:x[0], ord_deg[:top]))#retorna uma lista com os nos com os 10 primeiros
        #x[0]-> key; x[1]-> values
    
    ## topological metrics over degrees

    def mean_degree(self, deg_type = "inout"):#media dos graus
        degs = self.all_degrees(deg_type)#calculo dos graus de entrada e saída 8ou ambos) para todos os nós da rede
        return sum(degs.values()) / float(len(degs))#soma de todos os valores do dicionario e fazer a media de nos do grafico
        
    def prob_degree(self, deg_type = "inout"):#probabilidade desse grau existir no grafo
        '''Para cada grau quantos nós é que tenho'''
        degs = self.all_degrees(deg_type)#calculo dos graus de entrada e saída 8ou ambos) para todos os nós da rede
        res = {}#abrir dicionario
        for k in degs.keys():#percorrer todas as keys de degs
            if degs[k] in res.keys():#ver se tem um determinado k nas keys de res
                res[degs[k]] += 1 #adicionar esse k + 1 ao dicionario res
            else:#caso contrario
                res[degs[k]] = 1#adicionar ao dicionario esse k(grau) = 1
        for k in res.keys():
            res[k] /= float(len(degs))#probabilidade dos graus
        return res    
    
    
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
        if s == d: return 0
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
        #na primeira iteracao faz o for logo
        res = []
        l = [(s,0)] #lista com tuplo com s e a distancia de s a s (0)
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: 
                res.append((node,dist))# nao conta o s
            for elem in self.graph[node]:#vai ver onde e que o node s se esta a ligar
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): #vai ver se o p se encontra dentro de l ou em res
                    l.append((elem,dist+1))#adiciona o vertice a que se liga
        return res
 
    ## mean distances ignoring unreachable nodes
    def mean_distances(self):
        tot = 0 #total
        num_reachable = 0 #numero de vetores ligados entre si
        for k in self.graph.keys(): 
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk)#contagem de todas as ligacoes existentes entre todos os nos
        meandist = float(tot) / num_reachable #media de distancia de ligacao
        n = len(self.get_nodes()) #contagem de todos os nos que tem
        return meandist, float(num_reachable)/((n-1)*n) #num_reachable-> numero de ligacoes que existem / (n-1)*n) -> nº de ligacoes esperadas
    
    def closeness_centrality(self, node):#node = s
        '''Baseado nos nos que estao mais proximos dos restantes '''
        dist = self.reachable_with_dist(node) #uma lista que devolve os nos e as distancias que esse no tem desses nos
        if len(dist)==0: 
            return 0.0 #centralidade mais proxima e 0
        s = 0.0 #distancia
        for d in dist: #d = ( , )
            s += d[1] #tuplo (t,6)
        return len(dist) / s #todos os nos a dividir pela distancia total
        #Centralidade mais proxima = todos os tuplos (vertice com ligacao a esse vertice)/distancia total
    
    def highest_closeness(self, top = 10):
        '''Centralidade mais alta -> top 10'''
        cc = {} #abrir o dicionario com todas as keys do grafo e a centralidade mais proxima
        for k in self.graph.keys():#para todas as keys no grafo
            cc[k] = self.closeness_centrality(k)# o value de k = a centralidade mais proxima da key do grafo
        print(cc)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True) #ordenar o dicionario em ordem a centralidade mais proxima(transformar em lista)
        return list(map(lambda x:x[0], ord_cl[:top])) #retornar os vertices com o top 10
            
    
    def betweenness_centrality(self, node):
        '''Soma de todas as distancia possiveis '''
        total_sp = 0 #todos os caminhos curtos que existem
        sps_with_node = 0 #caminhos curtos que passam pelo node
        for s in self.graph.keys(): 
            for t in self.graph.keys():
                if s != t and s != node and t != node:
                    sp = self.shortest_path(s, t)#retorna os nodes entre s a t no caminho + curto
                    if sp is not None:# ou seja, se existir um caminho
                        total_sp += 1 #somar 1 aos caminhos todos que existem
                        if node in sp: #adicionar 1 se o node estiver no caminho entre s e t
                            sps_with_node += 1 #
        return sps_with_node / total_sp #caminhos que passam pelo node/ caminhos totais

    def highest_betweenness(self, top = 10):
        '''Centralidade mais alta -> top 10'''
        cc = {} #abrir o dicionario com todas as keys do grafo e a betweenness_centrality
        for k in self.graph.keys():#para todas as keys no grafo
            cc[k] = self.betweenness_centrality(k)# o value de k = a cbetweenness_centrality da key do grafo
        print(cc)
        ord_cl = sorted(list(cc.items()), key=lambda x : x[1], reverse = True) #ordenar o dicionario em ordem da betweenness_centrality (transformar em lista)
        return list(map(lambda x:x[0], ord_cl[:top])) #retornar os vertices com o top 10
    
    def centralidade_de_grau_vertice(self,v):
        '''A centralidade de grau de um vertice e dada pelo seu grau'''
        alldegree = self.all_degrees()
        return(alldegree[v]) #vai buscar o grau do vertice v
                    
    
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
        
    def clustering_coef(self, v):#nova função
        adjs = self.get_adjacents(v)
        if len(adjs) <=1: return 0.0
        ligs = 0
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph[i] or i in self.graph[j]: 
                        ligs = ligs + 1
        return float(ligs)/(len(adjs)*(len(adjs)-1))
        
    def all_clustering_coefs(self):#nova função
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs
        
    def mean_clustering_coef(self):#nova função
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))
            
    def mean_clustering_perdegree(self, deg_type = "inout"):#nova função
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

def is_in_tuple_list(tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res

    
if __name__ == "__main__":
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

