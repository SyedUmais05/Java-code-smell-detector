# Code Smell Detection Tool

## Overview
A web-based static analysis tool designed for academic software re-engineering courses. It analyzes Java source code to detect classic code smells without executing the code.

## Architecture
- **Frontend**: React (Vite)
- **Backend**: Python (FastAPI + javalang)
- **Communication**: REST API (JSON)

## Supported Code Smells
| Category | Smell | Heuristic |
|----------|-------|-----------|
| Category | Smell | Heuristic |
|----------|-------|-----------|
| **Bloaters** | Long Method | > 40 lines (estimated) |
| | Large Class | > 15 methods |
| | Long Parameter List | > 4 parameters |
| | Primitive Obsession | > 50% fields are primitives |
| | Data Clumps | Groups of ≥3 parameters repeated in ≥2 methods |
| **OO Abusers** | Switch Statements | > 5 cases |
| | Temporary Field | Field used in only 1 method (excluding accessors) |
| | Refused Bequest | Method throws `UnsupportedOperationException` |
| **Dispensables** | Duplicate Code | Identical block > 6 lines |
| | Dead Code | Private method never called within class |
| | Lazy Class | < 3 methods and < 2 fields |
| | Data Class | Class with >90% getters/setters |
| **Couplers** | Message Chains | `a().b().c().d()` pattern (> 3 calls) |
| | Feature Envy | Method uses frequent foreign data (Simplified) |
| | Middle Man | Method purely delegates to another object |

## Setup & Running

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
API will run at `http://localhost:8000`.

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
App will open at `http://localhost:5173`.

## Usage
1. Open the web app.
2. Paste Java code into the textarea (e.g., from `sample_smelly_code.java`).
3. Click "Analyze Code".
4. Review the generated report.

## Academic Context
This tool aligns with re-engineering concepts by providing:
- **Detection**: Automated identification of design flaws.
- **Diagnosis**: Explanations (Reason) and Locations.
- **Prescription**: Suggested refactoring techniques.
