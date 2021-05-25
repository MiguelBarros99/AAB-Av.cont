# -*- coding: utf-8 -*-

class Trie:  #construtir arvore apartir de padroes

    def __init__(self):
        self.nodes = {0: {}}  # dictionary
        self.num = 0

    def print_trie(self):
        for k in self.nodes.keys():
            print(k, "->", self.nodes[k])

    def add_node(self, origin, symbol):
        self.num += 1  # adicionar o numero do nodulo, adiciona sempre um que corre
        self.nodes[origin][symbol] = self.num  # adicionar a info ao node
        self.nodes[self.num] = {}  # abre o nome nodulo

    def add_pattern(self, p):  # p -> padrão, inicia sempre apartir da root
        pos = 0  # posição
        node = 0  # node
        while pos < len(p):
            if p[pos] not in self.nodes[node].keys():  # verifica a presença da letra(nucleotido) no node a ser chamado
                self.add_node(node, p[pos])  # self.add_note para adicionar
            node = self.nodes[node][p[pos]]  # o node que tem a letras atraves do dicionario
            pos += 1

    def trie_from_patterns(self, pats):
        for p in pats:  # um padrão da lista de padrões
            self.add_pattern(p)

    def prefix_trie_match(self, text):  # começa da posiçao 0
        pos = 0
        match = ""  # resultado
        node = 0
        while pos < len(text):
            if text[pos] in self.nodes[node].keys():
                node = self.nodes[node][text[pos]]  # passar para o proximo node _ output é um numero
                match += text[pos]  #adicionar a solução
                if self.nodes[node] == {}: #atingiu uma leaf e so da return a match nesse caso
                    return match
                else:
                    pos += 1 #seguir para a proxima posição
            else:  # senao tiver corre o ciclo e devolve none
                return None
        return None

    def trie_matches(self, text):  #tentar varias posições da seq
        res = []
        for i in range(len(text)):  # i vai ser a posição na sequencia text
            m = self.prefix_trie_match(text[i:])
            if m != None: res.append((i, m))  #posição da sequencia que começou e m-> o match que foi dado
        return res


def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()  # chamar a classe
    t.trie_from_patterns(patterns)
    t.print_trie()


def test2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    print(t.nodes)
    print(t.prefix_trie_match("GAGATCCTA"))
    print(t.trie_matches("GAGATCCTA"))


# test()
# print()
test2()