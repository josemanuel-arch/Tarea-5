# Guion para el video de evidencia (Activity 3)

La consigna pide un video (.mp4) de máximo 3 minutos donde el programa se
ejecute y expliques brevemente los datos de entrada y salida. Este guion es
una guía; puedes narrarlo en inglés o en español, como te sientas más cómodo.

## Antes de grabar
1. Abre una terminal en la carpeta con los cinco archivos .java.
2. Ten a la vista los archivos y la terminal.
3. Comandos que vas a ejecutar:
   - `javac Person.java Doctor.java Patient.java Guard.java HospitalTest.java`
   - `java HospitalTest`

## Qué decir (aprox. 2 a 3 minutos)

**1. Presentación (15 s).**
"Hola, soy José Manuel Rodríguez Cantú. Esta es la evidencia de la Activity 3:
el diseño de una jerarquía de clases para un sistema de un hospital."

**2. Diseño de las clases (45 s).**
"Tengo una clase abstracta Person con los datos comunes, nombre y edad, y un
método abstracto register. De ella heredan tres subclases: Doctor, que agrega
el departamento; Patient, que agrega la enfermedad; y Guard, que agrega el
turno y, de forma opcional, un teléfono. Cada subclase reutiliza el
constructor de Person con super, y cada una implementa su propio register.
Guard tiene dos constructores sobrecargados: uno con teléfono y otro sin él."

**3. Compilación (20 s).**
Ejecuta `javac ...` y di:
"Compilo los cinco archivos con javac. No aparece ningún error ni advertencia."

**4. Ejecución y explicación de la salida (60 s).**
Ejecuta `java HospitalTest` y explica:
"Al correr el programa se crean cuatro personas. El Doctor Joseph, de 41 años,
del departamento de Neurología, imprime Welcome Doctor. El paciente Richard,
de 78 años, con Chronic Headache, imprime Welcome Patient. El guardia John, de
39 años, turno Morning, se crea con el constructor de tres parámetros, así que
su teléfono aparece como not provided. El guardia Kevin, de 43 años, turno
Afternoon, se crea con el constructor de cuatro parámetros y sí muestra su
teléfono. Cada persona imprime un saludo distinto porque register está
sobrescrito en cada subclase, que es el polimorfismo que pedía la actividad."

**5. Cierre (10 s).**
"Con esto se demuestran la herencia, la abstracción y la sobrecarga. Gracias."

## Salida esperada (para que verifiques que todo salió bien)

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
