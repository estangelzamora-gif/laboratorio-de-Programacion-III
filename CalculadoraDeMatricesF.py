import random

class Laboratorio2:

    # -------------------------
    # LEER MATRIZ
    # -------------------------
    def leer_matriz(self):

        filas = int(input("Filas: "))
        columnas = int(input("Columnas: "))

        matriz = []

        for i in range(filas):

            fila = []

            for j in range(columnas):

                num = float(input(f"Elemento [{i}][{j}]: "))
                fila.append(num)

            matriz.append(fila)

        return matriz, filas, columnas


    # -------------------------
    # SUMA MATRICES
    # -------------------------
    def suma_matrices(self):

        print("Matriz A")
        A,f1,c1 = self.leer_matriz()

        print("Matriz B")
        B,f2,c2 = self.leer_matriz()

        if f1 != f2 or c1 != c2:
            print("No se pueden sumar")
            return

        C = []

        for i in range(f1):

            fila = []

            for j in range(c1):

                fila.append(A[i][j] + B[i][j])

            C.append(fila)

        print("Resultado")

        for fila in C:
            print(fila)


    # -------------------------
    # PRODUCTO MATRICES
    # -------------------------
    def producto_matrices(self):

        print("Matriz A")
        A,f1,c1 = self.leer_matriz()

        print("Matriz B")
        B,f2,c2 = self.leer_matriz()

        if c1 != f2:
            print("No se pueden multiplicar")
            return

        C = []

        for i in range(f1):

            fila = []

            for j in range(c2):

                suma = 0

                for k in range(c1):

                    suma += A[i][k] * B[k][j]

                fila.append(suma)

            C.append(fila)

        print("Resultado")

        for fila in C:
            print(fila)


    # -------------------------
    # MATRIZ POR VECTOR
    # -------------------------
    def matriz_vector(self):

        A,f,c = self.leer_matriz()

        vector = []

        for i in range(c):

            num = float(input(f"Vector elemento {i}: "))
            vector.append(num)

        resultado = []

        for i in range(f):

            suma = 0

            for j in range(c):

                suma += A[i][j] * vector[j]

            resultado.append(suma)

        print("Resultado:",resultado)


    # -------------------------
    # INVERSA 2x2
    # -------------------------
    def inversa(self):

        A,f,c = self.leer_matriz()

        if f != 2 or c != 2:
            print("Solo funciona para matriz 2x2")
            return

        det = A[0][0]*A[1][1] - A[0][1]*A[1][0]

        if det == 0:
            print("No tiene inversa")
            return

        inv = [
            [A[1][1]/det , -A[0][1]/det],
            [-A[1][0]/det , A[0][0]/det]
        ]

        print("Inversa")

        for fila in inv:
            print(fila)


    # =========================
    # ORDENAMIENTOS
    # =========================

    def burbuja(self,lista):

        n=len(lista)

        for i in range(n):

            for j in range(n-1):

                if lista[j] > lista[j+1]:

                    aux = lista[j]
                    lista[j] = lista[j+1]
                    lista[j+1] = aux

        return lista


    def insercion(self,lista):

        for i in range(1,len(lista)):

            actual = lista[i]
            j=i-1

            while j>=0 and lista[j] > actual:

                lista[j+1] = lista[j]
                j -=1

            lista[j+1] = actual

        return lista


    def seleccion(self,lista):

        n=len(lista)

        for i in range(n):

            min=i

            for j in range(i+1,n):

                if lista[j] < lista[min]:

                    min=j

            aux = lista[i]
            lista[i] = lista[min]
            lista[min] = aux

        return lista


    def mergesort(self,lista):

        if len(lista) > 1:

            mitad=len(lista)//2
            izq=lista[:mitad]
            der=lista[mitad:]

            self.mergesort(izq)
            self.mergesort(der)

            i=j=k=0

            while i < len(izq) and j < len(der):

                if izq[i] < der[j]:
                    lista[k]=izq[i]
                    i+=1
                else:
                    lista[k]=der[j]
                    j+=1

                k+=1

            while i < len(izq):
                lista[k]=izq[i]
                i+=1
                k+=1

            while j < len(der):
                lista[k]=der[j]
                j+=1
                k+=1

        return lista


    # =========================
    # MENU MATRICES
    # =========================

    def menu_matrices(self):

        while True:

            print("\nOPERACIONES MATRICES")
            print("1 Sumar matrices")
            print("2 Producto matrices")
            print("3 Inversa")
            print("4 Matriz por vector")
            print("5 Volver")

            op=input("Opcion: ")

            match op:

                case "1":
                    self.suma_matrices()

                case "2":
                    self.producto_matrices()

                case "3":
                    self.inversa()

                case "4":
                    self.matriz_vector()

                case "5":
                    break

                case _:
                    print("Opcion invalida")


    # =========================
    # MENU ORDENAMIENTO
    # =========================

    def menu_ordenamiento(self):

        n=int(input("Cantidad de numeros: "))

        lista=[random.uniform(0,100) for i in range(n)]

        print("Lista original:",lista)

        print("Burbuja:",self.burbuja(lista.copy()))
        print("Insercion:",self.insercion(lista.copy()))
        print("Seleccion:",self.seleccion(lista.copy()))
        print("MergeSort:",self.mergesort(lista.copy()))

        lista2=lista.copy()
        lista2.sort()

        print("Sort Python:",lista2)


    # =========================
    # MENU PRINCIPAL
    # =========================

    def menu(self):

        while True:

            print("\nLABORATORIO 2")
            print("1 Operaciones con matrices")
            print("2 Ordenamientos")
            print("3 Salir")

            op=input("Seleccione: ")

            match op:

                case "1":
                    self.menu_matrices()

                case "2":
                    self.menu_ordenamiento()

                case "3":
                    print("Programa terminado")
                    break

                case _:
                    print("Opcion invalida")


if __name__ == "__main__":

    app=Laboratorio2()
    app.menu()