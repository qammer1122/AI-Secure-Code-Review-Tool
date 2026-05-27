import os
import shutil
from git import Repo
from utils import run_ml_analysis
from bandit_analysis import run_bandit_analysis

# Set up the GitHub folder for cloned repositories
GITHUB_FOLDER = 'github_projects'
os.makedirs(GITHUB_FOLDER, exist_ok=True)


def clone_repository(github_url):
    """Clones the GitHub repository to a local directory."""
    repo_name = github_url.split('/')[-1].replace('.git', '')
    clone_path = os.path.join(GITHUB_FOLDER, repo_name)

    # Remove existing directory if it already exists
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path)

    # Clone the repository
    Repo.clone_from(github_url, clone_path)
    return clone_path


def analyze_repository(clone_path, model, tokenizer, max_sequence_length, dataset):
    """Analyzes each Python file in the cloned repository."""
    analysis_results = []

    for root, _, files in os.walk(clone_path):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code_content = f.read()

                # Perform ML-based analysis line by line
                for line in code_content.split('\n'):
                    if line.strip():
                        ml_score, severity, suggested_fix = run_ml_analysis(
                            line, tokenizer, model, max_sequence_length, dataset
                        )
                        if severity is not None:
                            analysis_results.append({
                                "type": "ML",
                                "code": line,
                                "severity": severity,
                                "fixes": suggested_fix
                            })

                # Perform Bandit analysis on entire file
                bandit_results = run_bandit_analysis(code_content)
                for result in bandit_results:
                    analysis_results.append({
                        "type": "Bandit",
                        "code": result['code'],
                        "severity": result['severity'],
                        "fixes": result['fixes']
                    })

    return analysis_results


def analyze_github_repo(github_url, model, tokenizer, max_sequence_length, dataset):
    """Clones and analyzes a GitHub repository, returning the analysis results."""
    clone_path = clone_repository(github_url)
    results = analyze_repository(clone_path, model, tokenizer, max_sequence_length, dataset)
    return results
