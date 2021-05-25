class SuffixTree2:

    def __init__(self):
        self.nodes = {0: (-1, {})}  # root node
        self.num = 0

    def print_tree(self):
        for k in self.nodes.keys():
            m,n = self.descompact(k)
            if m < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", m, n)

    def descompact(self,k):
        if self.nodes[k][0] != -1: #senao for um leaf
            m,n = self.nodes[k][0]
        else: #se for um elemento do ramo
            m= self.nodes[k][0]
            n = ''
        return m,n

    def add_node(self, origin, symbol, leafnum=-1):
        self.num += 1  # numero de nodulo adiciona
        self.nodes[origin][1][symbol] = self.num  # 1 é para ir buscar  dentro do tuplo no dicionario
        self.nodes[self.num] = (leafnum, {})  # construi o tuplo para o node a seguir

    def add_suffix(self, p, sufnum, seq):  # o -padrao , sufnum - i
        pos = 0
        node = 0
        while pos < len(p):  # seguir a sequencia no ciclo pos
            if p[pos] not in self.nodes[node][1].keys():  # se a letra na posição pos da seq p não tiver no dicionario no node
                if pos == len(p) - 1:
                    self.add_node(node, p[pos], (sufnum, seq)) # adicionar o node final/leaf se for o $.
                else:
                    self.add_node(node, p[pos])  # adicionar ao node a letra p[pos]
            node = self.nodes[node][1][p[pos]]  # mudar de node, output é um numero
            pos += 1  # avançar uma posição

    def suffix_tree_from_seq(self, seq1 , seq2):
        seq1 = seq1 + "$"  # adiciona dollar a seq1
        seq2 = seq2 + '#'
        for i in range(len(seq1)):
            self.add_suffix(seq1[i:], i, 0)  # range para passar a seq de i ao fim e apartir de que posição foi passada
        for i in range(len(seq2)):
            self.add_suffix(seq2[i:], i, 1)  # range para passar a seq de i ao fim e apartir de que posição foi passada

    def find_pattern(self, pattern):
        #       pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
            else:
                return None
        x = self.get_leafes_below(node) #ir buscar os patterns direitos
        res0, res1= [],[]
        for i in x:
            m,n = i
            if n == 0:
                res0.append(m)
            elif n ==1:
                res1.append(m)
        return (res0,res1)

    def get_leafes_below(self, node):
        res = []
        m,n = self.descompact(node) #desconcatenar os tuplos
        if m >= 0:  # maior ou igual 0 é para verificar uma leaf
            res.append((m,n))  # adicionar o valor da leaf
        else:
            for k in self.nodes[node][1].keys():  # correr todas as keys no nodulo
                newnode = self.nodes[node][1][k]  # mudar para o node
                leafes = self.get_leafes_below(newnode)  # recursividade para seguir os ramos ate leaf
                res.extend(leafes)  # concatenar a lista da recursiva
        return res

    def get_coords(self): #obter as coords dos ultimos pontos
        res= []
        x = len(self.nodes)-1
        p = 1
        while p != 0 and x != 0:
            if self.nodes[x][0]!= -1:
                m,n = self.descompact(x)
                if m == 0 and n == 0: #sequencia 0 na intereção 0
                    res.append(x)
            x -= 1
        x = len(self.nodes)-1
        p = 1
        while p != 0 and x != 0:
            if self.nodes[x][0] != -1:
                m, n = self.descompact(x)
                if m == 0 and n == 1: #sequencia 1 na intereção 0
                    res.append(x)
            x -= 1
        return res

    def get_sequence(self):
        s1 = '' #abrir a construção de sequencias
        s2 = ''
        seq1, seq2 = self.get_coords() #coordenadas dos nodulos iniciais
        x = seq1
        while x > 0:
            l,y = self.find_node(x)  #encontrar o nodulo de onde veio e prosseguir ate o node 0
            s1 = l + s1 # adiciona a letra a seq em construção
            x = y # redefinir o x para o nodulo anterior
        x = seq2
        while x > 0:
            l, y = self.find_node(x) #encontrar o nodulo de onde veio e prosseguir ate o node 0
            s2 = l + s2 # adiciona a letra a seq em construção
            x = y # redefinir o x para o nodulo anterior
        return s1,s2

    def find_node(self,coord):  # encontrar o nodulo anterior
        x = len(self.nodes) - 1
        p = 1
        while p != 0 and x >= 0:  #ciclo do while para correr os nodes e procurar qual o node e a letra associada aoa seguimento para o proximo node
            for i in self.nodes[x][1].keys():
                if self.nodes[x][1][i] == coord:
                    p = 0
                    k = i,x
            x -=1
        return k  #decolve a letra associada e o node

    def largestCommonSubstring (self):
        f_match = ''
        f_count = 0
        s1,s2 = self.get_sequence()  #obter as sequencias iniciais
        for i in range(len(s1)): #correr em for a s1 e a s2
            for l in range(len(s1)):
                count = 0
                match = ''
                if s1[i] == s2[l]: #quando haver match
                    p = 1
                    x, y = i , l
                    while p!= 0: #abro ciclo de while para correr separadamente e obter o max de substring
                        if s1[x] == s2[y]:
                            match += s1[x]
                            count += 1
                            x += 1
                            y += 1
                        else: #quando houver diferenças verificar se é uma substring maior e substituir
                            if count > f_count:
                                f_match = match
                                f_count = count
                            p = 0 #terminar o ciclo while
        return f_match

def test2():
    seq1 = "GADDGFGGGGGGGGGHLDHOFOIGJKCTA"
    seq2 = "TAAGADGGFGGGGGGGGGHLDHOFOIGJKCTA"
    st = SuffixTree2()
    st.suffix_tree_from_seq(seq1,seq2)
    #print(st.get_coords())
    #st.print_tree()
    print(st.nodes)
    #print(len(st.nodes))
    #print(st.find_pattern("TAC"))
    # print(st.repeats(2,2))
    #print(st.matches_prefix("TA"))
    print(st.largestCommonSubstring())

test2()




