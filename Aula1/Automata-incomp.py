# -*- coding: utf-8 -*-


class Automata:  #automatos finitos

    def __init__(self, alphabet, pattern):    #alfabeto e padrão
        self.numstates = len(pattern) + 1  #tamanho do padrão + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)

    def buildTransitionTable(self, pattern):
        for q in range(self.numstates):  #range no numero de estados
            for a in self.alphabet:  #para cada letra do alfabeto
                prefixo = pattern[:q] + a  #padrao ate posição q +  posivel letra do alfabeto
                p = overlap(prefixo, pattern)
                self.transitionTable[(q, a)] = p  # p - Estado posisivel a avançar    q - posição no padrão

    def printAutomata(self):  # imprime a informação da classe
        print("States: ", self.numstates)
        print("Alphabet: ", self.alphabet)
        print("Transition table:")
        for k in self.transitionTable.keys():
            print(k[0], ",", k[1], " -> ", self.transitionTable[k])

    def nextState(self, current, symbol):
        return self.transitionTable[(current, symbol)]  #da o estado para qual avançar

    def applySeq(self, seq):
        q = 0  #estadio 0
        res = [q]
        for c in seq:
            q = self.nextState(q, c)  #q vai mudando conforme corre a seq, indo o next state buscar a info a tabela
            res.append(q)  #append do estado atual à tabela
        return res

    def occurencesPattern(self, text):
        q = 0
        res = []
        for i in range(len(text)):
            q = self.nextState(q, text[i])  # correr o nextstate q é o estado atual e se q = numero de estados
            if q == self.numstates - 1: res.append(i - self.numstates + 2)  # 2 e um para ter o espaço que adicionamos(inicio do state) mais ter o comprimento da sequencia
        return res  # a lista é as posiçoes onde se encontram os padroes


def overlap(s1, s2):
    maxov = min(len(s1), len(s2))  #maximo de overlap
    for i in range(maxov, 0, -1):   #do maxima até 0
        if s1[-i:] == s2[:i]: return i  #devolve o numero de overlap
    return 0


def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print(auto.applySeq("CACAACAA"))  # lista com sequencias posição do padrao na sequencia
    print(auto.occurencesPattern("CACAACAA"))  # local de ocorrencia do padrao completo


test()

#States:  4
#Alphabet:  AC
#Transition table:
#0 , A  ->  1
#0 , C  ->  0
#1 , A  ->  1
#1 , C  ->  2
#2 , A  ->  3
#2 , C  ->  0
#3 , A  ->  1
#3 , C  ->  2
#[0, 0, 1, 2, 3, 1, 2, 3, 1]
#[1, 4]



