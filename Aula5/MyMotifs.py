# -*- coding: utf-8 -*-
"""
@author: miguelrocha
"""


def createMatZeros(nl,nc):  # matriz de 0, com o temanho de nl * nc
    res = []
    for i in range(0, nl):
        res.append([0] * nc)
    return res


def printMat(mat):  # função responsável por dar print a matriz
    for i in range(0, len(mat)): print(mat[i])


class MyMotifs:
    def __init__(self, seqs):  #  lista de seq
        self.size = len(seqs[0])  # comprimentos de caractares das seq
        self.seqs = seqs  # lista de motif
        self.alphabet = seqs[0].alfabeto()  # alfabeto
        self.doCounts()  # matriz de contagens das letras entre as seqs
        self.createPWM()  # matriz de PWM, que é a matriz de probabilidades

    def __len__(self):  # return do comprimento das seqs
        return self.size

    def doCounts(self):  # cria as matrizes de contagens
        self.counts = createMatZeros(len(self.alphabet), self.size)  #alfabeto das linhas, tamanho na coluna
        for s in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(s[i]) #indexar qual é a ordem do carater no alfabeto
                self.counts[lin][i] += 1 #adicionar 1 a essa celula da matriz

    def createPWM(self):  # cria a mtriz de probabilidades
        if self.counts == None: self.doCounts()  #contagens se não tiver ja sido feito
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)  #pwm = contagens verificadas / numero de seqs (numero total de casas que la ha )

    def consensus(self):  # obter consensus na matriz dos counts por coluna
        res = ""
        for j in range(self.size): #correr a seqeuncia
            maxcol = self.counts[0][j] #primeira letra do alfabeto
            maxcoli = 0
            for i in range(1, len(self.alphabet)): #correr todas as letras do alfabeto
                if self.counts[i][j] > maxcol: #se contragem for superior alterar
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]  #append a string
        return res

    def maskedConsensus(self):  # obtem o masked consensus,consensus só com as letras que tem uma incidência maior do que 50%
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol:
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2: #apenas se tiver + que 50% leva append a res
                res += self.alphabet[maxcoli]
            else: #senão leva append de -
                res += "-"
        return res

    def probabSeq(self, seq):  # probabilidade de a seq ter o motif
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]  #operação de multiplicação
        return res

    def probAllPositions(self,seq):  # este em vez de calcular a probabilidade de acontecer devolve uma lista com as probabilidades de acontecer em cada letra da seq
        res = []
        for k in range(len(seq) - self.size + 1): #correr asequencia toda
            res.append(self.probabSeq(seq))  #guardar os scores
        return res

    def mostProbableSeq(self,seq):  #seq é o motif possivel devolve numero do index com prob
        maximo = -1.0
        maxind = -1
        for k in range(len(seq) - self.size):
            p = self.probabSeq(seq[k:k + self.size])
            if (p > maximo):
                maximo = p
                maxind = k
        return maxind


def test():

    from MySeq import MySeq
    seq1 = MySeq("AAAGTT")
    seq2 = MySeq("CACGTG")
    seq3 = MySeq("TTGGGT")
    seq4 = MySeq("GACCGT")
    seq5 = MySeq("AACCAT")
    seq6 = MySeq("AACCCT")
    seq7 = MySeq("AAACCT")
    seq8 = MySeq("GAACCT")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat(motifs.counts)
    printMat(motifs.pwm)
    print(motifs.alphabet)

    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))

    print(motifs.consensus())
    print(motifs.maskedConsensus())


if __name__ == '__main__':
    test()
