from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import subprocess
import random

app = Flask(__name__,
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
app.secret_key = 'dictionary-search-secret-key-2024'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, 'users.json')
DICTIONARY_FILE = os.path.join(BASE_DIR, 'dictionary.txt')
C_EXE = os.path.join(BASE_DIR, 'binary_search.exe')

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def load_dictionary_words():
    if not os.path.exists(DICTIONARY_FILE):
        return []
    with open(DICTIONARY_FILE, 'r') as f:
        return sorted([line.strip().lower() for line in f if line.strip()])

def perform_binary_search(word):
    word = word.strip().lower()
    
    if os.path.exists(C_EXE):
        try:
            result = subprocess.run([C_EXE, word], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            print(f"Error calling C executable: {e}")
    
    words = load_dictionary_words()
    if not words:
        return "Dictionary file missing."
    
    left, right = 0, len(words) - 1
    while left <= right:
        mid = (left + right) // 2
        if words[mid] == word:
            return f"Word '{word}' found at position {mid} in the dictionary."
        elif words[mid] < word:
            left = mid + 1
        else:
            right = mid - 1
    
    return f"Word '{word}' not found in the dictionary."

def get_search_history(username):
    history_file = os.path.join(BASE_DIR, f'history_{username}.json')
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

def add_to_search_history(username, word, result):
    history_file = os.path.join(BASE_DIR, f'history_{username}.json')
    history = get_search_history(username)
    history.insert(0, {'word': word, 'result': result, 'timestamp': len(history) + 1})
    history = history[:20]
    with open(history_file, 'w') as f:
        json.dump(history, f)

def clear_search_history(username):
    history_file = os.path.join(BASE_DIR, f'history_{username}.json')
    if os.path.exists(history_file):
        os.remove(history_file)

@app.route('/')
@login_required
def index():
    word_count = len(load_dictionary_words())
    result = request.args.get('result')
    history = get_search_history(current_user.id)
    return render_template('index.html', word_count=word_count, result=result, history=history[:5])

@app.route('/search', methods=['POST'])
@login_required
def search():
    word = request.form.get('word', '')
    if word.strip():
        result = perform_binary_search(word)
        add_to_search_history(current_user.id, word, result)
        return redirect(url_for('index', result=result))
    return redirect(url_for('index'))

@app.route('/autocomplete', methods=['GET'])
@login_required
def autocomplete():
    query = request.args.get('q', '').lower()
    if len(query) < 2:
        return jsonify([])
    
    words = load_dictionary_words()
    suggestions = [w for w in words if w.startswith(query)][:10]
    return jsonify(suggestions)

@app.route('/random-word', methods=['POST'])
@login_required
def random_word():
    words = load_dictionary_words()
    if words:
        word = random.choice(words)
        result = perform_binary_search(word)
        add_to_search_history(current_user.id, word, result)
        return redirect(url_for('index', result=result))
    return redirect(url_for('index'))

@app.route('/clear-history', methods=['POST'])
@login_required
def clear_history():
    clear_search_history(current_user.id)
    flash('Search history cleared!')
    return redirect(url_for('index'))

@app.route('/history')
@login_required
def history():
    history = get_search_history(current_user.id)
    return render_template('history.html', history=history)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = load_users()
        if username in users and check_password_hash(users[username], password):
            user = User(username)
            login_user(user)
            flash(f'Welcome back, {username}!')
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters')
        elif len(password) < 6:
            flash('Password must be at least 6 characters')
        elif password != confirm_password:
            flash('Passwords do not match')
        else:
            users = load_users()
            if username in users:
                flash('Username already exists')
            else:
                users[username] = generate_password_hash(password)
                save_users(users)
                flash('Account created! Please login.')
                return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)