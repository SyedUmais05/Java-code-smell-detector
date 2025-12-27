public class GodClass {
    // 1. Primitive Obsession (Many primitive fields, few objects)
    private int id;
    private int age;
    private int height;
    private int weight;
    private int zipCode;
    private int status;
    private String name;
    private String email;
    private String address;
    private String city;
    private String country;
    private String phone;
    private boolean isActive;
    private boolean isVerified;
    private boolean hasSubscription;

    // 2. Temporary Field (Only used in tempMethod)
    private int tempField; 

    public GodClass() {}

    // 3. Long Method (> 40 lines) with 4. Duplicate Code & 5. Switch Statements
    public void complexLogic(int type) {
        System.out.println("Start Processing...");
        int result = 0;
        
        // Filler logic to ensure length > 40
        for (int i = 0; i < 5; i++) {
            System.out.println("Initializing step " + i);
            result += i * 2;
        }

        // Switch Statement (> 5 cases)
        switch (type) { 
            case 1: result = 10; break;
            case 2: result = 20; break;
            case 3: result = 30; break;
            case 4: result = 40; break;
            case 5: result = 50; break;
            case 6: result = 60; break; 
            case 7: result = 70; break;
        }
        
        // Duplicate Code Block 1 (> 6 lines)
        System.out.println("Processing transaction header...");
        System.out.println("Validating user session...");
        System.out.println("Checking database connectivity...");
        System.out.println("Verifying security tokens...");
        System.out.println("Logging access timestamp...");
        System.out.println("Preparing response payload...");
        System.out.println("Transaction pre-check complete.");

        if (result > 100) {
            System.out.println("High value transaction");
        } else {
            System.out.println("Standard value transaction");
        }

        // Duplicate Code Block 2 (Identical to Block 1)
        System.out.println("Processing transaction header...");
        System.out.println("Validating user session...");
        System.out.println("Checking database connectivity...");
        System.out.println("Verifying security tokens...");
        System.out.println("Logging access timestamp...");
        System.out.println("Preparing response payload...");
        System.out.println("Transaction pre-check complete.");
        
        // 6. Message Chains ( > 3 dots)
        // System.out.println(this.getConfig().getSettings().getNetwork().getProxy());
        String chain = new StringBuilder().append("a").append("b").append("c").append("d").toString();
    }

    // 7. Data Clumps (Repeated parameters in methods)
    public void bookFlight(String start, String end, String date) { System.out.println("Flight"); }
    public void bookTrain(String start, String end, String date) { System.out.println("Train"); }
    public void bookBus(String start, String end, String date) { System.out.println("Bus"); }

    // 8. Long Parameter List (> 4 parameters)
    public void terribleMethod(int p1, String p2, boolean p3, double p4, float p5, Object p6) {
        System.out.println("Too many params");
    }

    // 9. Temporary Field Usage
    public void tempMethod() {
        tempField = 42; // Used only here
        System.out.println(tempField);
    }

    // 10. Refused Bequest
    public void legacyMethod() {
        throw new UnsupportedOperationException("Not supported in this version");
    }

    // 11. Dead Code (Private method never called)
    private void secretMethod() {
        System.out.println("I am never called");
    }

    // Extra methods to trigger 12. Large Class (> 15 methods)
    public void method01() {}
    public void method02() {}
    public void method03() {}
    public void method04() {}
    public void method05() {}
    public void method06() {}
    public void method07() {}
    public void method08() {}
}

// 13. Lazy Class (< 3 methods, < 2 fields)
class LazyComponent {
    public void doNothing() {}
}

// 14. Data Class (Mostly getters/setters)
class UserData {
    private String name;
    private int age;
    private String email;

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
