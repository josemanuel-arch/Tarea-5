/**
 * HospitalTest.java
 * Test program for the hospital class hierarchy. It creates the four people
 * requested in the activity and registers each one. The Guard cases show the
 * two overloaded constructors: John is created without a phone and Kevin with
 * a phone.
 * Object Oriented Programming - Module 3, Activity 3.
 */
public class HospitalTest {
    public static void main(String[] args) {
        // Test data requested in the activity
        Doctor doctor = new Doctor("Joseph", 41, "Neurologist");
        Patient patient = new Patient("Richard", 78, "Chronic Headache");
        Guard guardNoPhone = new Guard("John", 39, "Morning");                        // 3-argument constructor
        Guard guardWithPhone = new Guard("Kevin", 43, "Afternoon", "+52 232 456345"); // 4-argument constructor

        System.out.println("=== Hospital registration system ===");

        // Doctor
        System.out.println();
        System.out.println("Doctor");
        System.out.println("  Name: " + doctor.getName());
        System.out.println("  Age: " + doctor.getAge());
        System.out.println("  Department: " + doctor.getDepartment());
        doctor.register();

        // Patient
        System.out.println();
        System.out.println("Patient");
        System.out.println("  Name: " + patient.getName());
        System.out.println("  Age: " + patient.getAge());
        System.out.println("  Illness: " + patient.getIllness());
        patient.register();

        // Guard created without a phone (shorter overloaded constructor)
        System.out.println();
        System.out.println("Guard");
        System.out.println("  Name: " + guardNoPhone.getName());
        System.out.println("  Age: " + guardNoPhone.getAge());
        System.out.println("  Shift: " + guardNoPhone.getShift());
        System.out.println("  Phone: " + (guardNoPhone.getPhone() == null ? "not provided" : guardNoPhone.getPhone()));
        guardNoPhone.register();

        // Guard created with a phone (longer overloaded constructor)
        System.out.println();
        System.out.println("Guard");
        System.out.println("  Name: " + guardWithPhone.getName());
        System.out.println("  Age: " + guardWithPhone.getAge());
        System.out.println("  Shift: " + guardWithPhone.getShift());
        System.out.println("  Phone: " + (guardWithPhone.getPhone() == null ? "not provided" : guardWithPhone.getPhone()));
        guardWithPhone.register();
    }
}
