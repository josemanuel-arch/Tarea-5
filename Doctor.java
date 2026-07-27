/**
 * Doctor.java
 * A doctor is a Person who also belongs to a medical department.
 * Object Oriented Programming - Module 3, Activity 3.
 */
public class Doctor extends Person {
    private String department; // the department the doctor works in

    /** Creates a doctor with a name, an age and a department. */
    public Doctor(String nameD, int ageD, String departmentD) {
        super(nameD, ageD); // reuse the Person constructor for the shared data
        this.department = departmentD;
    }

    /** Returns the doctor's department. */
    public String getDepartment() {
        return department;
    }

    /** Greets the doctor when registering. */
    @Override
    public void register() {
        System.out.println("Welcome Doctor!");
    }
}
