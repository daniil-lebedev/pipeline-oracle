# Pipeline Oracle

**Pipeline Oracle** is a cutting-edge CI/CD failure analysis tool that leverages the power of AI (via OpenAI's GPT-4 Turbo) to provide clear, actionable insights for fixing pipeline issues. Integrated directly with GitHub Actions, Pipeline Oracle automatically fetches logs from failed workflows, analyzes them, and generates detailed reports to help your team quickly diagnose and resolve issues. 🚀🔧

---

## Features

- **Automated Log Collection:** 📂  
  Automatically collects logs from failed GitHub Actions workflows.

- **AI-Powered Analysis:** 🤖  
  Uses OpenAI's GPT-4 Turbo to analyze CI/CD logs and provide specific remediation advice.

- **Seamless GitHub Integration:** 🔗  
  Runs automatically on workflow failures and uploads analysis reports as artifacts for easy access.

- **Future Enhancements:**
    - **Issue Automation:** Automatically file or update GitHub issues with the analysis report. 📝
    - **Real-Time Notifications:** Integrate with Slack or email to alert your team instantly. 📣
    - **Historical Trend Analysis:** Track recurring failures over time to drive continuous improvement. 📈

---

## How It Works

1. **Failure Detection:** ⚠️  
   When a CI/CD pipeline fails, the **On Failure Log Analysis** workflow is triggered.

2. **Log Collection:** 📥  
   The workflow uses the GitHub CLI to fetch logs from the most recent failed workflow run (excluding itself).

3. **AI Analysis:** 🧠  
   The logs are sent to OpenAI's GPT-4 Turbo for analysis, generating a detailed report with actionable fixes.

4. **Artifact Upload:** 📤  
   The report and logs are uploaded as artifacts, so you can download and review them directly from the GitHub Actions run summary.

---

## Setup and Installation

### Prerequisites

- A GitHub repository with workflows using GitHub Actions.
- An OpenAI API key (set as the repository secret `OPENAI_API_KEY`). 🔑
- A GitHub Personal Access Token (PAT) with required permissions (set as the repository secret `GH_PAT`). 🔒

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/pipeline-oracle.git
   cd pipeline-oracle

2. **Install Dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```
3. **Configure Secrets:**
    - Set your OpenAI API key as the repository secret `OPENAI_API_KEY`.
    - Set your GitHub PAT as the repository secret `GH_PAT`.

## Usage

Pipeline Oracle runs automatically when a workflow fails, thanks to the On Failure Log Analysis workflow configured in your repository. ⚙️

### Running Locally

You can also run the analysis locally. Make sure you have a log file at `logs/full_log.txt`, then run:


This will:

- Read the log file.
- Send the logs to OpenAI for analysis.
- Generate an analysis_report.md with AI-generated insights.

Contributions are welcome! Please fork this repository, create a new branch, and open a pull request with your changes. 🙌

## License
This project is licensed under the MIT License. See the [LICENSE](License.md) file for details.

## Acknowledgements
- [OpenAI](https://openai.com) for providing the powerful GPT-4 Turbo model.
- [GitHub](https://github.com) for enabling seamless CI/CD workflows with GitHub Actions.