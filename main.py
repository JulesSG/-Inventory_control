"""
 Proyecto final
 Fecha: 10/6/2021
 Autores:
 Julio Salazar
 Joshua Alarcon
 Programa: inventario
"""
import os
from datetime import datetime # Libreria para extraer la hora del sistema

"""
estructura del inventario
ID/TIPO/NOMBRE/CANTIDAD
estructura de las transacciones
nombrePieza$ID$tipoTransacc$Estatus$cantidad$fechahora
"""
def fecha(): # funcion que extrae la hora y la guarda en una lista
    feHo=[datetime.now().strftime('%d/%m/%Y'),datetime.now().strftime('%H:%M')]
    return feHo

def cargarArchivos(): # Esta funcion abre los archivos y los carga en una lista(las transacciones) y en un diccionario(el inventario)
    global inventarioDIC
    global transaccionesList
    transaccionesList =[]
    inventarioDIC = {}
    transacciones=open('Transacciones.txt','r')
    inventario=open('Inventario.txt','r')
    for i in inventario:
      inventarioDIC[i[:2]]=i.split("/")# se llena el diccionario
    inventario.close()
    for i in transacciones:
        transaccionesList.append(i)


def ingresarPiezas(ID,aumento): #  En esta funcion se ingresan las piezas por ID
    bandera=0
    f = fecha()
    for i in inventarioDIC:
        if i == ID.upper():
             bandera=1
             print("Realizada con exito")
             inventarioDIC[i][3]=int(aumento)+int(inventarioDIC[i][3])
             transaccionesList.append(f"{inventarioDIC[i][2]}${inventarioDIC[i][0]}$Ingresar pieza$Realizada${aumento}${f[0]}-{f[1]}\n")
    if bandera==0:
        print("ID no existe\n")
        transaccionesList.append(f"-$-$Ingresar pieza$Error$0${f[0]}-{f[1]}\n")

def extraerPiezas(ID,disminuyo): # en esta funcion se extraen piezas por ID
  try:
    piezas =  int(inventarioDIC[ID.upper()][3])-int(disminuyo)
    f = fecha()
    for i in inventarioDIC:
        if i == ID.upper():
            if piezas>=0:
               inventarioDIC[i][3]=piezas
               transaccionesList.append(f"{inventarioDIC[i][2]}${inventarioDIC[i][0]}$Retirar pieza$Realizada${disminuyo}${f[0]}-{f[1]}\n")
            else:
               print(f'Error al estraer {disminuyo}  {inventarioDIC[i][1]} de  {inventarioDIC[i][2]}, no hay suficientes. Fecha: {f[0]} Hora: {f[1]}\n ')
               transaccionesList.append(f"{inventarioDIC[i][2]}${inventarioDIC[i][0]}$Retirar pieza$Error$0${f[0]}-{f[1]}\n")
  except KeyError:
        f = fecha()
        print("ID no existe\n")
        transaccionesList.append(f"-$-$Retirar pieza$Error$0${f[0]}-{f[1]}\n")


def hayInven(ID,nombre,opcion): # esta funcion realiza consultas al inventario, por ID, nombre, si hay o no hay existencia de piezas en el inventario
    bandera=0
    for i in inventarioDIC: # se aprobecha este for para hacer 2 tipos de consultas
          if int(inventarioDIC[i][3])>0:
            if opcion==1: # Cuando hay piezas en existencia en el inventario
              print(f"Hay {inventarioDIC[i][3]} {inventarioDIC[i][1]} de {inventarioDIC[i][2]}, ID: {inventarioDIC[i][0]}")

          elif opcion==4: # Cuando no hay piezas en existencia en el inventario
                 print(f"Hay 0 {inventarioDIC[i][1]} de {inventarioDIC[i][2]}, ID: {inventarioDIC[i][0]}")

    if opcion==2: # Consulta de existencia por ID
        try:
            if int(inventarioDIC[ID.upper()][3]) > 0:
                    print(f"Hay {inventarioDIC[ID.upper()][3]} {inventarioDIC[ID.upper()][1]} de {inventarioDIC[ID.upper()][2]}, ID: {inventarioDIC[ID.upper()][0]}")
            else:
                print('No hay existencia de esa pieza')
        except KeyError:
            print("El ID que ingreso, no existe\n")

    elif opcion == 3: # Consulta de existencia por nombre
       for i in  inventarioDIC:
         if nombre.lower()==inventarioDIC[i][2].lower():
           bandera = 1
           if int(inventarioDIC[i][3]) > 0:
               print(f"Hay {inventarioDIC[i][3]} {inventarioDIC[i][1]} de {inventarioDIC[i][2]}, ID: {inventarioDIC[i][0]}")
           else:
               print('No hay existencia de esa pieza')
       if bandera == 0:
           print("El nombre que ingreso, no existe\n")



def imprimirInvent(): # Imprime el inventario (el que esta cargado en RAM, el diccionario, por lo tanto, si no se cierra el programa
    f = fecha()       # adecuadamente, no se actualizara el archivo)
    print("--------------------------Inventario------------------------------------\n")
    print(f"Fecha: {f[0]} Hora: {f[1]}\n")
    print('{:<12}     {:<8} {:<15}    {:<15}'.format('Tipo de Pieza', 'ID' ,'Nombre','Cantidad'))
    for i in inventarioDIC:
         print(" {:<12}     {:<8} {:<15}      {:<15}".format( inventarioDIC[i][1],  inventarioDIC[i][0]  ,inventarioDIC[i][2] ,inventarioDIC[i][3]))

def reporte(): # crea un reporte de cierre, imprime el inventario actual y actualiza los archivos con la lista y el diccionario
    transacciones = open('Transacciones.txt', "w")
    f = fecha()
    inventario=open('Inventario.txt','w')
    transaccionesList.append(f"-$-$Cierre del programa$Realizada$0${f[0]}-{f[1]}\n")
    print((f"Cierre del programa. \n"))
    imprimirInvent()
    for i in inventarioDIC:
        for x in range(4):
            if x<3:
               inventario.write(str(inventarioDIC[i][x])+'/')
            else:
                inventario.write(str(inventarioDIC[i][x]) + '/\n')
    for i in transaccionesList:
        transacciones.write(i)
    transacciones.close()
    inventario.close()

def impreTran(): # imprime las transacciones
    print('-----------------------------------------Transacciones-------------------------------------------------\n')
    print('{:<16} {:<8} {:<30} {:<30} {:<30} {:<30}'.format('Nombre Pieza','ID','Tipo de transaccion','Estatus','Cantidad','Fecha-Hora\n'))
    for i in transaccionesList:
       temp=i.split('$')
       print('{:<16} {:<8} {:<30} {:<30} {:<30} {:<30}'.format(temp[0], temp[1], temp[2], temp[3],temp[4], temp[5]))

def main():  # menu principal
        opcion = 0
        cargarArchivos()
        modo=input('Dijite 1 si quiere ingresar con el color normal, dijite 2 para ingresar con color hacker: ')
        if modo=='1':
            os.system('color 0f') # definir color de letra
        else:
           os.system('color 02')
        while opcion < 10:
            f = fecha()
            try:
                print("            Control de Inventario\n")
                print("*********      Menú de opciones    ***********")
                print("\n")
                print("1- Ingresar piezas")
                print("2- Retirar piezas")
                print("3- Piezas existentes en el inventario")
                print("4- Reporte de transacciones")
                print('5- Consulta por ID de pieza')
                print('6- Consulta por nombre de pieza')
                print('7- Imprimir el inventario')
                print('8- Piezas por comprar')
                print('9- Salir y generar reporte de cierre\n')
                opcion = int(input("Digite la opción: "))
                print("\n")
                os.system('cls') # borrar pantalla
                if opcion == 1:
                    ID = input('ingrese el ID de la pieza que va a agregar: ')
                    while True:
                     try:
                      cantidad=int(input('Ingrese la cantidad que desea agregar: '))
                      if cantidad>=0:
                          ingresarPiezas(ID, cantidad)
                          wait = input('Presiona enter para continuar \n')
                          os.system('cls')
                          break
                      else:
                        print('No se aceptan numeros negativos\n')
                        transaccionesList.append(f"-$-$Ingresar pieza$Error$0${f[0]}-{f[1]}\n")
                      wait = input('Presiona enter para continuar \n')
                      os.system('cls')
                     except ValueError:
                         print("\n Entrada no aceptada, ingresa una opcion numerica entera positiva\n")
                         transaccionesList.append(f"-$-$Ingresar pieza$Error$0${f[0]}-{f[1]}\n")
                         wait = input('Presiona enter para continuar \n')
                         os.system('cls')

                elif opcion == 2:
                    ID = input('ingrese el ID de la pieza que va a extraer: ')
                    while True:
                        try:

                            cantidad = int(input('Ingrese la cantidad que desea extraer: '))
                            if cantidad >= 0:
                                extraerPiezas(ID, cantidad)
                                wait = input('Presiona enter para continuar \n')
                                os.system('cls')
                                break
                            else:
                                print('No se aceptan numeros negativos\n')
                                transaccionesList.append(f"-$-$Retirar pieza$Error$0${f[0]}-{f[1]}\n")
                            wait = input('Presiona enter para continuar \n')
                            os.system('cls')
                        except ValueError:
                            print("\n Entrada no aceptada, ingresa una opcion numerica entera positiva\n")
                            transaccionesList.append(f"-$-$Retirar pieza$Error$0${f[0]}-{f[1]}\n")
                            wait = input('Presiona enter para continuar \n')
                            os.system('cls')

                elif opcion == 3:
                    print("Componentes existentes en el inventario\n")
                    hayInven(0,0,1)
                    wait = input('\nPresiona enter para continuar \n')
                    os.system('cls')

                elif opcion == 4:
                    impreTran()
                    wait = input('\nPresiona enter para continuar \n')
                    os.system('cls')

                elif opcion == 5:
                  id=input('Dijite el ID de la pieza que desea consultar: ')
                  hayInven(id,0,2)
                  wait = input('\nPresiona enter para continuar \n')
                  os.system('cls')

                elif opcion == 6:
                    nombre = input('Dijite el nombre de la pieza que desea consultar: ')
                    hayInven(0, nombre, 3)
                    wait = input('\nPresiona enter para continuar \n')
                    os.system('cls')

                elif opcion == 7:
                  imprimirInvent()
                  wait = input('\nPresiona enter para continuar \n')
                  os.system('cls')

                elif opcion == 8:
                    print("Se necesitan comprar las siguientes piezas:\n")
                    hayInven(0,0,4)
                    wait = input('\nPresiona enter para continuar \n')
                    os.system('cls')

                elif opcion == 9:
                    reporte()
                    wait = input('\nPresiona enter para continuar \n')
                    break

            except ValueError:
                print("\n Entrada no aceptada, ingresa una opcion numerica entera positiva\n")
                wait=input('Presiona enter para continuar \n')
                os.system('cls')
            except IndexError:
             pass

main() # se llama la funcion principal