"""
Titulo: Lectura, procesamiento y dibujo de un archivo DEM
Autor: Felipe Godoy Cerca
Fecha: 26-05-2019

Descripcion:

Codigo realizado para la asignatura Analisis de Algoritmos, el cual consiste
en implementar la lectura y dibujo de un archivo DEM ( Digital
Elevation Model) obtenido desde el proyecto STRM (Shuttle Radar Topography
Mision), ademas, realizando el procesamiento para el dibujo de sombras.

Obtener dataset:
https://www2.jpl.nasa.gov/srtm/
https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/

Fuentes e informacion util:
https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
https://librenepal.com/article/reading-srtm-data-with-python/
http://desktop.arcgis.com/es/arcmap/10.3/tools/spatial-analyst-toolbox/how-hillshade-works.htm
https://www.neonscience.org/create-hillshade-py
https://matplotlib.org/examples/specialty_plots/topographic_hillshading.html
https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html


"""


import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource
from tqdm import tqdm

DATA_DIR = "data/" # Directorio para leer y guardar informacion
DATA_FILE = "S32W070.hgt" # Archivo .hgt que contiene DEM
LT_INIT = -32 # Latitud inicial del archivo .hgt
LON_INIT = -70 # Longitud inicial del archivo .hgt

SAMPLES = 1201 # 3601 para STRM1 - 1201 para STRM3
SECOND = 1/SAMPLES # Tamaño de paso entre una coordenada y otra
LGT_AZIMUT= 100 # Angulo azimut del sol
LGT_ELEVATION = 45 # Angulo de elevacion del sol
VER_EXAGERATION = 1 # Exageracion vertical para marcar sombras
FILE = os.path.join(DATA_DIR,DATA_FILE)

# Funcion que lee el archivo .hgt pasando los bytes de 16 bit en formato
# big-endesian retornando un array numpy
def read_elevation_from_file(hgt_file):
    print("Leyendo archivo ubicado en {}".format(hgt_file))
    with open(hgt_file, 'rb') as hgt_data:
        # Se leen bytes transformandolos a enteros de 16bits, finalmente convirtiendolo en matriz de 1201x1201
        elevations = np.fromfile(hgt_data, np.dtype('>i2'), SAMPLES*SAMPLES)\
                                                .reshape((SAMPLES, SAMPLES))
        return elevations

# Debido a que el archivo .hgt entrega valores vacios representados por un -32625
# se reemplazan por el promedio para mejorar la representacion, retornando un arreglo limpio
def clean_data(e):
    print("Limpiando datos incorrectos...")
    prev = np.ptp(e)
    mean = np.mean(e) #Se obtiene promedio de medidas
    for item in np.nditer(e, op_flags=['readwrite']):
        if item < 0:
            item[...] = mean
    print("Amplitud maxima antes de limpieza \t{}".format(prev))
    print("Amplitud maxima despues de la limpieza \t{}".format(np.ptp(e)))
    return e

# Funcion para crear el eje x e y para representarlo en 2D y 3D
def create_xy(init_lat,init_lon):
    x = np.arange(init_lat, init_lat+1, SECOND)
    y = np.arange(init_lon, init_lon+1, SECOND)

    return x,y

#Funcion opcional a la disponible en matplotlib, cumple la misma funcion recibiendo azimut y elevacion
def hillshade(array,azimuth,angle_altitude):
    azimuth = 360.0 - azimuth

    x, y = np.gradient(array)
    slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)
    azimuthrad = azimuth*np.pi/180.
    altituderad = angle_altitude*np.pi/180.

    shaded = np.sin(altituderad)*np.sin(slope) + np.cos(altituderad)*np.cos(slope)*np.cos((azimuthrad - np.pi/2.) - aspect)

    return 255*(shaded + 1)/2

# Funcion que permite dibujar los perfiles Norte-Sur (default) o Este-Oeste (invertir=true)
def plot_perfiles(data, invertir= False):
    fig1 = plt.figure()
    a = fig1.subplots()
    if invertir:
        c = e.T

    for line in np.arange(0,SAMPLES+1,20):
        a.plot(c[line])

    plt.show()

# Funcion que permite vizualizar el DEM en 2D y 3D
def plot_strm(x,y,e):
    # Se declara el tamaño de la ventana
    fig = plt.figure(figsize=(15,5))

    # Se extraen latitud y longitud minimas y maximas
    xmin,xmax,ymin,ymax = x[0],x[-1],y[0],y[-1]

    #Se declara fuente de luz con azimut y grado de elevacion
    ls = LightSource(LGT_AZIMUT, LGT_ELEVATION)

    #Se crea subplot para graficar DEM en 3D
    ax1 = fig.add_subplot(1,2,1,projection='3d')
    ax1.set_title("Proyeccion en 3D", y=1.08)
    ax1.set_zlim(0,np.amax(e))
    x, y = np.meshgrid(x, y)
    rgb = ls.shade(e,cmap=cm.gray, vert_exag=VER_EXAGERATION, blend_mode='soft')
    sup = ax1.plot_surface(x,y,e, facecolors=rgb, linewidth=0, antialiased = False, shade=False)

    #Se crea 2do subplot para graficar DEM en 2D
    ax2 = fig.add_subplot(1,2,2)
    ax2.set_title("Vista 2D", y=1.08)

    # Se transforma el DEM a hillshade utilizando el LighSource
    # vert_exag es la exageracion vertical
    l = ls.hillshade(e, vert_exag=10)

    # Permite vizualizar el DEM con sombras aplicadas, ademas de su ejes de latitud y longitud
    sup = ax2.imshow(l, cmap='gray', extent=[xmin, xmax, ymin, ymax])

    # Funcion que permite ver el DEM sin hillshade
    # ax2.matshow(e, interpolation="bilinear", origin="lower",cmap=cm.cividis, extent=[xmin, xmax, ymin, ymax])

    # Se define el titulo de ventana
    plt.suptitle("Vistas de STRM", fontsize=18)

    # Permite rotar la imagen 3D en 360
    # for angle in range(0, 360):
    #     ax1.view_init(30, angle)
    #     plt.draw()
    #     plt.pause(.01)

    fig.colorbar(sup, shrink=0.5, aspect=5)
    plt.show()
    fig.savefig("{}/results.png".format(DATA_DIR), bbox_inches='tight')

# Funcion que permite calcular las pendientes
# La idea era calcularlas para poder calcular sombras, pero no sirvio la idea xd
def calcular_pendiente(data):
    print("Calculando pendientes...")

    x = np.arange(SAMPLES)

    pendientes = []
    with tqdm(total=SAMPLES) as pbar:
        for line in data:
            p = []
            for i in range(len(line)-1):
                dy = (line[i+1]- line[i]) / (x[i+1]-x[i])
                p.append(dy)
            pendientes.append([p])
            pbar.update(1)

    return (np.array(pendientes).reshape((1201,1200)))


if __name__ == "__main__":
    e = read_elevation_from_file(FILE)
    e = clean_data(e)
    x,y = create_xy(LT_INIT,LON_INIT)

    plot_strm(x,y,e)