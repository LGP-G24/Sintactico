#https://chocopy.org/chocopy_language_reference.pdf
import lexico as lex #analisador lexico
import TokensReference as tkr
from os import system #para limpiar la consola

'''
global c
c = 0
def program():
  c = c + 5
  return c
print (program())
'''
#Para facilitar las pruebas vamos a leer todo asi
fileToRead = 'test.txt'
tokens = lex.lexico(fileToRead) #Tokens es de tipo lista
system('clear') #Antes de todo limpiamos la consola para evitar outputs anteriores

#Ahora si empezamos a trabajar
expectedToken = [] #en esta variable vamos a guardar lo que posiblemente esperamos
currentIdent = 0 #Con esta variable vamos a revisar la identacion

def var_def():
  type_var()
  expectedToken.append('tk_igual')
  literal()

def type_var():
  expectedToken.append('tk_dos_puntos')
  chocoType()
  return

def chocoType():
  types = ['int','str','object','bool','id']#hay que tener en cuenta la lista
  expectedToken.append(types)
  return

def literal():
  types = ['tk_entero','True','False','None','tk_cadena','id']
  expectedToken.append(types)
  return  

for token in tokens:
  if(token[0] == 't'): #es una nueva linea entonces reinicie
    print('*****new line')
    expectedToken = []
    continue
  if(len(expectedToken) < 1): #si esta vacio es una nueva linea
    #empezamos con una variable
    if(token[0] == 'id'):
      var_def()
  else: #Ya deberia tener algo para comparar
    # print(expectedToken)
    currentExpected = expectedToken.pop(0) #cojemos el primer elemento de el camino esperado
    if(type(currentExpected) == list ): #si es una lista miramos que este en las posibilidades
      if(token[0] not in currentExpected):
        print('Error se esperaba',currentExpected,'pero se obtuvo',token[0]) #error
    else:
      if(token[0] != currentExpected):
        print('Error se esperaba', currentExpected,'pero se obtuvo',token[0]) #error
