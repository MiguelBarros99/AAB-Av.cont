from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding
from MyMotifs import MyMotifs


def createMatZeros(nl, nc):
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()


class EAMotifsInt (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])

    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            ind.setFitness(fit)


class EAMotifsReal(EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs.motifSize) * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])

    def vec_to_pwn(self, v):
        pwm = createMatZeros(len(self.motifs.alphabet), self.motifs.motifSize)
        for i in range(0, len(v),len(self.motifs.alphabet)):
            col_idx = i / len(self.motifs.alphabet)
            col = v[i:i+len(self.motifs.alphabet)]
            soma = sum(col)
            for j in range(len(self.motifs.alphabet)):
                pwm[i][col_idx] = col[j] / soma



    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            self.motifs.pwm = self.vec_to_pwn(sol)
            s=[]
            for seq in self.motifs.seqs:
                p= self.motifs.mostProbableSeqEX(seq)
                s.append(p)
            #TPC usar score multiplicativo sem atualizar PWM
            fit = self.motifs.score(sol)



def test1():
    ea = EAMotifsInt(100, 1000, 50, "exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


def test2():
    ea = EAMotifsReal(100, 2000, 50, "exemploMotifs.txt", 2)
    ea.run()
    ea.printBestSolution()


test1()
# test2()
