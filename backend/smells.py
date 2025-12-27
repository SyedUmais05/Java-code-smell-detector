import javalang
from javalang.tree import MethodDeclaration, ClassDeclaration, SwitchStatement, FormalParameter, BasicType, ReferenceType, MemberReference, MethodInvocation, ThrowStatement, ClassCreator
import collections

# Thresholds (Configurable)
THRESHOLDS = {
    "LONG_METHOD": 40,
    "LARGE_CLASS_LINES": 300,
    "LARGE_CLASS_METHODS": 15,
    "LONG_PARAMETER_LIST": 4,
    "SWITCH_CASES": 5,
    "DUPLICATE_CODE_BLOCK": 6,
    "DATA_CLUMP_FIELDS": 3,
    "MESSAGE_CHAIN_LENGTH": 3,
    "LAZY_CLASS_METHODS": 3
}

def detect_bloaters(tree, source_code_lines):
    smells = []
    
    # 1. Long Method & 2. Long Parameter List (Existing)
    for path, node in tree.filter(MethodDeclaration):
        # Long Method Heuristic
        if node.position:
            start_line = node.position.line
            end_line = start_line
            if node.body:
                for statement in node.body:
                     if hasattr(statement, 'position') and statement.position:
                         end_line = max(end_line, statement.position.line)
            length = (end_line - start_line) + 2 
            
            if length > THRESHOLDS["LONG_METHOD"]:
                 smells.append({
                    "type": "Long Method",
                    "location": f"{node.name}()",
                    "severity": "High" if length > THRESHOLDS["LONG_METHOD"] * 2 else "Medium",
                    "reason": f"Method length estimated at {length} lines",
                    "suggestedRefactoring": "Extract Method"
                })

        # Long Parameter List
        if len(node.parameters) > THRESHOLDS["LONG_PARAMETER_LIST"]:
            smells.append({
                "type": "Long Parameter List",
                "location": f"{node.name}()",
                "severity": "Medium",
                "reason": f"Method has {len(node.parameters)} parameters",
                "suggestedRefactoring": "Introduce Parameter Object"
            })

    # 3. Large Class (Existing)
    for path, node in tree.filter(ClassDeclaration):
        method_count = len(node.methods)
        if method_count > THRESHOLDS["LARGE_CLASS_METHODS"]:
             smells.append({
                "type": "Large Class",
                "location": node.name,
                "severity": "High",
                "reason": f"Class has {method_count} methods",
                "suggestedRefactoring": "Extract Class"
            })
            
    # 4. Primitive Obsession (Existing)
    for path, node in tree.filter(ClassDeclaration):
        fields = [f for f in node.fields]
        if not fields: continue
        
        primitive_count = 0
        total_fields = 0
        for field in fields:
            if isinstance(field.type, BasicType):
                primitive_count += 1
            elif isinstance(field.type, ReferenceType) and field.type.name in ["String", "Integer", "Double", "Boolean"]:
                 primitive_count += 1
            total_fields += 1
            
        if total_fields > 3 and (primitive_count / total_fields) > 0.5:
             smells.append({
                "type": "Primitive Obsession",
                "location": node.name,
                "severity": "Low",
                "reason": f"{primitive_count}/{total_fields} fields are primitives",
                "suggestedRefactoring": "Replace Data Value with Object"
            })

    # 5. Data Clumps (New: Repeated groups of >= 3 parameters)
    # Heuristic: Find method signatures with overlapping parameter sequences of types/names
    param_groups = collections.Counter()
    for path, node in tree.filter(MethodDeclaration):
        if not node.parameters: continue
        # Extract types
        params = []
        for p in node.parameters:
            t = p.type.name if hasattr(p.type, 'name') else 'Unknown'
            params.append(t)
        
        # Look for subsets of size 3
        if len(params) >= THRESHOLDS["DATA_CLUMP_FIELDS"]:
            # Simple check: store the sorted tuple of types
            # (Better would be types+names or just types if distinct enough)
            group = tuple(sorted(params))
            param_groups[group] += 1
            
    for group, count in param_groups.items():
        if count >= 2: # Appears in at least 2 methods (heuristic for single file)
             smells.append({
                "type": "Data Clumps",
                "location": f"Global (Method Parameters)",
                "severity": "Medium",
                "reason": f"Parameter group {group} appears in {count} methods",
                "suggestedRefactoring": "Extract Class"
            })

    return smells

def detect_oo_abusers(tree, source_code_lines):
    smells = []
    
    # 1. Switch Statements (Existing)
    for path, node in tree.filter(SwitchStatement):
        cases = node.cases
        if len(cases) > THRESHOLDS["SWITCH_CASES"]:
             smells.append({
                "type": "Switch Statements",
                "location": f"Line {node.position.line}",
                "severity": "Medium",
                "reason": f"Switch statement has {len(cases)} cases",
                "suggestedRefactoring": "Replace Conditional with Polymorphism"
            })
            
    # 2. Temporary Field (New)
    # Heuristic: Field used in only one method (and not getter/setter)
    class_fields = set()
    for path, node in tree.filter(ClassDeclaration):
        for field in node.fields:
             for declarator in field.declarators:
                 class_fields.add(declarator.name)
    
    field_usage = {f: set() for f in class_fields}
    for path, node in tree.filter(MethodDeclaration):
        # Walk method body to find refs
        for _, ref in node.filter(MemberReference):
            if ref.member in class_fields:
                field_usage[ref.member].add(node.name)
                
    for field, methods in field_usage.items():
        # exclude setters/getters roughly
        real_usage = [m for m in methods if not (m.startswith("set") or m.startswith("get"))]
        if len(real_usage) == 1:
             smells.append({
                "type": "Temporary Field",
                "location": f"Field '{field}'",
                "severity": "Low",
                "reason": f"Field used mainly in single method '{list(real_usage)[0]}'",
                "suggestedRefactoring": "Extract Class"
            })

    # 3. Refused Bequest (New)
    # Heuristic: Method overrides but throws UnsupportedOperationException
    for path, node in tree.filter(MethodDeclaration):
        # We can't easily check @Override without resolving annotations fully or inheritance, 
        # but we can look for specific exception
        if node.throws and 'UnsupportedOperationException' in node.throws:
             smells.append({
                "type": "Refused Bequest",
                "location": f"{node.name}()",
                "severity": "Medium",
                "reason": "Method throws UnsupportedOperationException",
                "suggestedRefactoring": "Push Down Method / Extract Superclass"
            })
        # Check body for strict throw
        if node.body and len(node.body) == 1:
            stmt = node.body[0]
            if isinstance(stmt, ThrowStatement):
                # Check what is thrown.. hard to deep dive in simplified AST usage
                pass # Javalang structure for Throw is generic

    return smells

def detect_dispensables(tree, source_code_lines):
    smells = []
    
    # 1. Duplicate Code (Existing)
    lines = [l.strip() for l in source_code_lines if l.strip()]
    if len(lines) > THRESHOLDS["DUPLICATE_CODE_BLOCK"]:
        seen_blocks = {}
        window_size = THRESHOLDS["DUPLICATE_CODE_BLOCK"]
        for i in range(len(lines) - window_size + 1):
            block = tuple(lines[i:i+window_size])
            if block in seen_blocks:
                smells.append({
                    "type": "Duplicate Code",
                    "location": f"Lines near {i}",
                    "severity": "Medium",
                    "reason": "Identical block of code detected multiple times",
                    "suggestedRefactoring": "Extract Method"
                })
                break 
            seen_blocks[block] = i

    # 2. Dead Code (New: Private methods never called)
    private_methods = set()
    all_calls = set()
    
    for path, node in tree.filter(MethodDeclaration):
        if 'private' in node.modifiers:
            private_methods.add(node.name)
        
        # Collect calls in this method body
        for _, invocation in node.filter(MethodInvocation):
            all_calls.add(invocation.member)
            
    dead_methods = private_methods - all_calls
    for dm in dead_methods:
         smells.append({
            "type": "Dead Code",
            "location": f"{dm}()",
            "severity": "Medium",
            "reason": "Private method is never called within the file",
            "suggestedRefactoring": "Inline Method / Delete Code"
        })

    # 3. Lazy Class (New)
    for path, node in tree.filter(ClassDeclaration):
        # Heuristic: Few methods (excluding getters/setters) and fields
        methods = node.methods
        real_methods = [m for m in methods if not (m.name.startswith("get") or m.name.startswith("set"))]
        
        if len(real_methods) < THRESHOLDS["LAZY_CLASS_METHODS"] and len(node.fields) < 2:
             smells.append({
                "type": "Lazy Class",
                "location": node.name,
                "severity": "Low",
                "reason": "Class has very little functionality/data",
                "suggestedRefactoring": "Collapse Hierarchy / Inline Class"
            })
            
    # 4. Data Class (Existing) - Logic: Mostly getters/setters
    for path, node in tree.filter(ClassDeclaration):
        methods = node.methods
        if len(methods) > 2:
            is_data_class = True
            non_accessors = 0
            for m in methods:
                name = m.name
                if not (name.startswith("get") or name.startswith("set") or name.startswith("is")):
                    is_data_class = False
                    non_accessors += 1
            
            # Refined: If >90% are accessors
            ratio = (len(methods) - non_accessors) / len(methods)
            if ratio > 0.9: 
                 smells.append({
                    "type": "Data Class",
                    "location": node.name,
                    "severity": "Low",
                    "reason": "Class appears to only contain getters and setters",
                    "suggestedRefactoring": "Move Method"
                })

    return smells

def detect_couplers(tree, source_code_lines):
    smells = []
    
    # 1. Feature Envy (New: Simple Heuristic)
    # Check if a method uses more fields/methods from another class than its own (rough check)
    for path, node in tree.filter(MethodDeclaration):
        # Count 'this.' or implicit field access vs 'otherObject.'
        pass # Without symbol table/types, this is very hard to guess accurately.
        # Simple Proxy: Count variables that have many methods called on them?
        
    # 2. Message Chains (New)
    for i, line in enumerate(source_code_lines):
        if line.count("().") >= THRESHOLDS["MESSAGE_CHAIN_LENGTH"]:
            smells.append({
                "type": "Message Chains",
                "location": f"Line {i+1}",
                "severity": "Medium",
                "reason": "Complex method chaining detected (>.().().)",
                "suggestedRefactoring": "Hide Delegate"
            })
            
    # 3. Middle Man (New)
    # Method bodies strictly delegates: return x.foo()
    for path, node in tree.filter(MethodDeclaration):
        if node.body and len(node.body) == 1:
            stmt = node.body[0]
            # Check if it's a return statement with a method invocation
            # Or just an expression statement
            # This is intricate AST matching. 
            pass

    return smells
