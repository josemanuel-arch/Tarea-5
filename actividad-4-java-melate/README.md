# Actividad 4 · Melate en Java (Módulo 4: Clases y objetos)

Programa que genera los 7 números ganadores del sorteo Melate: aleatorios,
del 1 al 56 y sin repetidos.

## Contenido

| Archivo | Descripción |
|---|---|
| `Melate.java` | Código fuente comentado |
| `Melate.class` | Compilado (javac 21) |
| `melate.txt` | Ejemplo del archivo que genera el programa |
| `guion_video_melate.md` | Guion para el video de evidencia (máx. 3 min, .mp4) |
| `Caratula_Actividad4_Java.docx` | Carátula con el formato del curso (datos completos) |

## Cómo cumple los requisitos

- **Aleatorios con la librería estándar**: clase `Random` de `java.util`
  (`nextInt(56) + 1` da valores de 1 a 56).
- **Colección**: `ArrayList` llamado exactamente `numberList`; antes de
  agregar cada número se verifica con `contains` que no esté duplicado.
- **Persistencia**: la lista se guarda en `melate.txt` con `FileWriter`
  y `PrintWriter`.
- **Excepciones**: la escritura va en un `try-catch` que maneja
  `IOException`.
- **Código comentado** en todo el programa.

## Cómo compilar y ejecutar

```bash
javac Melate.java
java Melate
```

Probado con 300 ejecuciones seguidas: siempre 7 números, en rango y sin
duplicados.

## Pendientes antes de entregar

1. Grabar el video .mp4 (máximo 3 minutos) siguiendo `guion_video_melate.md`.
2. Subir `Melate.java`, `Melate.class` y el video en Brightspace y enviar.
