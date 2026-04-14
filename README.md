# Dictionary Search System (Python + C Hybrid)

This project combines **Python (Flask)** for a simple web interface and **C** for the core Binary Search algorithm (Design and Analysis of Algorithms - DAA).

## Project Structure

```
daa/
├── frontend/                  # Frontend (UI Layer)
│   ├── templates/            # HTML files
│   │   ├── index.html
│   │   ├── login.html
│   │   └── signup.html
│   └── static/               # Static files
│       └── css/
│           └── style.css
├── backend/                  # Backend (Business Logic Layer)
│   ├── app.py               # Flask web application
│   └── binary_search.c      # C source for DAA algorithm
├── dictionary.txt           # Word data
├── users.json               # User credentials (created at runtime)
└── README.md
```

## How it works
- **Frontend**: HTML templates and CSS for the user interface.
- **Backend**: Python Flask handles web requests, user auth, and calls the C binary search algorithm.
- **Hybrid Logic**: The Python app automatically uses the compiled C executable (`binary_search.exe`) if available, otherwise falls back to Python.

## Getting Started

### 1. Install Python Dependencies
```bash
cd backend
pip install flask flask-login werkzeug
```

### 2. Compile the C Algorithm (Optional but Recommended for DAA)
```bash
gcc binary_search.c -o binary_search.exe
```

### 3. Run the App
```bash
python app.py
```
Visit `http://127.0.0.1:5000` in your browser.

## Why this approach?
1. **Simplicity**: Python/Flask is much easier for building web pages and handling user accounts.
2. **DAA Focus**: Using C for the binary search allows you to study and analyze the algorithm's performance.
3. **Clean Architecture**: Frontend and Backend separation follows good software engineering practices.
