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

#variables space
tokensInLines = []
auxList = []
line = []
noError = True
debugLog = True
currentToken = 0


def printWarning(message):
  if not debugLog: return
  print(colors.WARNING + message + colors.ENDC)
  return
def printError(message):
  if not debugLog: return
  noError = False
  print(colors.FAIL + message + colors.ENDC)
  return
def printGood(message):
  if not debugLog: return
  print(colors.OKGREEN + message + colors.ENDC)
  return
def printDev(message):
  if not debugLog: return
  print(colors.HEADER + message + colors.ENDC)
  return

def restartLine():
  global currentToken
  global noError
  currentToken = 0
  noError = True

def checkIdent():
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

def goToNextToken():
  global currentToken
  currentToken += 1
  return

def id_path():
  printDev("id path started")
  goToNextToken()
  if len(line) == 1: return
  elif line[currentToken] == 'tk_dos_puntos':
    printDev('definicion de variable')
    var_def()
  elif line[currentToken] == 'tk_igual':
    printDev('igualacion de variable')
  elif line[currentToken] == 'tk_llave_izq':
    printDev('igualacion de variable lista')
  else:
    printeError("Error en variable")

def var_def():
  type_var()
  goToNextToken()
  if(line[currentToken] != 'tk_igual'): 
      printError('Se esperaba tk_igual pero se leyo ' + line[currentToken])
  literal()

def type_var():
  goToNextToken()
  if(line[currentToken] == 'tk_llave_izq'):
    list_declaration()
  else:
    chocoType()
  return

def list_declaration():
  printDev('definicion de variable lista')
  goToNextToken()
  chocoType()
  goToNextToken()
  if(line[currentToken] != 'tk_llave_der'):
    printError('Se esperaba tk_llave_der pero se leyo ' + line[currentToken])
  return

def chocoType():
  types = ['int','str','object','bool','id']#hay que tener en cuenta la lista
  if(line[currentToken] not in types):
    printError('Se esperaba'+ str(types) +' pero se obtuvo ' + line[currentToken])
  return

def literal():
  goToNextToken()
  types = ['tk_entero','True','False','None','tk_cadena','id']
  if(line[currentToken] not in types):
    printError('Se esperaba ' + str(types) + ' pero se obtuvo' + line[currentToken])
  return


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
for currentLine in tokensInLines:
  line = currentLine
  restartLine() #reiniciamos las variables de utilidad
  print(line)
  #primero miramos la identacion 
  if checkIdent(): continue
  goToNextToken() #una vez valida la identacion procedemos al siguiente token
  #Ahora vamos a ver por donde cogemos
  if line[currentToken] == 'id': id_path()
  if noError: printGood('Linea correcta')
  