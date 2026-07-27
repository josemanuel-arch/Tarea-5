/**
 * Person.java
 * Abstract superclass for every person in the hospital system.
 * It keeps the data and behavior shared by doctors, patients and guards,
 * so that common code lives in a single place (abstraction + inheritance).
 * Object Oriented Programming - Module 3, Activity 3.
 */
public abstract class Person {
    // Data fields shared by every person
    private String name; // the person's name
    private int age;     // the person's age in years

    /** Constructor that sets the name and age common to every person. */
    public Person(String nameP, int ageP) {
        this.name = nameP;
        this.age = ageP;
    }

    /** Returns the person's name. */
    public String getName() {
        return name;
    }

    /** Returns the person's age. */
    public int getAge() {
        return age;
    }

    /**
     * Registers the person in the system. Each subclass greets its own kind
     * of person in its own way, so the method is abstract and every subclass
     * must provide its own version.
     */
    public abstract void register();
}
