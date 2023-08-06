<div class="document">

<div class="documentwrapper">

<div class="bodywrapper">

<div class="body" role="main">

<div class="section" id="welcome-to-pydbod-s-documentation">

# Welcome to PyDBOD’s documentation![¶](#welcome-to-pydbod-s-documentation "Enlazar permanentemente con este título")

</div>

<div class="section" id="introduccion">

# Introduccion[¶](#introduccion "Enlazar permanentemente con este título")

Bienvenido a PyDBOD, la biblioteca de Python para la detección de anomalías usando algoritmos basados en distancias. En esta bibliotica tienes una amplia selección de algoritmos los cuales vamos a documentar a continuación. El uso de todos se reduce a la creación de un objeto de la clase respectiva y el uso del método **fit_predict**.

Para instalar el paquete o obtener una distribución usar el repositorio en github o en PyPI:

<https://github.com/miki97/TFG-OutlierDetection>

<https://pypi.org/project/PyDBOD/>

</div>

<div class="section" id="lof">

# LOF[¶](#lof "Enlazar permanentemente con este título")

Local Outlier Factor (LOF), o en español factor de valor atı́pico local, es una cuantificación del valor atı́pico de un punto perteneciente al conjunto de datos. Esta cuantificación es capaz de ajustar las variaciones en las densidades locales.

<dl class="function">

<dt id="LOF"> LOF <span class="sig-paren">(</span>_k = 20_<span class="sig-paren">)</span>[¶](#LOF "Enlazar permanentemente con esta definición")</dt>

<dd>

Constructor para la creación del objeto de la clase LOF.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

**int** – k, número de k vecinos a calcular

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

objeto de la clase LOF

</dd>

</dl>

</dd>

</dl>

<dl class="function">

<dt id="fit_predict"> fit_predict<span class="sig-paren">(</span>_data_<span class="sig-paren">)</span>[¶](#fit_predict "Enlazar permanentemente con esta definición")</dt>

<dd>

Método para aplicar el algoritmo LOF a una matriz de datos.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

**numpy.array** – data, matriz de datos

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

numpy.array de puntuaciones de anomalía

</dd>

</dl>

</dd>

</dl>

</div>

<div class="section" id="loop">

# LOOP[¶](#loop "Enlazar permanentemente con este título")

Local Outlier Probability (LoOP), esta técnica combina varios conceptos. En primer lugar, la idea de localidad, los algoritmos basados en densidad como LOF. Por otro lado, LOCI con conceptos probabilı́sticos.

<dl class="function">

<dt id="LOOP"> LOOP <span class="sig-paren">(</span>_k = 20_, _lamda=3_<span class="sig-paren">)</span>[¶](#LOOP "Enlazar permanentemente con esta definición")</dt>

<dd>

Constructor para la creación del objeto de la clase LOOP.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

*   **int** – k, número de k vecinos a calcular

*   **int** – lamda, párametro para regular la normalización

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

objeto de la clase LOOP

</dd>

</dl>

</dd>

</dl>

<dl class="function">

<dt> fit_predict <span class="sig-paren">(</span>_data_<span class="sig-paren">)</span></dt>

<dd>

Método para aplicar el algoritmo LOOP a una matriz de datos.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

**numpy.array** – data, matriz de datos

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

numpy.array de probabilidad anomalia [0-1]

</dd>

</dl>

</dd>

</dl>

</div>

<div class="section" id="ldof">

# LDOF[¶](#ldof "Enlazar permanentemente con este título")

Local Outlier Probability (LoOP), utiliza la distancia relativa de un objeto a sus vecinos para medir la cantidad de objetos que se desvıían de su vecindario disperso.

<dl class="function">

<dt id="LDOF"> LDOF <span class="sig-paren">(</span>_k = 20_<span class="sig-paren">)</span>[¶](#LDOF "Enlazar permanentemente con esta definición")</dt>

<dd>

Constructor para la creación del objeto de la clase LDOF.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

**int** – k, número de k vecinos a calcular

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

objeto de la clase LOOP

</dd>

</dl>

</dd>

</dl>

<dl class="function">

<dt> fit_predict <span class="sig-paren">(</span>_data_<span class="sig-paren">)</span></dt>

<dd>

Método para aplicar el algoritmo LDOF a una matriz de datos.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

**numpy.array** – data, matriz de datos

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

numpy.array de puntuaciones de anomalía

</dd>

</dl>

</dd>

</dl>

</div>

<div class="section" id="pinn-lof">

# PINN-LOF[¶](#pinn-lof "Enlazar permanentemente con este título")

Projection-Indexed Nearest-Neighbour (PINN), en este algoritmo se propone un método de detección de valores atı́picos locales proyectivo basado en LOF.

<dl class="function">

<dt> PINN-LOF(k = 20, t=2, s=1, h=20) </dt>

<dd>

Constructor para la creación del objeto de la clase PINN-LOF.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

*   **int** – k, número de k vecinos a calcular

*   **int** – t, probabilidad de seleccion de caracteristicas para la proyección

*   **int** – s, probabilidad de selección para la proyección

*   **int** – h, número de k vecinos a calcular en la proyección

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

objeto de la clase PINN-LOF

</dd>

</dl>

</dd>

</dl>

<dl class="function">

<dt> fit_predict <span class="sig-paren">(</span>_data_<span class="sig-paren">)</span></dt>

<dd>

Método para aplicar el algoritmo PINN-LOF a una matriz de datos.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

**numpy.array** – data, matriz de datos

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

numpy.array de puntuaciones de anomalía

</dd>

</dl>

</dd>

</dl>

</div>

<div class="section" id="outres">

# OUTRES[¶](#outres "Enlazar permanentemente con este título")

Outres es un algoritmo que propone desarrollar una puntuación de anomalı́as basada en la desviación de objetos en las proyecciones subespaciales. Para la selección de dichos subespacios se analiza la uniformidad de los datos en ellos.

<dl class="function">

<dt id="OUTRES"> OUTRES <span class="sig-paren">(</span>_epsilon=15_, _alpha=0.01_<span class="sig-paren">)</span>[¶](#OUTRES "Enlazar permanentemente con esta definición")</dt>

<dd>

Constructor para la creación del objeto de la clase OUTRES.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

*   **int** – epsilon, radio para la selección del vecindario

*   **float** – alpha, limite de uniformidad que se permite como interesante

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

objeto de la clase OUTRES

</dd>

</dl>

</dd>

</dl>

<dl class="function">

<dt> fit_predict <span class="sig-paren">(</span>_data_<span class="sig-paren">)</span></dt>

<dd>

Método para aplicar el algoritmo OUTRES a una matriz de datos.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

**numpy.array** – data, matriz de datos

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

numpy.array de puntuaciones de anomalía

</dd>

</dl>

</dd>

</dl>

</div>

<div class="section" id="odin">

# ODIN[¶](#odin "Enlazar permanentemente con este título")

Outlier Detection using Indegree Number (ODIN),es un algoritmo que hace uso del grafico de los k-vecinos más cercanos y usa el grado de los nodos para el calculo de anomalías

<dl class="function">

<dt id="ODIN"> ODIN <span class="sig-paren">(</span>_k=20_, _t=0.01_<span class="sig-paren">)</span>[¶](#ODIN "Enlazar permanentemente con esta definición")</dt>

<dd>

Constructor para la creación del objeto de la clase ODIN.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

*   **int** – k, número de k vecinos a calcular

*   **int** – t, umbral de dicisión

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

objeto de la clase ODIN

</dd>

</dl>

</dd>

</dl>

<dl class="function">

<dt> fit_predict <span class="sig-paren">(</span>_data_<span class="sig-paren">)</span></dt>

<dd>

Método para aplicar el algoritmo ODIN a una matriz de datos.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

**numpy.array** – data, matriz de datos

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

numpy.array de decisión 1-0

</dd>

</dl>

</dd>

</dl>

</div>

<div class="section" id="meandist">

# MeanDIST[¶](#meandist "Enlazar permanentemente con este título")

El algoritmo MeanDIST usa la la media de las distancias en su vecindario para ordenar a los vérticesy seleccionar los que más se desvian.

<dl class="function">

<dt id="MeanDIST"> MeanDIST <span class="sig-paren">(</span>_k=20_, _t=1.5_<span class="sig-paren">)</span>[¶](#MeanDIST "Enlazar permanentemente con esta definición")</dt>

<dd>

Constructor para la creación del objeto de la clase MeanDIST.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

*   **int** – k, número de k vecinos a calcular

*   **int** – t, parámatro para ampliar o reducir el umbral.

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

objeto de la clase MeanDIST

</dd>

</dl>

</dd>

</dl>

<dl class="function">

<dt> fit_predict <span class="sig-paren">(</span>_data_<span class="sig-paren">)</span></dt>

<dd>

Método para aplicar el algoritmo MeanDIST a una matriz de datos.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

**numpy.array** – data, matriz de datos

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

numpy.array de decisión 1-0

</dd>

</dl>

</dd>

</dl>

</div>

<div class="section" id="kdist">

# KDIST[¶](#kdist "Enlazar permanentemente con este título")

El algoritmo KDIST el máximo de las distancias a sus k-vecinos más cercanos para ordenar a los vértices y seleccionar los que más se desvian.

<dl class="function">

<dt id="KDIST"> KDIST <span class="sig-paren">(</span>_k=20_, _t=1.5_<span class="sig-paren">)</span>[¶](#KDIST "Enlazar permanentemente con esta definición")</dt>

<dd>

Constructor para la creación del objeto de la clase KDIST.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

*   **int** – k, número de k vecinos a calcular

*   **int** – t, parámatro para ampliar o reducir el umbral.

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

objeto de la clase KDIST

</dd>

</dl>

</dd>

</dl>

<dl class="function">

<dt> fit_predict <span class="sig-paren">(</span>_data_<span class="sig-paren">)</span></dt>

<dd>

Método para aplicar el algoritmo KDIST a una matriz de datos.

<dl class="field-list simple">

<dt class="field-odd">Parámetros</dt>

<dd class="field-odd">

**numpy.array** – data, matriz de datos

</dd>

<dt class="field-even">Tipo del valor devuelto</dt>

<dd class="field-even">

numpy.array de decisión 1-0

</dd>

</dl>

</dd>

</dl>

<dl class="function">

<dt id="enumerate"> enumerate <span class="sig-paren">(</span>_sequence_<span class="optional">[</span>, _start=0_<span class="optional">]</span><span class="sig-paren">)</span>[¶](#enumerate "Enlazar permanentemente con esta definición")</dt>

</dl>

*   [<span class="std std-ref">Índice</span>](genindex.html)

*   [<span class="std std-ref">Índice de Módulos</span>](py-modindex.html)

*   [<span class="std std-ref">Página de Búsqueda</span>](search.html)

</div>

</div>

</div>

</div>

<div class="sphinxsidebar" role="navigation" aria-label="main navigation">

<div class="sphinxsidebarwrapper">

# [PyDBOD](#)

### Navegación

<div class="relations">

### Related Topics

*   [Documentation overview](#)

</div>

<div id="searchbox" style="display: none" role="search">

### Búsqueda rápida

<div class="searchformwrapper">

<form class="search" action="search.html" method="get"><input type="text" name="q"> <input type="submit" value="Ir a"></form>

</div>

</div>

<script type="text/javascript">$('#searchbox').show(0);</script></div>

</div>

</div>

<div class="footer">©2019, Miguel Ángel López Robles. | Powered by [Sphinx 2.0.1](http://sphinx-doc.org/) & [Alabaster 0.7.12](https://github.com/bitprophet/alabaster) | [Page source](_sources/index.rst.txt)</div>
