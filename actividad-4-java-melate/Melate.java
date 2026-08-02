import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Random;

/**
 * Actividad 4 - Modulo 4: Clases y objetos en Java
 * Genera los 7 numeros ganadores del sorteo Melate de la Loteria Nacional.
 * Los numeros son aleatorios, van del 1 al 56 y no pueden repetirse.
 * La lista se guarda en un archivo de texto usando FileWriter y PrintWriter.
 */
public class Melate {

    // Cantidad de numeros ganadores y valor maximo permitido
    private static final int CANTIDAD_NUMEROS = 7;
    private static final int NUMERO_MAXIMO = 56;

    public static void main(String[] args) {
        // Se genera la lista con los 7 numeros sin repetir
        ArrayList<Integer> numberList = generarNumeros();

        // Se muestran los numeros en la consola
        System.out.println("Numeros ganadores del Melate: " + numberList);

        // Se guarda la lista en un archivo de texto (medio persistente)
        guardarNumeros(numberList, "melate.txt");
    }

    /**
     * Genera los numeros aleatorios entre 1 y 56 usando la clase Random
     * de la libreria estandar (java.util). Antes de guardar cada numero
     * en el ArrayList se revisa que no este repetido.
     */
    public static ArrayList<Integer> generarNumeros() {
        ArrayList<Integer> numberList = new ArrayList<>();
        Random random = new Random();

        // Se repite hasta juntar los 7 numeros diferentes
        while (numberList.size() < CANTIDAD_NUMEROS) {
            // nextInt(56) da un valor de 0 a 55; se suma 1 para tener de 1 a 56
            int numero = random.nextInt(NUMERO_MAXIMO) + 1;

            // Solo se agrega si el numero no esta ya en la lista
            if (!numberList.contains(numero)) {
                numberList.add(numero);
            }
        }
        return numberList;
    }

    /**
     * Guarda la lista de numeros en un archivo de texto con FileWriter y
     * PrintWriter. El bloque try-catch maneja la excepcion IOException
     * para evitar que el programa falle si el archivo no se puede abrir.
     */
    public static void guardarNumeros(ArrayList<Integer> numberList, String nombreArchivo) {
        try {
            FileWriter fw = new FileWriter(nombreArchivo);
            PrintWriter pw = new PrintWriter(fw);

            pw.println("Numeros ganadores del sorteo Melate:");
            for (int numero : numberList) {
                pw.println(numero);
            }

            pw.close(); // se cierra el archivo para que los datos queden guardados
            System.out.println("Los numeros se guardaron en el archivo " + nombreArchivo);
        } catch (IOException e) {
            // Si ocurre un error al abrir o escribir el archivo, se avisa al usuario
            System.out.println("Error al escribir el archivo: " + e.getMessage());
        }
    }
}
