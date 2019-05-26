# STRM- Analisis-de-Algoritmos

## Descripcion
Codigo realizado para la asignatura Analisis de Algoritmos, el cual consiste
en implementar la lectura y dibujo de un archivo DEM ( Digital
Elevation Model) obtenido desde el proyecto STRM (Shuttle Radar Topography
Mision) realizado por la NASA, ademas, realizando el procesamiento para el dibujo de sombras.

## Instalacion

Tan solo se debe descargar el repositorio, existen tres
datasets cargados en la carpeta data, si desea cargar otro archivo
puedes obtenerlo desde el siguiente link

https://www2.jpl.nasa.gov/srtm/

https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/

### Requerimientos

El codigo ha sido diseñado y probado en Linux, se 
 requiere los siguientes paquetes:

```
Python 3.6
Numpy
Matplotlib
tqdm
```

Si tienes instalado conda o pip ejecuta el siguiente comando
```
pip install numpy matplotlib tqdm

or

conda install numpy matplotlib tqdm
```

## Ejecucion

Una vez instalados los paquetes necesarios ejecuta el siguiente comando:
```
# Por defecto abrira el archivo S33W070.hgt
python app.py
```

#### Opcional:
```
# Puedes indicar la ruta del archivo que tu desees
python app.py data/S05W070.hgt
```

## Resultados

![Resultado] (https://github.com/felipegodoycc/STRM-Analisis-de-Algoritmo/blob/master/data/result-S33W070.png)

### Fuentes e informacion de utilidad

https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
https://librenepal.com/article/reading-srtm-data-with-python/
http://desktop.arcgis.com/es/arcmap/10.3/tools/spatial-analyst-toolbox/how-hillshade-works.htm
https://www.neonscience.org/create-hillshade-py
https://matplotlib.org/examples/specialty_plots/topographic_hillshading.html
https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html