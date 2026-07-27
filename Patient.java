/**
 * Patient.java
 * A patient is a Person who is admitted with a certain illness.
 * Object Oriented Programming - Module 3, Activity 3.
 */
public class Patient extends Person {
    private String illness; // the illness the patient is treated for

    /** Creates a patient with a name, an age and an illness. */
    public Patient(String nameP, int ageP, String illnessP) {
        super(nameP, ageP); // reuse the Person constructor for the shared data
        this.illness = illnessP;
    }

    /** Returns the patient's illness. */
    public String getIllness() {
        return illness;
    }

    /** Greets the patient when registering. */
    @Override
    public void register() {
        System.out.println("Welcome Patient!");
    }
}
