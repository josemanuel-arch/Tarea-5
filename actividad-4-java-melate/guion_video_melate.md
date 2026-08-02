# Guion del video · Actividad 4: Melate en Java

**Límite: 3 minutos máximo, formato .mp4.** El video debe mostrar el
programa corriendo, con descripción hablada de los datos de salida y las
conclusiones. Objetivo: 2 minutos y medio.

## Preparación

1. Abre `Melate.java` en tu editor (NetBeans, IntelliJ, VS Code o el que uses).
2. Ten una terminal lista en la carpeta del proyecto, o el botón Run del IDE.
3. Borra el archivo `melate.txt` si existe, para generarlo en vivo.
4. Graba la pantalla con audio (PowerPoint, Zoom u OBS) y **exporta a .mp4**.

## Guion

**[Pantalla: el código en el editor] (0:00 – 0:20)**

"Hola, soy José Manuel Rodríguez Cantú, matrícula 00612676. Esta es mi
Actividad 4 del Módulo 4 de Java: un programa que genera los 7 números
ganadores del Melate para la Lotería Nacional. Los números van del 1 al
56 y no pueden repetirse."

**[Pantalla: recorrer el código despacio] (0:20 – 1:10)**

"Les explico rápido el código. En el método generarNumeros uso la clase
Random del paquete java util, que es de la librería estándar de Java. El
método nextInt de 56 me da un número de 0 a 55, y le sumo 1 para que
quede entre 1 y 56. Los números los guardo en una colección: un ArrayList
que se llama numberList. Antes de agregar cada número, con el método
contains reviso que no esté repetido; si ya está, se genera otro.

Después, en el método guardarNumeros, guardo la lista en un medio
persistente: un archivo de texto que se llama melate punto txt, usando
las clases FileWriter y PrintWriter. Todo esto va dentro de un bloque
try-catch que atrapa la IOException, para que el programa no truene si
hay algún problema al abrir o escribir el archivo."

**[Pantalla: terminal o consola del IDE, ejecutar] (1:10 – 2:00)**

"Ahora lo ejecuto. Compilo con javac Melate punto java y lo corro con
java Melate... Y aquí está la salida: el programa imprime los 7 números
ganadores, por ejemplo estos que salieron ahorita, todos entre 1 y 56 y
sin repetirse, y el mensaje de que se guardaron en el archivo.

Lo corro una segunda vez... y salen números diferentes, porque son
aleatorios, pero siempre son 7 y nunca se repiten dentro del mismo
sorteo. Ahora abro el archivo melate punto txt... y aquí están guardados
los números de la última ejecución. Con esto queda la evidencia de que la
persistencia funciona."

**[Pantalla: el código o la salida] (2:00 – 2:30)**

"Como conclusión: en esta actividad usé cuatro cosas de Java. Las
colecciones, porque el ArrayList me deja guardar los números y revisar
duplicados muy fácil con contains; la librería estándar, con la clase
Random para los aleatorios; la persistencia, con FileWriter y PrintWriter
para dejar los resultados en un archivo de texto; y el manejo de
excepciones con try-catch, que evita que el programa falle si el archivo
no se puede abrir. Con esto el sistema cumple todo lo que pidió la
actividad. Gracias."

## Entrega (antes de hoy 23:00)

- [ ] `Melate.java` (el código fuente)
- [ ] `Melate.class` (el compilado)
- [ ] El video en formato **.mp4** (máximo 3 minutos)
- [ ] Subir los tres archivos en Brightspace y dar clic en **Enviar**
