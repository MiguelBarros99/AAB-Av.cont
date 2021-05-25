# -*- coding: utf-8 -*-

class SuffixTree:  #construtir arvore apartir dea sequencia

    def __init__(self):
        self.nodes = {0: (-1, {})}  # root node
        self.num = 0

    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0: print(k, "->", self.nodes[k][1])
            else: print(k, ":", self.nodes[k][0])

    def add_node(self, origin, symbol, leafnum=-1):
        self.num += 1  # numero de nodulo adiciona
        self.nodes[origin][1][symbol] = self.num  # 1 é para ir buscar o dicionario dentro do tuplo
        self.nodes[self.num] = (leafnum, {})  # constroi tuplo para o node seguinte

    def add_suffix(self, p, sufnum):  # o -padrao , sufnum - i
        pos = 0
        node = 0
        while pos < len(p):  # seguir a sequencia no ciclo pos
            if p[pos] not in self.nodes[node][1].keys():  # se a letra na posição pos da seq p não tiver no dicionario no node
                if pos == len(p) - 1:
                    self.add_node(node, p[pos], sufnum)  # adiciona o node final/leaf se for o $. sufnum é o index i na seq original
                else:
                    self.add_node(node, p[pos])  # adicionar ao node a letra p[pos]
            node = self.nodes[node][1][p[pos]]  # mudar de node, output é um numero
            pos += 1  # avança uma posição

    def suffix_tree_from_seq(self, text):
        t = text + "$"  # adiciona dollar á seq
        for i in range(len(t)):
            self.add_suffix(t[i:], i)  # range para passar a seq de i ao fim e apartir de que posição foi passada

    def find_pattern(self, pattern):
        node = 0
        for pos in range(len(pattern)): #seguir as posições no padrao a pesquisa pela arvore
            if pattern[pos] in self.nodes[node][1].keys():  # se a letra tiver nas keys
                node = self.nodes[node][1][pattern[pos]]  # seguir para o proximo node
            else:  # mal de missmatch da return de none para esse padrão
                return None
        return self.get_leafes_below(node)

    def get_leafes_below(self, node):
        res = []
        if self.nodes[node][0] >= 0:  # maior ou igual 0 é para verificar se é uma leaf
            res.append(self.nodes[node][0])  # adicionar o valor da leaf
        else:
            for k in self.nodes[node][1].keys():  # correr todas as keys no nodulo
                newnode = self.nodes[node][1][k]  # mudar para o node
                leafes = self.get_leafes_below(newnode)  # recursividade para seguir os ramos ate leaf
                res.extend(leafes)  # concatenar a lista da recursiva (pode ter varias leafs)
        return res

    def nodes_below(self, node):
        """Ficha exercicio 1 A"""
        nodes = list(self.nodes[node][1].values())  # vai buscar os valores do dicionario dos nodulos a seguir
        if nodes != []:
            for i in nodes: nodes.extend(list(self.nodes[i][1].values()))  # a lista vai aumentando (acrescenta a lista) conforme ele corre os nodulos
            return nodes
        else: # se o nodes for vazio
            return None

    def matches_prefix(self, prefix):
        """Ficha exercicio 1 B"""
        res = []
        pos = self.find_pattern(prefix)  # local onde é encontrado o sufixo
        orig = self.get_sequence()  # sequencia original
        if pos != [] or None:
            for i in pos:
                hipoteses = len(orig) - i  # numero de hipoteses (compriemnto maximo)
                dist = len(prefix)
                while dist <= hipoteses:  # distâncias
                    if orig[i:i + dist] not in res:
                        res.append(orig[i:i + dist])
                    dist += 1
        return res

    def get_sequence(self):
        """Funçao suporte a matches_prefix, obter a sequencia original de inicio da arvore"""
        sequence = ''
        m = self.nodes[0][1].keys()  # nodulo da root
        for i in m:
            if self.nodes[0][1][i] == 1:  # buscar a primeira letra
                node = self.nodes[0][1][i]
                sequence += i
        p = 1
        while p != 0:  # começar while para construir o sequencia
            m = self.nodes[node][1].keys()  # obter keys
            for letra in m:
                dic = self.nodes[node][1]  # ir buscar dicionario para o node em questao
                if dic.get(letra) == node + 1:  # verificar para a letra do node se segue a ordem de ser a primeira.
                    node = self.nodes[node][1][letra]  # seguir para o proximo nodulo
                    sequence += letra
                    if self.nodes[node][0] != -1:  # se for o esterisco e se o proximo nodulo é uma leaf
                        p = 0
        return sequence[:len(sequence) - 1]  # devolver a seq final a retirar o $ ou #


def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    # print (st.find_pattern("TA"))
    # print (st.find_pattern("ACG"))


def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    # print(st.get_sequence())
    print(st.nodes)
    # print (st.find_pattern("TA"))
    # print(st.repeats(2,2))
    print(st.matches_prefix("TA"))


test()
print()
test2()
