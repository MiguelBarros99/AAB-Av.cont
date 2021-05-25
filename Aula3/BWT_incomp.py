# -*- coding: utf-8 -*-

class BWT:

    def __init__(self, seq="", buildsufarray=False):
        self.bwt = self.build_bwt(seq, buildsufarray)

    def set_bwt(self, bw):
        self.bwt = bw

    def build_bwt(self, text, buildsufarray=False): #construir o bwt para rodar a string
        ls = []
        for i in range(len(text)): #dollar ja incluido na sequencia
            ls.append(text[i:] + text[:i])
        ls.sort() #sorted por ordem alfabetica
        res = ""
        for i in range(len(text)):
            res += ls[i][len(text) - 1]  # Percorrer a lista e para cada string vai buscar o último elemento da string
        if buildsufarray: #apenas se for true para o init
            self.sa = []
            for i in range(len(ls)):
                stpos = ls[i].index("$") #indexação em relação ao $ para poder reconstruir
                self.sa.append(len(text) - stpos - 1)
        return res

    def inverse_bwt(self):
        firstcol = self.get_first_col()  #obter a 1 coluna para indexação
        res = ""
        c = "$" # o primeiro carater é sempre $
        occ = 1 # buscar a primeira ocorrencia
        for i in range(len(self.bwt)): #percorre a str da bwt (ultima coluna)
            pos = find_ith_occ(self.bwt, c, occ) #indexação do $ no incio
            c = firstcol[pos] #vai buscar a primeira coluna a que letra corresponde
            occ = 1
            k = pos - 1
            while firstcol[k] == c and k >= 0: #serve para ver se quantos mais carateres desses ha na priemria comuna antes
                occ += 1
                k -= 1 #define o k e occ para o priximo for
            res += c
        return res

    def get_first_col(self):
        firstcol = []
        for c in self.bwt: # na bwt pega na primeira coluna e guarda-a
            firstcol.append(c)
        firstcol.sort() #ordena segundo a ordem alfabetica
        return firstcol

    def last_to_first(self): #ligação entre as duas colunas
        res = []
        firstcol = self.get_first_col()
        for i in range(len(firstcol)):
            c = self.bwt[i]
            ocs = self.bwt[:i].count(c) + 1 #conta ocorrencias desse carater até ao i (numero do carater)
            res.append(find_ith_occ(firstcol, c, ocs))  #dou append ao res a occorencia na 1 coluna
        return res

    def bw_matching(self, patt):
        lf = self.last_to_first()
        res = []
        top = 0
        bottom = len(self.bwt) - 1
        flag = True
        while flag and top <= bottom:
            if patt != "": #se existir padrão
                symbol = patt[-1]
                patt = patt[:-1]
                lmat = self.bwt[top:(bottom + 1)] #top e bottom usados para restringir na bwt
                if symbol in lmat:
                    topIndex = lmat.index(symbol) + top #index na bwt (1º index)
                    bottomIndex = bottom - lmat[::-1].index(symbol) #index na bwt (ultima index com o sybolo
                    top = lf[topIndex]  #index na bwt para o range da firstcol antes
                    bottom = lf[bottomIndex]
                else:
                    flag = False
            else:
                for i in range(top, bottom + 1): res.append(i)
                flag = False
        return res

    def bw_matching_pos(self, patt):
        res = []
        matches = self.bw_matching(patt)
        for m in matches:
            res.append(self.sa[m])
        res.sort()
        return res


# auxiliary

def find_ith_occ(l, elem, index):   #index da x occorrencia na btw
    j, k = 0, 0
    while k < index and j < len(l):
        if l[j] == elem:
            k = k + 1
            if k == index: return j
        j += 1
    return -1


def test():
    seq = "TAGACAGAGA$"
    bw = BWT(seq)
    print(bw.bwt)
    print(bw.last_to_first())
    print(bw.bw_matching("AGA"))


def test2():
    bw = BWT("")
    bw.set_bwt("ACG$GTAAAAC")
    print(bw.inverse_bwt())


def test3():
    seq = "TAGACAGAGA$"
    bw = BWT(seq, True)
    print("Suffix array:", bw.sa)
    print(bw.bw_matching_pos("AGA"))


test()
test2()
test3()

