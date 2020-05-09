import sys
import TokensReference as tkr

nombres = []
class token:
    token_name = ""
    lexeme = ""

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def add_token(self,t):
        self.token_name = t

    def add_char(self,c):
        #print(self.lexeme)
        self.lexeme += c

    def print_token(self):
        if self.lexeme in tkr.tokens and self.token_name != "tk_cadena":
            print ("<{},{},{}>".format(self.token_name,self.row,self.column))
        else:
            if (self.token_name == "tk_cadena"):
              print ("<{},\"{}\",{},{}>".format(self.token_name,self.lexeme,self.row,self.column))
            else:  
              print ("<{},{},{},{}>".format(self.token_name,self.lexeme,self.row,self.column))

    def add_to_tokens(self):
        nombres.append((self.token_name,self.lexeme,self.row,self.column))

def Row(row,line): #funcion para recorrer la linea, formar el lexema e imprimir el token
    state = 1; maxi = 1; i = 0; cont = 0; espacios=0;nl=0
    print("--------")
    while i < len(line):
        #print(state)
        if state == 1 and (line[i] == " " or  line[i] == "\t"):
            espacios += 1
            #print(espacios)
            i += 1
        elif(line[i]=="\n"):
          i += 1
          nl=1
        else:
            if state == 1:
                t = token(row,i+1)
                if (i== espacios):
                  t.add_token("tk_espacio"+" "+str (espacios))
                  t.add_to_tokens()
                  t.print_token()
                  espacios=0
            state = FSM(state,line[i],t.lexeme)
            #print(line[i],"   ",t.lexeme," state: ", state)
            if state == 7:
                cont = 1
            maxi = max(maxi,state)
            if state == 8:
              return 0
            if state == 0:
                print (">>> Error lexico (linea: {}, posicion: {})".format(row,t.column))
                return -1
            elif state < 0:
                if maxi <= 3:
                    if int(t.lexeme) >= 2147483647: 
                      print (">>> Error lexico (linea: {}, posicion: {})".format(row,t.column))
                      return -1
                    t.add_token("tk_entero")
                    t.lexeme = t.lexeme.split(".")[0]
                elif maxi == 4:
                    t.add_token("tk_real")
                elif maxi == 5:
                    if(t.lexeme=='/'or t.lexeme =='!'):
                      print (">>> Error lexico (linea: {}, posicion: {})".format(row,t.column))
                      return -1
                    t.add_token(tkr.tokens[t.lexeme])
                elif maxi == 6:
                    if t.lexeme in tkr.tokens:
                        t.add_token(tkr.tokens[t.lexeme])
                    else:
                        t.add_token("id")
                elif maxi == 7:
                    cont = 0
                    t.add_token("tk_cadena")
                if maxi != 7:
                    i += state
                t.add_to_tokens()
                t.print_token()
                maxi = 1
                state = 1
            elif line[i] != "\'" and line[i] != "\"":
                t.add_char(line[i])
            i += 1
            
    if cont == 1:
        print (">>> Error lexico (linea: {}, posicion: {})".format(row,t.column))
        return -1
    print("tk_newline")
    nombres.append("tk_newline")

    return 0


def FSM(state,c,lex): #funcion para recorrer el automata finite-state machine 
    if state == 1:
        if c == '#':
            return 8
        if c >= "0" and c <= "9":
            return 2
        elif (c >= "A" and c <= "Z") or (c >= "a" and c <= "z")or (c == "_"):
            return 6
        elif (c == '\"'):
            return 7
        elif (c == '!'or c =='/'):
          return 5
        elif c in tkr.tokens:
            return 5
        else:
            return 0
    elif state == 2:
        if c >= "0" and c <= "9":
            return 2
        elif (c >= "A" and c <= "Z") or (c >= "a" and c <= "z"):
            return -1
        else:
            return -1
    elif state == 3:
        if c >= "0" and c <= "9":
            return 4
        else:
            return -2
    elif state == 4:
        if c >= "0" and c <= "9":
            return 4
        elif (c >= "A" and c <= "Z") or (c >= "a" and c <= "z"):
            return 0
        else:
            return -1
    elif state == 5:
        if lex+c in tkr.tokens:
            return 5
        else:
            return -1
    elif state == 6:
        if (c >= "A" and c <= "Z") or (c >= "a" and c <= "z") or (c >= "0" and c <= "9") or c == "_":
            return 6
        else:
            return -1
    elif state == 7:
        if (c=='\'') or (c == '\"'):
            return -1
        if (ord(c) == 92):
          return 9
        if(ord(c)>=32 and ord(c)<=126):
          return 7
        else:
            return 0
    elif state == 9:
      if (c != "n" or c != "t" or c != "\"" or c != "\\"):
        return 0
      return 7

def lexico(fileToRead):
  fic = open(fileToRead, "r")
  lines = []
  for i in fic:
    lines.append(i)
  fic.close()
  #lines = sys.stdin.readlines()
  #print("Nuevo caso")
  for i in range(len(lines)):
    if Row(i+1,lines[i]+" ") == -1:
        break
  return nombres
