# -*- coding: utf-8 -*-


class Automata:

    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)

    def buildTransitionTable(self, pattern):
        for q in range(self.numstates):
            for a in self.alphabet:
                prefixo = pattern[:q] + a
                p = overlap(prefixo, pattern)
                self.transitionTable[(q, a)] = p  # p - posição no padrao    q - posição na sequencia

    def printAutomata(self):  # imprime a informação da classe
        print("States: ", self.numstates)
        print("Alphabet: ", self.alphabet)
        print("Transition table:")
        for k in self.transitionTable.keys():
            print(k[0], ",", k[1], " -> ", self.transitionTable[k])

    def nextState(self, current, symbol):
        return self.transitionTable[(current, symbol)]

    def applySeq(self, seq):
        q = 0
        res = [q]
        for c in seq:
            q = self.nextState(q, c)
            res.append(q)
        return res

    def occurencesPattern(self, text):
        q = 0
        res = []
        for i in range(len(text)):
            q = self.nextState(q, text[i])  # correr o nextstate
            if q == self.numstates - 1: res.append(i - self.numstates + 2)  # 2 e um para ter o espaço que adicionamos(inicio do state) mais ter o comprimento da sequencia
        return res  # a lista é as posiçoes onde se encontram os padroes


def overlap(s1, s2):
    maxov = min(len(s1), len(s2))
    for i in range(maxov, 0, -1):
        if s1[-i:] == s2[:i]: return i
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



