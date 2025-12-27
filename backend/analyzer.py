import javalang
from smells import detect_bloaters, detect_oo_abusers, detect_dispensables, detect_couplers

def analyze_code(source_code: str):
    """
    Analyzes Java source code for smells.
    Returns a structured dictionary report.
    """
    
    # 1. Parse API
    try:
        tree = javalang.parse.parse(source_code)
    except javalang.parser.JavaSyntaxError as e:
        return {
            "error": f"Syntax Error: {e.description} at line {e.at.line}",
            "summary": {"totalLines": len(source_code.splitlines()), "totalSmells": 0},
            "smells": []
        }
    except Exception as e:
         return {
            "error": f"Parsing Error: {str(e)}",
            "summary": {"totalLines": len(source_code.splitlines()), "totalSmells": 0},
            "smells": []
        }

    lines = source_code.splitlines()
    total_lines = len(lines)
    
    all_smells = []
    
    # Run Detectors
    all_smells.extend(detect_bloaters(tree, lines))
    all_smells.extend(detect_oo_abusers(tree, lines))
    all_smells.extend(detect_dispensables(tree, lines))
    all_smells.extend(detect_couplers(tree, lines))
    
    # Summary
    summary = {
        "totalLines": total_lines,
        "totalSmells": len(all_smells)
    }
    
    return {
        "summary": summary,
        "smells": all_smells
    }
