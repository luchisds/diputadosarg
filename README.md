# DIPUTADOSARG

Este es un proyecto open-source que busca crear y mantener actualizada un API REST con la información dispionible en el sitio www.diputados.gov.ar en cuanto a la planta actual de diputados nacionales, sus proyectos y presentismo.

La idea es agregar a futuro las votaciones por diputado.



Mucha de la informacion relevante en el sitio www.diputados.gov.ar se encuentra en formato PDF que dificulta el acceso a los datos sin antes extraer los datos de cada uno de estos archivos. Para estos casos utilizo la herramienta TABULA (https://github.com/tabulapdf/tabula)

Los datos disponibles en las paginas HTML se obtienen mediante tecnicas de scrapping de datos.

Utilizo el lenguaje PYTHON y el framework Django.