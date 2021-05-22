# -*- coding: utf-8 -*-

class BoyerMoore:

    def __init__(self, alphabet, pattern):
        self.alphabet = alphabet
        self.pattern = pattern
        self.preprocess()

    def preprocess(self):
        self.process_bcr()
        self.process_gsr()

    def process_bcr(self):
        """Bad Caracter rule"""
        self.occ = {}  # abrir um dicionario
        for c in self.alphabet:  # adiciona ao dicionario todas as letras do alphabeto com valor -1
            self.occ[c] = -1
        for i in range(len(self.pattern)):
            c = self.pattern[i]  # altera no dicionario a letra no pattern para valor de i
            self.occ[c] = i

    def process_gsr(self):
        """Good Sufix rule"""
        self.f = [0] * (len(self.pattern) + 1)  # abrir uma lista com o 0 com o tamanho do pattern
        self.s = [0] * (len(self.pattern) + 1)
        i = len(self.pattern)
        j = len(self.pattern) + 1  # define o i e j como pelo comprimento do padrão
        self.f[i] = j  # altera o ultimo elemento da lista f para o valor de f
        while i > 0:
            while j <= len(self.pattern) and self.pattern[i - 1] != self.pattern[j - 1]:  # vai definir lista s, em S que significa o numero de casas que podesse avançar caso não encaixe no pattern
                if self.s[j] == 0:
                    self.s[j] = j - i
                j = self.f[j]
            i -= 1
            j -= 1
            self.f[i] = j
        j = self.f[0]
        for i in range(
                len(self.pattern)):  # quando ta definido como 0 alterar para o valor de  j mais recente que significa passar o restante da cadeia.
            if self.s[i] == 0: self.s[i] = j
            if i == j: j = self.f[j]

    def search_pattern(self, text):
        res = []
        i = 0  # POSIÇÃO NA SEQ INICIAL
        while i <= (len(text) - len(self.pattern)):  # para começar a correr a sequencia
            j = len(self.pattern) - 1
            while j >= 0 and self.pattern[j] == text[j + i]:  # continuar a correr enquanto esta a dar match
                j -= 1
            if j < 0:
                res.append(i)
                i = i + self.s[0]  # avançar para i "casas" para a frente como j<0 significa que deu match com um padrão
            else:
                c = text[i + j]
                i += max(self.s[j + 1], j - self.occ[c])  # avançar uma sequencia dependo do GSR e BCR
        return res


def test():
    bm = BoyerMoore("ACTG", "ACCA")
    print(bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))


test()

# result: [5, 13, 23, 37]

