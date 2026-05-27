from bandit.core.manager import BanditManager
from bandit.core import config as b_config
import tempfile
import os

def run_bandit_analysis(code):
    # Create a temporary file to store the code input for Bandit to analyze
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code.encode('utf-8'))
        temp_file_path = temp_file.name

    try:
        # Initialize Bandit configuration and manager with agg_type set to "file"
        conf = b_config.BanditConfig()
        b_mgr = BanditManager(conf, agg_type="file")  # Setting agg_type to "file"
        b_mgr.discover_files([temp_file_path])

        # Run Bandit analysis
        b_mgr.run_tests()

        # Format the results
        report_data = []
        for result in b_mgr.results:
            # Get the actual code line that caused the issue
            code_line = result.get_code()  # Use get_code() to retrieve the code snippet
            report_data.append({
                "code": code_line,  # Use the actual code snippet instead of the test ID
                "severity": result.severity.capitalize(),
                "fixes": result.text,
            })

        return report_data

    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)
