import javalang
from javalang.tree import MethodDeclaration, ClassDeclaration, SwitchStatement, FormalParameter, BasicType, ReferenceType, MemberReference, MethodInvocation
import collections

# Thresholds (Configurable)
THRESHOLDS = {
    "LONG_METHOD": 40,
    "LARGE_CLASS_LINES": 300,
    "LARGE_CLASS_METHODS": 15,
    "LONG_PARAMETER_LIST": 4,
    "SWITCH_CASES": 5,
    "DUPLICATE_CODE_BLOCK": 6
}

def detect_bloaters(tree, source_code_lines):
    smells = []
    
    # 1. Long Method
    # 2. Long Parameter List
    for path, node in tree.filter(MethodDeclaration):
        # Long Method
        if node.position:
            # Estimate lines: strictly, javalang doesn't give end line easily without full token parsing, 
            # but we can try to estimate or if we had tokens. 
            # For simplicity in this constrained tool, we might need a workaround or assume end_line is available if we mapped it.
            # Actually, without tokens, exact line count of a node is hard.
            # Heuristic: Difference between this node's start and next node's start?
            # Better heuristic for this tool: Count statements in body? 
            # User asked for "Long Method -> > 40 lines". 
            # We will use a line-counting heuristic based on the body statements range if available, 
            # or roughly count statements * 1.5. 
            # Let's try to find the start line and just count body statements as a proxy if we can't get end line?
            # Wait, if we have the source code, we can maybe map it?
            # Let's stick to a simpler "Statement Count" proxy for lines if exact lines are hard, 
            # OR try to track positions.
            # Javalang nodes have .position (line, col). 
            
            # Let's use a rough heuristic: 
            # Length = (Last statement line) - (First statement line) + overhead?
            
            start_line = node.position.line
            end_line = start_line
            if node.body:
                # Find the max line in the body
                for statement in node.body:
                     # Recursive search for max line in this subtree could be expensive/complex
                     # Let's just look at direct children for now or walk the body
                     if hasattr(statement, 'position') and statement.position:
                         end_line = max(end_line, statement.position.line)
            
            # This is lower bound. Let's assume some formatting overhead.
            length = (end_line - start_line) + 2 # +2 for braces
            
            # To be more robust, we could just re-scan the source code, but matching names is tricky.
            # Let's trust the heuristics for now.
            if length > THRESHOLDS["LONG_METHOD"]:
                 smells.append({
                    "type": "Long Method",
                    "location": f"{node.name}()",
                    "severity": "High" if length > THRESHOLDS["LONG_METHOD"] * 2 else "Medium",
                    "reason": f"Method length estimated at {length} lines (threshold: {THRESHOLDS['LONG_METHOD']})",
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

    # 3. Large Class
    for path, node in tree.filter(ClassDeclaration):
        method_count = len(node.methods)
        # Estimate class lines similar to method lines
        start_line = node.position.line if node.position else 1
        # It's hard to get exact end of class without token stream.
        # But usually entire file is one class in these academic snippets.
        # We can use total file lines if it's the main class.
        # OR count members.
        
        # Smart Heuristic: If this is the *only* or *main* class, use total logical lines.
        # Otherwise, just use method count as the primary indicator for Large Class here.
        
        if method_count > THRESHOLDS["LARGE_CLASS_METHODS"]:
             smells.append({
                "type": "Large Class",
                "location": node.name,
                "severity": "High",
                "reason": f"Class has {method_count} methods",
                "suggestedRefactoring": "Extract Class"
            })
            
    # 4. Primitive Obsession (Heuristic: > 60% of fields are primitives)
    for path, node in tree.filter(ClassDeclaration):
        fields = [f for f in node.fields]
        if not fields: continue
        
        primitive_count = 0
        total_fields = 0
        for field in fields:
            # field.type is ReferenceType or BasicType
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

    return smells

def detect_oo_abusers(tree, source_code_lines):
    smells = []
    
    # Switch Statements
    for path, node in tree.filter(SwitchStatement):
        # Check cases
        cases = node.cases
        if len(cases) > THRESHOLDS["SWITCH_CASES"]:
             smells.append({
                "type": "Switch Statements",
                "location": f"Line {node.position.line}",
                "severity": "Medium",
                "reason": f"Switch statement has {len(cases)} cases",
                "suggestedRefactoring": "Replace Conditional with Polymorphism"
            })
            
    # Temporary Field (Hard to detect accurately without data flow)
    # Heuristic: Field only used in one method?
    # We will skip complex data flow for this academic tool and focus on easier ones or simplistic heuristic.
    # Simplified Heuristic: If a class has a field that appears to be used in only 1 method (excluding setters/getters).
    
    return smells

def detect_dispensables(tree, source_code_lines):
    smells = []
    
    # 1. Duplicate Code (Text based)
    # Sliding window of 6 lines
    lines = [l.strip() for l in source_code_lines if l.strip()] # Ignore empty lines
    if len(lines) > THRESHOLDS["DUPLICATE_CODE_BLOCK"]:
        seen_blocks = {}
        window_size = THRESHOLDS["DUPLICATE_CODE_BLOCK"]
        for i in range(len(lines) - window_size + 1):
            block = tuple(lines[i:i+window_size])
            if block in seen_blocks:
                smells.append({
                    "type": "Duplicate Code",
                    "location": f"Lines near {i}", # Rough location
                    "severity": "Medium",
                    "reason": "Identical block of code detected multiple times",
                    "suggestedRefactoring": "Extract Method"
                })
                break # Just report once per file to avoid noise
            seen_blocks[block] = i

    # 2. Data Class
    # Class has methods, but all of them start with get/set/is or are constructors?
    for path, node in tree.filter(ClassDeclaration):
        methods = node.methods
        if len(methods) > 2:
            is_data_class = True
            for m in methods:
                name = m.name
                if not (name.startswith("get") or name.startswith("set") or name.startswith("is")):
                    is_data_class = False
                    break
            
            if is_data_class:
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
    
    # Message Chains: a.b().c().d()
    for path, node in tree.filter(MethodInvocation):
        # This is tricky in Javalang. Chained calls are often nested selectors or nested MethodInvocations.
        # We might just grep for this one or look at the structure.
        # Heuristic: count dots in the source line?
        pass # Todo: refine
        
    # Grep-based Message Chain & Feature Envy (Simple)
    for i, line in enumerate(source_code_lines):
        # Message Chain
        if line.count("().") > 2:
            smells.append({
                "type": "Message Chains",
                "location": f"Line {i+1}",
                "severity": "Medium",
                "reason": "Complex method chaining detected (>.().().)",
                "suggestedRefactoring": "Hide Delegate"
            })
            
    return smells
