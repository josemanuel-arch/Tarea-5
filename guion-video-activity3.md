# Guion cronometrado para el video (Activity 3)

La consigna pide un video (.mp4) de máximo 3 minutos donde el programa se
ejecute y expliques brevemente la entrada y la salida. Puedes narrar en
español (la salida del programa está en inglés y se entiende igual).

## Cómo usarlo
- Graba el audio de corrido, a un ritmo cómodo. Apunta a 1:15 a 1:45 min.
- Los tiempos entre corchetes son solo una referencia para que tus palabras
  coincidan con lo que va apareciendo en pantalla. No tienes que ser exacto.
- Después me mandas el audio (.mp3, .m4a o .wav) y yo lo sincronizo con el video.

## Qué se ve en pantalla (video que ya tienes)
- 0:00 terminal vacía
- 0:01 a 0:10 se escribe el comando `javac ...`
- 0:10 compila, sin errores
- 0:11 a 0:13 se escribe `java HospitalTest`
- 0:13 a 0:17 aparece la salida
- 0:17 en adelante queda la salida completa en pantalla

## Narración

**[0:00, terminal vacía]**
"Hola, soy José Manuel Rodríguez Cantú. Les muestro la evidencia de la
Activity 3, el diseño de una jerarquía de clases para el sistema de un
hospital en Java."

**[~0:04, mientras se escribe el comando javac]**
"Primero compilo las cinco clases del proyecto con javac: Person, Doctor,
Patient, Guard y la clase de prueba, HospitalTest."

**[~0:10, cuando termina de compilar]**
"La compilación termina sin errores ni advertencias."

**[~0:11, mientras se escribe java HospitalTest]**
"Enseguida ejecuto el programa con java HospitalTest."

**[~0:13, cuando aparece la salida]**
"Y esta es la salida del programa."

**[~0:17 en adelante, con toda la salida en pantalla]**
"El diseño parte de una clase abstracta, Person, que guarda los datos
comunes, el nombre y la edad, y define un método abstracto llamado register.
De ella heredan tres subclases, y en la salida se ve cada una: el doctor
Joseph, de 41 años, del departamento de Neurología; el paciente Richard, de
78 años, con dolor de cabeza crónico; y dos guardias. El guardia John se creó
sin teléfono, por eso aparece como not provided, mientras que Kevin se creó
con teléfono y sí lo muestra. Ahí se ve la sobrecarga de constructores: la
clase Guard se puede crear de dos formas. Además, cada persona imprime un
saludo distinto, Welcome Doctor, Welcome Patient o Welcome Guard, porque cada
subclase sobrescribe el método register, y eso es el polimorfismo. Con este
ejercicio quedan demostradas la herencia, la abstracción y la sobrecarga.
Gracias."

## Salida esperada (para que confirmes que quedó bien)

```
=== Hospital registration system ===

Doctor
  Name: Joseph
  Age: 41
  Department: Neurologist
Welcome Doctor!

Patient
  Name: Richard
  Age: 78
  Illness: Chronic Headache
Welcome Patient!

Guard
  Name: John
  Age: 39
  Shift: Morning
  Phone: not provided
Welcome Guard!

Guard
  Name: Kevin
  Age: 43
  Shift: Afternoon
  Phone: +52 232 456345
Welcome Guard!
```
