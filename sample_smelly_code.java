public class SmellyClass {
    // 1. Primitive Obsession (Many primitive fields)
    private int id;
    private String name;
    private String email;
    private String address;
    private String city;
    private String zipCode;
    private int age;
    private boolean isActive;

    // 2. Data Class (Mostly getters/setters)
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    // 3. Long Method & Switch Statements
    public void complexLogic(int type) {
        // Bloater: Long Method (simulated with comments for brevity in this file, but logic counts statements)
        System.out.println("Start");
        int result = 0;
        
        switch (type) { // OO Abuser: Switch Statement
            case 1: result = 10; break;
            case 2: result = 20; break;
            case 3: result = 30; break;
            case 4: result = 40; break;
            case 5: result = 50; break;
            case 6: result = 60; break; // > 5 cases
        }
        
        // Bloater: Long Parameter List Check
        doSomethingComplex(1, "test", true, 5.0, "extra");
        
        // Dispensable: Duplicate Code
        System.out.println("Step 1 initialization");
        System.out.println("Checking database connection");
        System.out.println("Verifying user credentials");
        System.out.println("Logging access attempt");
        System.out.println("Validation complete");
        
        // ... some logic ...
        
        // Duplicate block
        System.out.println("Step 1 initialization");
        System.out.println("Checking database connection");
        System.out.println("Verifying user credentials");
        System.out.println("Logging access attempt");
        System.out.println("Validation complete");
    }

    // 4. Long Parameter List
    public void doSomethingComplex(int p1, String p2, boolean p3, double p4, String p5) {
        System.out.println("Too many parameters");
    }
}
