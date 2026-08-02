# Guion del video · Tarea 4: Circuitos con compuertas lógicas

Duración objetivo: 4 minutos. Habla natural, sin leer palabra por palabra:
usa este guion como base y dilo con tus palabras.

## Preparación (antes de grabar)

1. Abre el reporte (PDF o Word) en pantalla completa.
2. Abre MATLAB con `comprobacion_puerta_granja.m` cargado y córrelo una vez
   para confirmar que jala.
3. Cierra notificaciones y otras ventanas.
4. Haz una pasada de ensayo cronometrada.

## Guion

**[Pantalla: carátula del reporte]**

"Hola, buenas tardes. Soy José Manuel Rodríguez Cantú, matrícula 00612676.
En este video les presento mi Tarea 4 del Módulo 4 de Álgebra Booleana,
que trata sobre circuitos con compuertas lógicas y su aplicación."

**[Pantalla: sección 3, análisis del problema]**

"El problema es el siguiente: en una granja me contratan para diseñar una
puerta electrónica que se abre con tres botones: A, B y C. La puerta solo
se abre en dos casos: cuando se pulsa únicamente C, con A y B sin pulsar,
o cuando se pulsan los tres botones al mismo tiempo. Uso el valor 1 para
botón pulsado, 0 para botón en reposo, y la salida X vale 1 cuando la
puerta se abre."

**[Pantalla: Tabla 2, la tabla de verdad]**

"Esta es la tabla de verdad con las ocho combinaciones posibles. Además de
las entradas A, B y C, agregué las columnas para evaluar la función: las
negaciones de A y de B, el término A prima B prima C, que es la condición
uno, y el término A B C, que es la condición dos. Como pueden ver, la
salida X solo vale 1 en dos renglones: el 0 0 1 y el 1 1 1. En todos los
demás la puerta queda cerrada."

**[Pantalla: sección 4, función y simplificación]**

"De esos dos renglones sale la función canónica: X igual a A prima por B
prima por C, más A por B por C. Para simplificarla apliqué álgebra de
Boole: los dos términos comparten la C, así que la factorizo y me queda X
igual a C por, entre paréntesis, A prima B prima más A B. Y esa expresión
del paréntesis es justo la definición de la compuerta XNOR, que vale 1
cuando A y B son iguales. Entonces la función mínima queda X igual a C por
A XNOR B. También lo comprobé con el mapa de Karnaugh: los dos unos no son
celdas adyacentes, por eso la reducción sale por factorización."

**[Pantalla: Figuras 1 y 2, los circuitos]**

"Aquí están los dos circuitos. El de la función canónica necesita cinco
compuertas: dos inversores, dos AND de tres entradas y una OR. En cambio,
el circuito simplificado solo necesita dos: una XNOR que compara A con B,
y una AND que combina ese resultado con C. Por eso mi propuesta es el
circuito simplificado: hace exactamente lo mismo con menos componentes,
menos conexiones y menos costo."

**[Pantalla: MATLAB, correr el script en vivo]**

"Para comprobar que las dos funciones son equivalentes hice este script en
MATLAB. Genera las ocho combinaciones, evalúa los términos de las dos
condiciones, la salida canónica y la simplificada... lo ejecuto... y aquí
está la tabla: coincide renglón por renglón con la del reporte, y la
función isequal me confirma que las dos expresiones dan lo mismo, o sea
que el diseño es correcto."

**[Pantalla: conclusiones del reporte]**

"Como conclusión, esta tarea me permitió ver cómo el álgebra booleana
convierte un requerimiento escrito, las condiciones para abrir una puerta,
en un circuito digital real. La tabla de verdad garantiza que el diseño
cumpla lo que se pide, la simplificación reduce el circuito de cinco a dos
compuertas, y la comprobación en software valida todo antes de armar el
circuito físico. Gracias."

## Paso a paso para grabar y entregar

1. **Graba**: PowerPoint (Grabar → Grabación de pantalla), Zoom (reunión
   solo tú + compartir pantalla + grabar) o grabación de pantalla del
   iPhone mostrando el PDF.
2. **Revisa** que se escuche tu voz y se lea la pantalla.
3. **Sube** el video a YouTube en modo **oculto** o a Google Drive con
   permiso "cualquier persona con el enlace puede ver".
4. **Prueba** el enlace en una ventana de incógnito.
5. **Pega** el enlace en la sección 8 del Word y guarda el documento.
6. **Pega el escudo** de la universidad en la carátula (cópialo de tu
   tarea anterior).
7. **Sube** el Word en Brightspace y da clic en **Enviar**.
