# Tarea 4 · Circuitos con compuertas lógicas y su aplicación

Materiales de la tarea: diseño del circuito lógico de una puerta electrónica
para una granja con tres botones (A, B y C).

## Contenido

| Archivo | Descripción |
|---|---|
| `Tarea4_Circuitos_con_compuertas_logicas.docx` | Reporte para entregar (carátula + 5 cuartillas + referencias) |
| `Tarea4_Circuitos_con_compuertas_logicas.pdf` | Vista previa en PDF del reporte |
| `comprobacion_puerta_granja.m` | Script de MATLAB que comprueba el diseño |
| `img/circuito_canonico.png` | Diagrama del circuito de la función canónica |
| `img/circuito_simplificado.png` | Diagrama del circuito simplificado (XNOR + AND) |

## Resumen del diseño

- Condiciones de apertura: 1) C pulsado con A y B en reposo; 2) A, B y C pulsados.
- Función canónica: `S = A'·B'·C + A·B·C`
- Función simplificada: `S = C · (A XNOR B)`

## Pendientes antes de entregar

1. Completar en la carátula: escuela/facultad, materia, nombre, matrícula y profesor.
2. Grabar el video de explicación y pegar el enlace en la sección 8.
3. Ejecutar `comprobacion_puerta_granja.m` en MATLAB para reproducir la comprobación.
4. Revisar el documento completo y hacerlo propio antes de enviarlo.
