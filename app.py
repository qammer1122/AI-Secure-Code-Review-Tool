import os
from datetime import datetime
from flask import Flask, request, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from model import train_ml_model
from utils import run_ml_analysis
from bandit_analysis import run_bandit_analysis
from github_analysis import analyze_github_repo  # FIX A: no longer trains model at import

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')  # BUG FIX #7: prefer env variable
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['GITHUB_FOLDER'] = 'github_projects'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GITHUB_FOLDER'], exist_ok=True)

# Train the ML model and load the dataset
model, tokenizer, max_sequence_length, dataset = train_ml_model()

# Global variable to store analysis history
analysis_history = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_ml', methods=['POST'])
def upload_ml_file():
    # Handle ML analysis on code provided as text or file
    code_content = request.form.get('code_input', '').strip()
    file = request.files.get('file')

    if not code_content and not file:
        flash("No code provided for analysis")
        return redirect(url_for('index'))

    # If a file is uploaded, read its content
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:  # FIX C: encoding
            code_content = f.read()

    # Run ML analysis on the code
    code_lines = code_content.split('\n')
    analysis_results = []
    for code in code_lines:
        if code.strip():
            ml_score, severity, suggested_fix = run_ml_analysis(code, tokenizer, model, max_sequence_length, dataset)
            if severity is not None:  # BUG FIX #1: skip lines where result is (None, None, None)
                analysis_results.append({"code": code, "severity": severity, "fixes": suggested_fix})

    # Store analysis with timestamp
    analysis_history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "ML Analysis",
        "results": analysis_results
    })

    return render_template('report.html', analysis_results=analysis_results, analysis_type="ML")


@app.route('/upload_bandit', methods=['POST'])
def upload_bandit_file():
    # Handle Bandit analysis on code provided as text or file
    code_content = request.form.get('code_input', '').strip()
    file = request.files.get('file')

    if not code_content and not file:
        flash("No code provided for analysis")
        return redirect(url_for('index'))

    # If a file is uploaded, read its content
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:  # FIX C: encoding
            code_content = f.read()

    # Run Bandit analysis on the code
    bandit_results = run_bandit_analysis(code_content)

    # Store analysis with timestamp
    analysis_history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "Bandit Analysis",
        "results": bandit_results
    })

    return render_template('report.html', analysis_results=bandit_results, analysis_type="Bandit")


@app.route('/ci_pipeline', methods=['GET', 'POST'])
def ci_pipeline():
    if request.method == 'POST':
        github_url = request.form.get('github_url').strip()
        if not github_url:
            flash("Please enter a GitHub repository URL.")
            return redirect(url_for('ci_pipeline'))

        # Run analysis on the GitHub repository
        analysis_results = analyze_github_repo(github_url, model, tokenizer, max_sequence_length, dataset)  # FIX A: pass trained model

        # Store analysis with timestamp
        analysis_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "CI Pipeline Analysis",
            "results": analysis_results,
            "repository": github_url
        })

        return render_template('report.html', analysis_results=analysis_results, analysis_type="CI Pipeline")
    return render_template('ci_pipeline.html')


@app.route('/history')
def history():
    return render_template('history.html', analysis_history=analysis_history)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
