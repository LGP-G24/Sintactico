#https://chocopy.org/chocopy_language_reference.pdf
import lexico as lex #analisador lexico
import TokensReference as tkr
import bColors as colors
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
'''
#Ahora si empezamos a trabajar
expectedToken = [] #en esta variable vamos a guardar lo que posiblemente esperamos
currentIdent = 0 #Con esta variable vamos a revisar la identacion

def errorMessage(currentExpected,whatGet):
  print('Error se esperaba',currentExpected,'pero se obtuvo',whatGet) #error+
  print(expectedToken,"esperados")

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

def normal_var_equal(tokenIndex):
  types = ['tk_entero','True','False','None','tk_cadena','id']
  expectedToken.append('tk_igual')
  if(tokens[tokenIndex+1][0] =='tk_llave_izq'):
    equal_list(tokenIndex+1)
    return
  expectedToken.append(types)
  return 

def list_var_equal(tokenIndex):
  print("igual list")
  return 

def equal_list():
  
  return


def insidekeys(tokenIndex):
  canBeIn = ['int','str','object','bool','id'] #posibles valores en la lista
  tokenIndex +=1 #sumamos uno para continuar con el flujo de ejecucion 
  while(True):
    if(tokens[tokenIndex][0] not in canBeIn):
      if(tokens[tokenIndex][0] == 'tk_llave_der'):
        tokenIndex +=1 #sumamos uno para continuar con el flujo de ejecucion 
        break  
      errorMessage(canBeIn,tokens[tokenIndex][0])
      break
    tokenIndex +=1 #sumamos uno para continuar con el flujo de ejecucion 
  return tokenIndex

tokenIndex = 0
while(tokenIndex < len(tokens)):
  if(tokens[tokenIndex][0] == 't'): #es una nueva linea entonces reinicie
    print('*****new line')
    expectedToken = []
    tokenIndex +=1
    continue
  if(len(expectedToken) < 1): #si esta vacio es una nueva linea
    #empezamos con una variable
    if(tokens[tokenIndex][0] == 'id'):
      if(tokens[tokenIndex + 1][0] == 'tk_dos_puntos'):
        var_def()
      elif(tokens[tokenIndex + 1][0] == 'tk_igual' ): #encontro una normal
        normal_var_equal(tokenIndex)
      elif(tokens[tokenIndex + 1][0] == 'tk_llave_izq' ):#encontro una lista
        list_var_equal()
      elif(tokens[tokenIndex + 1][0] == 't'): #salto de linea no pasa nada
        continue
      else:
        print("WTF acaba de poner una variable, sea serio")
  else: #Ya deberia tener algo para comparar
    # print(expectedToken)
    currentExpected = expectedToken.pop(0) #cojemos el primer elemento de el camino esperado
    if(type(currentExpected) == list ): #si es una lista miramos que este en las posibilidades
      if(tokens[tokenIndex][0] not in currentExpected):
        #revisamos llave izquierda
        if(tokens[tokenIndex][0]== 'tk_llave_izq'):
          tokenIndex = insidekeys(tokenIndex)
          continue
      #Si no fue nada entonces error y ya    
        errorMessage(currentExpected,tokens[tokenIndex][0])
        break
      #elif(token[0] == 'tk_llave_der'): 
    else:
      if(tokens[tokenIndex][0] != currentExpected):
        errorMessage(currentExpected,tokens[tokenIndex][0]) #error
        break
  tokenIndex +=1
'''

tokensInLines = []
auxList = []

def printWarning(message):
  print(colors.WARNING + message + colors.ENDC)
  return
def printError(message):
  print(colors.FAIL + message + colors.ENDC)
  return
def printGood(message):
  print(colors.OKGREEN + message + colors.ENDC)
  return

def checkIdent(line):
  if(line[0] == 't'):
    printWarning("Linea Vacia")
    return True
  else:
    try:
      ident = int(line[0])
      if(ident % 2 != 0):
        printError('Error de identacion')
    except:
      printError("caracter no esperado")

# vamos a generar una lista con todos los tokens en una
#linea, para poder hacer el analisis de cada uno
#basandonos en su estructura, es mas sencillo y menos abstracto
for token in tokens:
  if(len(token[0].split(' ')) != 1):
    auxList.append(token[0].split(' ')[1])
  else:
    auxList.append(token[0])
  if(token[0] == 't'):
    tokensInLines.append(auxList)
    auxList = []

#aqui vamos a hacer el analisis de cada una de las lineas 
#recordar que tokensInLines[n][0] es un numero o una t
for line in tokensInLines:
  #primero miramos la identacion
  print(line)
  if checkIdent(line): continue
  printGood('Linea correcta')
  