import os

def pytest_configure(config):
    project_root = os.path.dirname(os.path.abspath(__file__))
    allure_results_path = os.path.join(project_root, 'allure-results')
    config.option.allure_report_dir = allure_results_path

def pytest_sessionfinish(session, exitstatus):
    import subprocess
    project_root = os.path.dirname(os.path.abspath(__file__))

    results_dir = os.path.join(project_root, 'allure-results')
    report_dir = os.path.join(project_root, 'allure-report')

    subprocess.call(['allure', 'generate', results_dir, '--clean', '-o', report_dir])
