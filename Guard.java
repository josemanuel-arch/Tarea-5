/**
 * Guard.java
 * A guard is a Person who covers a shift and may have a contact phone.
 * This class shows constructor overloading: a guard can be created with or
 * without a phone number, and the shorter constructor reuses the longer one.
 * Object Oriented Programming - Module 3, Activity 3.
 */
public class Guard extends Person {
    private String shift; // the shift the guard covers (for example, Morning)
    private String phone; // the guard's contact phone (optional)

    /**
     * Creates a guard without a phone number. It calls the other constructor
     * with null as the phone, so the setup code is written only once.
     */
    public Guard(String nameG, int ageG, String shiftG) {
        this(nameG, ageG, shiftG, null); // constructor chaining (overloading)
    }

    /** Creates a guard with a phone number. */
    public Guard(String nameG, int ageG, String shiftG, String phoneG) {
        super(nameG, ageG); // reuse the Person constructor for the shared data
        this.shift = shiftG;
        this.phone = phoneG;
    }

    /** Returns the guard's shift. */
    public String getShift() {
        return shift;
    }

    /** Returns the guard's phone, or null if none was provided. */
    public String getPhone() {
        return phone;
    }

    /** Greets the guard when registering. */
    @Override
    public void register() {
        System.out.println("Welcome Guard!");
    }
}
