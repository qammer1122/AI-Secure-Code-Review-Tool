# 🤖 AI-Powered Secure Code Review Tool

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=flat-square&logo=flask&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![Bandit](https://img.shields.io/badge/Bandit-1.7.9-red?style=flat-square)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square)
![AI](https://img.shields.io/badge/AI-LSTM_Neural_Network-blueviolet?style=flat-square)

> An AI-powered web application that automatically detects security
> vulnerabilities in Python code using a trained LSTM neural network
> combined with Bandit static analysis. Supports direct code input,
> file upload, and full GitHub repository CI pipeline scanning.

---

## 📋 Project Overview

| Detail | Info |
|---|---|
| **Language** | Python 3.8+ |
| **Framework** | Flask |
| **AI Model** | LSTM Neural Network (TensorFlow/Keras) |
| **Static Analyzer** | Bandit v1.7.9 |
| **Analysis Modes** | ML Analysis, Bandit Analysis, CI Pipeline |
| **Severity Levels** | Critical, High, Medium, Low |

---

## ✨ Features

- ✅ **AI/ML Analysis** — LSTM model trained on security dataset classifies code severity
- ✅ **Bandit Static Analysis** — Industry-standard Python security linter
- ✅ **Dual Engine** — Run both ML and Bandit simultaneously for comprehensive coverage
- ✅ **GitHub CI Pipeline** — Clone and scan entire GitHub repositories automatically
- ✅ **File Upload** — Upload `.py` files directly for analysis
- ✅ **Code Paste** — Paste code directly into the web interface
- ✅ **History Tracking** — All analyses saved with timestamps
- ✅ **Severity Badges** — Color-coded Critical/High/Medium/Low results
- ✅ **Suggested Fixes** — Automated remediation recommendations per vulnerability

---

## 🏗️ Project Structure

---

## 🧠 How the AI Model Works

### Severity Thresholds

| Severity | Score Threshold | Class Weight |
|---|---|---|
| 🔴 Critical | ≥ 0.70 | 3x |
| 🟠 High | ≥ 0.60 | 2x |
| 🟡 Medium | ≥ 0.50 | 1.5x |
| 🟢 Low | ≥ 0.50 | 1x |
| Excluded | < 0.50 | — |

---

## 🔍 Analysis Modes

### 1. ML Analysis
Uses the trained LSTM neural network to classify each line of code by vulnerability severity. Checks against the security dataset for exact matches first, then uses model prediction.

### 2. Bandit Analysis
Runs Bandit static analysis on submitted code. Detects:
- Hardcoded passwords and secrets
- SQL injection vulnerabilities
- Use of dangerous functions (`eval`, `exec`, `subprocess`)
- Insecure cryptography
- XML vulnerabilities
- And 100+ more security checks

### 3. CI Pipeline (GitHub Integration)

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Internet connection (for GitHub CI Pipeline)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/qammer1122/AI-Secure-Code-Review-Tool.git
cd AI-Secure-Code-Review-Tool

# 2. Install dependencies
pip install -r requirements.txt

# Note: TensorFlow installation may take 5-10 minutes

# 3. Run the application
python app.py

# 4. Open browser
# http://localhost:5000
```

---

## 📦 Requirements

---

## 🖥️ Usage

### Analyze Code via Paste
1. Go to `http://localhost:5000`
2. Paste your Python code in the text area
3. Click **ML Analysis** or **Bandit Analysis**
4. View results with severity ratings and fixes

### Analyze via File Upload
1. Click **Upload a File**
2. Select a `.py` file
3. Choose analysis type and submit

### Scan a GitHub Repository
1. Click **CI Pipeline** in navbar
2. Enter a public GitHub repository URL
3. Click **Analyze Repository**
4. View comprehensive security report

---

## 📊 Example Output

### Vulnerable Code Input
```python
import subprocess
password = "admin123"
subprocess.call(user_input, shell=True)
eval(request.args.get('code'))
```

### Analysis Results

| # | Code | Severity | Suggested Fix |
|---|---|---|---|
| 1 | `password = "admin123"` | 🔴 Critical | Use environment variables for credentials |
| 2 | `subprocess.call(..., shell=True)` | 🟠 High | Avoid shell=True, use list arguments |
| 3 | `eval(request.args.get...)` | 🔴 Critical | Never use eval() with user input |
| 4 | `import subprocess` | 🟢 Low | Consider safer alternatives |

---

## 🗄️ Dataset

The model is trained on a custom security dataset (`security_dataset.csv`) containing:

| Column | Description |
|---|---|
| `code` | Python code snippet |
| `severity` | Critical / High / Medium / Low |
| `fixes` | Suggested remediation |

Training split: **80% train / 20% validation**

---

## 📚 Key Skills Demonstrated

- ✅ Machine learning model design and training (LSTM, TensorFlow/Keras)
- ✅ NLP tokenization and sequence padding for code analysis
- ✅ Flask web application development with multiple routes
- ✅ Static code analysis using Bandit security scanner
- ✅ GitHub repository integration using GitPython
- ✅ Adaptive severity classification with threshold tuning
- ✅ File handling and secure file upload implementation
- ✅ Full-stack web development (Python backend + HTML/CSS frontend)

---

## 🎓 Learning Outcomes

Through this project I gained:

- Hands-on experience applying ML to cybersecurity problems
- Understanding of how static analysis tools detect vulnerabilities
- Experience building end-to-end AI-powered security applications
- Knowledge of Python security vulnerabilities and remediation
- Skills in integrating multiple security analysis techniques
- Understanding of CI/CD security pipeline concepts

---

## 🔗 Related Projects

- [🔐 Threat Modeling Tool](https://github.com/qammer1122/Threat-Modeling-Tool) — STRIDE-based system threat analysis
- [🔴 Web Security Labs](https://github.com/qammer1122/Web-Security-Labs) — PortSwigger penetration testing
- [🔵 SIEM Deployment](https://github.com/qammer1122/SIEM-Deployment) — Wazuh security monitoring

---

## 📞 Contact

**Qammer Abbas**
📧 [qammer1122@gmail.com](https://mail.google.com/mail/?view=cm&fs=1&to=qammer1122@gmail.com)
🔗 [LinkedIn](https://linkedin.com/in/qammer1122)
🐙 [GitHub](https://github.com/qammer1122)
🛡️ [TryHackMe](https://tryhackme.com/p/qammer1122)
