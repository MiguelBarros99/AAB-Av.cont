# -*- coding: utf-8 -*-

from MySeq import MySeq
from MyMotifs import MyMotifs
from random import randint
from random import random

class MotifFinding:

    def __init__(self, size=8, seqs=None):
        self.motifSize = size  # definir o tamanho dos motifs a procurar (8 por default)
        if (seqs != None):  # se seqs é definido constroi o self.seqs e self.alphabet
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []  # senão é lista vazia

    def __len__(self):
        return len(self.seqs)  # nº de elementos na lista self.seqs

    def __getitem__(self, n):
        return self.seqs[n]  # primeira seq em self.seqs ('string')

    def seqSize(self, i):
        return len(self.seqs[i])  # tamanho da sequencia i

    def readFile(self, fic, t):  # ler um ficheiro e add a self.seqs (t é o tipo de sequencia)
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(), t))
        self.alphabet = self.seqs[0].alfabeto()

    def createMotifFromIndexes(self,indexes):  # input de uma lista de númereos, contem o número em que para cada seq começa o motif()
        pseqs = []
        for i, ind in enumerate(indexes):
            pseqs.append(MySeq(self.seqs[i][ind:(ind + self.motifSize)], self.seqs[i].tipo))  # adiciona a pseqs (uma sequência i  onde começa o motif e onde vai acabar) mais o tipo de seq que é
        return MyMotifs(pseqs)  # vai correr em Mymotifs com o pseqs

    # SCORES

    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()  # gera matriz de contagens
        mat = motif.counts  # transpor.la
        for j in range(len(mat[0])):  # para colunas da matriz
            maxcol = mat[0][j]  # maxcolun é igual ao primeiro elemento da coluna
            for i in range(1,len(mat)):  # iniciando no segundo elemento da coluna j e compara todos os scores da coluna
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score += maxcol  # adiciona o valor ao score
        return score

    def scoreMult(self,s):  #score em probabilidades
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score *= maxcol
        return score

    # EXHAUSTIVE SEARCH

    def nextSol(self, s):
        nextS = [0] * len(s)  # gera lista s, com a posição das seqs em que está a começar a formação dos motifs
        pos = len(s) - 1  # comprimento da lista s -1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize: #até pos diminuir
            pos -= 1
        if (pos < 0):nextS = None  # quando s tem size 0 devolve none
        else:
            for i in range(pos):  # iguala S á next s incrementando o ultimo elemento de s mais 1
                nextS[i] = s[i]
            nextS[pos] = s[pos] + 1
            for i in range(pos + 1, len(s)):  # vai acrescentar um 0 a lista s se esta não for composta por valores de s
                nextS[i] = 0
        return nextS

    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0] * len(self.seqs)  # lista de 0 com o numero de seqs na lista self.seqs
        while (s != None):
            sc = self.score(s)  # Score para as posições
            if (sc > melhorScore):  # verificar o melhor score e se true alterar
                melhorScore = sc
                res = s
            s = self.nextSol(s)  # o próximo s vai ser o nexts
        return res  #posições inicais que maximizam o score

    # BRANCH AND BOUND

    def nextVertex(self, s):
        res = []
        if len(s) < len(self.seqs):  # internal node -> down one level #se o comprimento de len(s) for menor implica que n está a abranjer as seqs todas logo ira dar append a mais um 0 e vai dar essa s como o nexts
            for i in range(len(s)):
                res.append(s[i])
            res.append(0)
        else:  # bypass
            pos = len(s) - 1
            while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:  # while para as posições e se condição se mantem
                pos -= 1
            if pos < 0: res = None  #se s for sem nada devovle none
            else:
                for i in range(pos): res.append(s[i])  # gera nova lista s e adiciona +1
                res.append(s[pos] + 1)
        return res

    def bypass(self,s):  # verificar se já esta nas ultimas letras de seq, se chegou vai altera para 0 e acrescenta
        res = []
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:pos -= 1
        if pos < 0: res = None
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos] + 1)
        return res

    def branchAndBound(self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0] * size  # lista s
        while s != None:  # ate s não ficar vazio
            if len(s) < size:  # vericar que len s não é menor que size, senao fazer optimScore
                optimScore = self.score(s) + (size - len(s)) * self.motifSize
                if optimScore < melhorScore: #score melhor vai ao bypass
                    s = self.bypass(s)
                else: #senao next vertex
                    s = self.nextVertex(s)
            else:
                sc = self.score(s)  # score dos motifs
                if sc > melhorScore:  # altera score caso seja menor
                    melhorScore = sc
                    melhorMotif = s
                s = self.nextVertex(s)  # S segue para nextvertex
        return melhorMotif

    # Consensus (heuristic)

    def heuristicConsensus(self):
        """ Procura as posições para o motif nas duas primeiras sequências """
        mf = MotifFinding(self.motifSize, self.seqs[:2])  # Procura exaustiva das duas primeiras sequências
        s = mf.exhaustiveSearch()  # vai procurar a posição inical entre 2 seqs com o score ideal
        for a in range(2,len(self.seqs)):  # Avalia a melhor posição para cada uma das outras sequências, guardando-a (maximiza o score)
            s.append(0)
            melhorScore = -1
            melhorPosition = 0
            for b in range(self.seqSize(a) - self.motifSize + 1):
                s[a] = b
                scoreatual = self.score(s)
                if scoreatual > melhorScore:
                    melhorScore = scoreatual
                    melhorPosition = b
                s[a] = melhorPosition
        return s

    # Consensus (heuristic)

    def heuristicStochastic(self):
        from random import randint
        s = [0] * len(self.seqs)  # Gera um vetor aleatória com o mesmo tamanho do número de sequências
        # Passo 1: inicia todas as posições com valores aleatórios
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)  # Escolhe um valor random como valor inicial de cada seq
        # Passo 2
        melhorscore = self.score(s)
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s)  # Constrói o perfil baseado nas posições iniciais s
            motif.createPWM()
            # Passo 3
            for i in range(len(self.seqs)):  # Avalia a melhor posição inicial para cada sequência com base no perfil
                s[i] = motif.mostProbableSeq(self.seqs[i])  # para cada seq qual é a subseq nelas que é mais provável (segundo PWM)
            # Passo 4
            # verifica melhoria
            scr = self.score(s)  # score
            if scr > melhorscore:  # alterar se é melhor
                melhorscore = scr
            else:
                improve = False
        return s

    # Gibbs sampling

    def gibbs(self, iterations=1000):
        s = []  # criar a lista de posições iniciais
        # Passo 1
        for i in range(len(self.seqs)): s.append(randint(0, len(self.seqs[i]) - self.motifSize - 1))  # escolher um numero random de start para cada sequência
        melhorscore = self.score(s)  # calcular o score de s
        bests = list(s)
        for it in range(iterations):
            # Passo 2: selecionar uma das sequência aleatoriamente
            seq_idx = randint(0, len(self.seqs) - 1)
            # Passo 3: criar um perfil que não contenha a sequência aleatória
            seq = self.seqs[seq_idx]  # indicar qual a seq que vai remover
            s.pop(seq_idx)  # remover a posição correspondente a seq escolhida p
            removed = self.seqs.pop(seq_idx)  # vai dar pop da seq a lista
            motif = self.createMotifFromIndexes(s)  # Criar o perfil sem a sequência
            motif.createPWM()
            self.seqs.insert(seq_idx,removed)  # reinserir seq removida da lista na posição seq_idx
            r = motif.probAllPositions(seq)  # probabilidade de todas as subseqs possiveis na seq removida
            pos = self.roulette(r)  # roulette da lista e escolher com valor maior que 0, devolvendo a posição onde se iniciou o motif
            s.insert(seq_idx, pos)  # adiciona o valor da pos do motif ao s na posição seq_idx
            score = self.score(s)  # score do novo
            if score > melhorscore:  # redifinir scores se for maior
                melhorscore = score
                bests = list(s)
        return bests  # vai dar return do s

    def roulette(self, f):
        tot = 0.0
        for x in f: tot += (0.01 + x)
        val = random() * tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind - 1

    # Pseudocontagens

    def scoreEX(self, m):  #contagem com as pseudo contagens
        score = 0
        motif = self.createMotifFromIndexes(m)
        motif.doCounts()
        mat = []
        for i in range(len(motif.counts)):
            linha = []
            for j in range(len(motif.counts[i])):
                linha.append(motif.counts[i][j] + 1)
            mat.append(linha)
        for k in range(len(mat[0])):
            maxcol = mat[0][k]
            for f in range(1, len(mat)):
                if mat[f][k] > maxcol:
                    maxcol = mat[f][k]
            score += maxcol
        return score

    def probabSeqEX(self, seq,pwm):  # A probabilidade de seq fazer parte deste quadro sendo que todos os elementos do quadro n pode ter valores negativos
        res = 1.0
        for i in range(self.motifSize):
            lin = self.alphabet.index(seq[i])
            res *= pwm[lin][i]
        return res

    def mostProbableSeqEX(self, seq,pwm):  # para que posição inicial da subseq de uma seq de comprimento indefenido encaixa melhor no quandro de motifs das seqs
        maximo = -1.0
        maxind = -1
        for k in range(len(seq) - self.motifSize):
            p = self.probabSeqEX(seq[k:k + self.motifSize], pwm)
            if (p > maximo):
                maximo, maxind = p,k
        return maxind

    def probAllPositionsEX(self, seq,pwm):  # lista com as probabilidades de acontecer em cada letra da seq
        res = []
        for k in range(len(seq) - self.motifSize + 1): res.append(self.probabSeqEX(seq, pwm))
        return res

    def heuristicStochasticex1_al5(self):
        s = [0] * len(self.seqs)
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize)
        # Passo 2
        melhorscore = self.scoreEX(s)  # score consoante o novo score2 que não tem 0
        improve = True
        while improve:
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            newPWM = []
            for k in range(len(motif.pwm)):
                linhas = []
                for t in range(len(motif.pwm[0])): linhas.append(motif.pwm[k][t] + 0.1)
                newPWM.append(linhas)
                # Passo 3
            for i in range(len(self.seqs)):
                s[i] = self.mostProbableSeqEX(self.seqs[i], newPWM)
            scr = self.scoreEX(s)
            if scr > melhorscore:
                melhorscore = scr
            else:improve = False
        return s

    def gibbsEX(self, iterations=1000):
        s = []
        for i in range(len(self.seqs)):
            s.append(randint(0, len(self.seqs[i]) - self.motifSize - 1))
        melhorscore = self.scoreEX(s)
        bests = list(s)
        for it in range(iterations):
            seq_idx = randint(0, len(self.seqs) - 1)
            seq = self.seqs[seq_idx]
            s.pop(seq_idx)
            removed = self.seqs.pop(seq_idx)
            motif = self.createMotifFromIndexes(s)
            motif.createPWM()
            newPWM = []  # matriz PWM
            for k in range(len(motif.pwm)):
                linhas = []
                for t in range(len(motif.pwm[0])): linhas.append(motif.pwm[k][t] + 0.1)
                newPWM.append(linhas)
            self.seqs.insert(seq_idx,removed)  # vai voltar a adicionar a seq removida a lista de seqs na posição seq_idx
            r = self.probAllPositionsEX(seq, newPWM)  # vai calcular a probabilidade de todas as subseqs possiveis na seq removida
            pos = self.roulette(r)  #  roulette da lista e escolher valores maior que 0, devolve posição onde se iniciou o motif
            s.insert(seq_idx, pos)  # valor da pos do motif ao s na posição seq_idx inserido
            score = self.scoreEX(s)  # score do novo s
            if score > melhorscore:  # vai ver se este é maior que o melhor scor se for, o melhorscore passa a ser o score e a bests passa a ser a s
                melhorscore = score
                bests = list(s)
        return bests  # return s

# tests

def test1():
    sm = MotifFinding()
    sm.readFile('exemploMotifs.txt', 'dna')
    sol = [25, 20, 2, 55, 59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)


def test2():
    print("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA", "dna")
    seq2 = MySeq("ACGTAGATGA", "dna")
    seq3 = MySeq("AAGATAGGGG", "dna")
    mf = MotifFinding(3, [seq1, seq2, seq3])
    sol = mf.exhaustiveSearch()
    print("Solution", sol)
    print("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print("Solution: ", sol2)
    print("Score:", mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())

    print("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print("Solution: ", sol1)
    print("Score:", mf.score(sol1))


def test3():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt", "dna")
    print("Branch and Bound:")
    sol = mf.branchAndBound()
    print("Solution: ", sol)
    print("Score:", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())


def test4():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt", "dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print("Solution: ", sol)
    print("Score:", mf.score(sol))
    print("Score mult:", mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    sol2 = mf.gibbs()
    print("Score:", mf.score(sol2))
    print("Score mult:", mf.scoreMult(sol2))


def testEX():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt", "dna")
    print("Heuristic stochasticEX")
    sol = mf.heuristicStochasticex1_al5()
    print("SolutionEX: ", sol)
    print("ScoreEX:", mf.scoreEX(sol))
    print("ConsensusEX:", mf.createMotifFromIndexes(sol).consensus())
    sol2 = mf.gibbsEX()
    print("Score:", mf.scoreEX(sol2))


test1()
print('-------------------')
test2()
print('-------------------')
test3()
print('-------------------')
test4()
print('-------------------')
testEX()
