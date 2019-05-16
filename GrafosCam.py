from tkinter import *
import math

#GRAFO LINEA INVERSO
#ALGORITMO PARA OBTENER UN GRAFO LINEA INVERSO

ventana = Tk()
ventana.geometry('1200x500')

lienzo = Canvas(ventana, width = 1200, height = 500, bg = 'white')
lienzo.place(x=0,y=0)

origen=[250]

radioExterno=[250]

nodos=[]
nodos1=[]

lista_x = []
lista_y = []
def identificar_puntos(recoleccion, contador):
    if(contador == 0):
        if(((recoleccion[0]**2) + (recoleccion[1]**2) >= (radioExterno[0]**2)-1) and ((recoleccion[0]**2) + (recoleccion[1]**2) <= (radioExterno[0]**2)+1)):
            lista_x.append(recoleccion[0])
            lista_y.append(recoleccion[1])
        recoleccion.pop(1)
                    
    else:
        iterador = 0
        while(iterador <= radioExterno[0]):
            recoleccion.append(iterador)
            identificar_puntos(recoleccion, (contador - 1))
            iterador += 0.141
        recoleccion.clear()

lista_x_polarizada = []
lista_y_polarizada = []
def polarizar():
    for e in range(len(lista_x) - 1, -1, -1):
        lista_x_polarizada.append((lista_x[e]))
        lista_y_polarizada.append(-(lista_y[e]))
    for i in range(0, len(lista_x), 1):
        lista_x_polarizada.append(-(lista_x[i]))
        lista_y_polarizada.append(-(lista_y[i]))
    for u in range(len(lista_x) - 1, -1, -1):
        lista_x_polarizada.append(-(lista_x[u]))
        lista_y_polarizada.append((lista_y[u]))
    for a in range(0, len(lista_x), 1):
        lista_x_polarizada.append(lista_x[a])
        lista_y_polarizada.append(lista_y[a])


lista_codigos_interseccion=["",""]
def generar_codigos_interseccion(labelA, labelB):
    lista_codigos_interseccion[0]=str(labelB)+str(labelA)+str(labelB)+str(labelA)
    lista_codigos_interseccion[1]=str(labelA)+str(labelB)+str(labelA)+str(labelB)
    
def findPosMin(lista):
    indice=0
    mini=max(lista)
    pos=0
    while(indice<(len(lista))):
        if(lista[indice]<mini):
            pos=indice
            mini=lista[indice]
            indice=0
            
        else:indice+=1

    return pos

def mayor_menor(nodoA,nodoB):
    lista=[nodoA.index_der,nodoA.index_izq,nodoB.index_der,nodoB.index_izq]
    lista1=[nodoA.identificador,nodoA.identificador,nodoB.identificador,nodoB.identificador]
    listas=[]
    listas1=[]
    for a in range(0,len(lista)):
        pos_minimo=findPosMin(lista)
        listas.append(lista[pos_minimo])
        listas1.append(lista1[pos_minimo])
        lista.pop(pos_minimo)
        lista1.pop(pos_minimo)

    return listas1

def identificar_interseccion(nodoA, nodoB):
    generar_codigos_interseccion(nodoA.identificador, nodoB.identificador)
    lista_mayor_menor=mayor_menor(nodoA, nodoB)
    codigo=""
    while(not(len(lista_mayor_menor)==0)):
        codigo+=str(lista_mayor_menor[0])
        lista_mayor_menor.pop(0)    

    lista_mayor_menor.clear()
    if(codigo in lista_codigos_interseccion): return True
    else: return False

class nodo:
    def __init__(self,radio,identificador,index,index1):
        self.index1=index1
        self.radio=radio
        self.diferencia=90-(self.radio/(radioExterno[0]/90))
        self.index=int(index%360)
        self.index_der=int((self.index+self.diferencia)%360)
        self.index_izq=int((self.index-self.diferencia)%360)
        self.identificador=identificador
        self.vecindario=[]

def actualizar_nodos(indice):
    for nodo in range(0,len(nodos)):
        NODO=nodos[nodo]
        if(abs(NODO.index-indice)<=50):
            if(indice > NODO.index):
                NODO.index=(NODO.index-5)%360
                NODO.index_der=(NODO.index_der-5)%360
                NODO.index_izq=(NODO.index_izq-5)%360
            else:
                NODO.index=(NODO.index+5)%360
                NODO.index_der=(NODO.index_der+5)%360
                NODO.index_izq=(NODO.index_izq+5)%360

        lienzo.create_line(lista_x_polarizada[NODO.index_der]+origen[0],lista_y_polarizada[NODO.index_der]+origen[0],lista_x_polarizada[NODO.index_izq]+origen[0],lista_y_polarizada[NODO.index_izq]+origen[0])

def graficar_interseccion(nodoA,nodoB):
    index1=nodoA.index
    index2=nodoB.index

    lienzo.create_line(lista_x_polarizada[int(nodoA.index1)]+origen[0]+600,lista_y_polarizada[int(nodoA.index1)]+origen[0],lista_x_polarizada[int(nodoB.index1)]+origen[0]+600,lista_y_polarizada[int(nodoB.index1)]+origen[0])

    radio=(nodoA.radio+50) #Cambio aqui(radio+=50)!

    diferencia=abs(index2-index1)
    if(diferencia<(360-diferencia)):
        distancia=diferencia
        if(index2>index1): index_interseccion=(index1+(distancia/2))%360
        else: index_interseccion=(index2+(distancia/2))%360
    else:
        distancia=(360-diferencia)
        if(index2<index1): index_interseccion=(index1+(distancia/2))%360
        else: index_interseccion=(index2+(distancia/2))%360

    index_interseccion=int(index_interseccion)

    normaA=math.sqrt((lista_x_polarizada[index1]**2)+(lista_y_polarizada[index1]**2))
    normaB=math.sqrt((lista_x_polarizada[index2]**2)+(lista_y_polarizada[index2]**2))
    dividendo=((lista_x_polarizada[index1]*lista_x_polarizada[index2])+(lista_y_polarizada[index1]*lista_y_polarizada[index2]))

    if(not(dividendo/(normaA*normaB)>1)):
        angulo=math.acos(dividendo/(normaA*normaB))
        angle=angulo/2
        
        dist_punt=radio/(math.cos(angle))

        norma_punto_interseccion=math.sqrt((lista_x_polarizada[index_interseccion]**2)+(lista_y_polarizada[index_interseccion]**2))
        VECTORUNIX=(lista_x_polarizada[index_interseccion]/norma_punto_interseccion)
        VECTORUNIY=(lista_y_polarizada[index_interseccion]/norma_punto_interseccion)

        #lienzo.create_line(origen[0],origen[0],(VECTORUNIX*dist_punt)+origen[0],(VECTORUNIY*dist_punt)+origen[0])
        lienzo.create_oval((VECTORUNIX*dist_punt)+origen[0]-5,(VECTORUNIY*dist_punt)+origen[0]-5,(VECTORUNIX*dist_punt)+origen[0]+5,(VECTORUNIY*dist_punt)+origen[0]+5, fill='black')

    else:
        nodoA.index=(nodoA.index+10)%360
        nodoB.index=(nodoB.index-10)%360
        nodoA.index_der=(nodoA.index_der+10)%360
        nodoB.index_der=(nodoB.index_der-10)%360
        nodoA.index_izq=(nodoA.index_izq+10)%360
        nodoB.index_izq=(nodoB.index_izq-10)%360
    
def actualizar_aristas():
    for nodoA in range(0,len(nodos)):
        for nodoB in range(0,len(nodos)):
            if(not(nodoA==nodoB)):
                NODOA=nodos[nodoA]
                NODOB=nodos[nodoB]
                if(identificar_interseccion(NODOA,NODOB)):
                    graficar_interseccion(NODOA,NODOB)
                    NODOA.vecindario[nodoB]=1
                else: NODOA.vecindario[nodoB]=0

def Bipartite(listaListas):
    nums=[]
    for i in range(0,len(nodos),1):
        nums.append(i)
    
    for a in range(0,len(listaListas),1):
        lista=listaListas[a]
        contenedor=[]
        for b in range(0,len(lista),1):
            if(lista[b]==1): contenedor.append(b)

        for b in range(0,len(contenedor),1):
            for c in range(0,len(contenedor),1):
                x=contenedor[b]
                y=contenedor[c]
                if(x in nums and y in nums):
                    if(listaListas[x][y]==1):
                        print("NO bipartito")
                        return False
    print("bipartito")
    return True

def Bipartition():
    iden_nodos=[]
    for nodo in nodos:
        iden_nodos.append(nodo.identificador)

    A,B=[],[]
    vecindario=nodos[0].vecindario
    for a in range(0,len(vecindario),1):
        if(vecindario[a]==1):
            print("1")
            B.append(iden_nodos[a])
        else:
            print("2")
            A.append(iden_nodos[a])
    return (A,B)

def Button(event):
    listaListas=[]
    for a in range(0,len(nodos),1):
        lista=['.' for i in range(0,a,1)]
        for b in range(a,len(nodos[a].vecindario),1):
            lista.append(nodos[a].vecindario[b])
        listaListas.append(lista)

    A,B=[],[]
    if(Bipartite(listaListas)): A,B=Bipartition()
    print(A)
    print(B)
                  
def Motion(event):
    x=(event.x-origen[0])
    y=-(event.y-origen[0])

    theta=math.atan(y/x)

    if(x<0): theta+=math.pi
    elif(y<0 and x>0): theta+=(2*math.pi)

    alpha=str(theta/(1.57/90))

    num=""
    index=0

    while(alpha[index]!="."):
        num+=alpha[index]
        index+=1

    indice=int(int(num)/(360/len(lista_x_polarizada)))
    indice=(indice%360)

    lienzo.delete(ALL)
    actualizar_nodos(indice)
    actualizar_aristas()
    
    lienzo.create_oval(0,0,500,500)
    for a in nodos:
        lienzo.create_oval(lista_x_polarizada[int(a.index1)]-5+origen[0]+600,lista_y_polarizada[int(a.index1)]-5+origen[0],lista_x_polarizada[int(a.index1)]+5+origen[0]+600,lista_y_polarizada[int(a.index1)]+5+origen[0])
        
#--------------------------------------------------------------------------¡BEGINNING OF EXECUTION!-------------------------------------------------------------------#

#Ejemplo de 36 nodos
nom_nodos=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']#,'1','2','3','4','5','6','7','8','9','0','A']
pos_nodos=[0,90,260,180,140,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260]#,270,280,290,300,310,320,330,340,350,360]

for a in range(0,len(nom_nodos),1):
    nodos.append(nodo(100,nom_nodos[a],pos_nodos[a],0))

for nodo in nodos:
    nodo.vecindario=[nodo.identificador for nodo in nodos]

for nodo in nodos:
    print(nodo.vecindario)

aumento=(360/len(nodos))%360
indice=0
for a in nodos:
    a.index1=(indice%360)
    indice+=aumento

#Esteban Hernandez Ramirez
#Proyecto de grafos

identificar_puntos([],2)
polarizar()

lienzo.bind('<Motion>',Motion)
lienzo.bind('<Button>',Button)
ventana.mainloop()
