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
| **Bloaters** | Long Method | > 40 lines (estimated) |
| | Large Class | > 15 methods |
| | Long Parameter List | > 4 parameters |
| | Primitive Obsession | > 50% fields are primitives |
| **OO Abusers** | Switch Statements | > 5 cases |
| **Dispensables** | Duplicate Code | Identical block > 6 lines |
| | Data Class | Class with only getters/setters/constructors |
| **Couplers** | Message Chains | `a().b().c().d()` pattern (Basic detection) |

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
