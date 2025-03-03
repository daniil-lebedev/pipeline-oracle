# Pipeline Oracle 🚀

**Pipeline Oracle** is a cutting-edge CI/CD failure analysis tool that leverages the power of AI (via OpenAI's GPT-4 Turbo) to provide clear, actionable insights for fixing pipeline issues. Integrated with GitHub Actions, Pipeline Oracle automatically fetches logs from failed workflows, analyzes them, and generates detailed reports to help your team quickly diagnose and resolve issues. 🔧🤖

---

## Features ✨

- **Automated Log Collection:** 📂  
  Automatically collects logs from failed GitHub Actions workflows.

- **AI-Powered Analysis:** 🤖  
  Uses OpenAI's GPT-4 Turbo to analyze logs and provide actionable fixes.

- **Seamless GitHub Integration:** 🔗  
  Triggers automatically on workflow failures, uploads analysis reports as artifacts, and creates GitHub issues with the report.

- **Plug-and-Play Integration:** 🔌  
  Easily add Pipeline Oracle to your repository using our composite GitHub Action—no need to copy complex code.

---

## How It Works ⚙️

1. **Failure Detection:** ⚠️  
   When a CI/CD pipeline fails, a designated workflow is triggered.

2. **Log Collection:** 📥  
   The workflow uses the GitHub CLI to fetch logs from the most recent failed run (excluding itself).

3. **AI Analysis:** 🧠  
   The logs are sent to OpenAI's GPT-4 Turbo for detailed analysis and remediation advice.

4. **Artifact Upload:** 📤  
   The analysis report and logs are uploaded as artifacts for easy review directly from the GitHub Actions run summary.

5. **GitHub Issue Creation:** 📝  
   A GitHub issue is automatically created with the AI-generated analysis report, assigning it to the merging user for prompt follow-up.

---

## Setup and Installation 🔧

### Prerequisites

- A GitHub repository with workflows using GitHub Actions.
- An **OpenAI API key** (set as the repository secret `OPENAI_API_KEY`). 🔑
- A **GitHub Personal Access Token (PAT)** with the required permissions (set as the repository secret `GH_PAT`). 🔒
- A **GitHub API key** (set as the repository secret `GITHUB_API_KEY`).  
  *Note: The GitHub API key is now required for advanced operations.*

---

## Quick Start: Add Pipeline Oracle via a Composite GitHub Action ⚡

Pipeline Oracle is now available as a reusable composite GitHub Action that makes integration plug-and-play. Follow these steps:

1. **Publish/Install the Action:**  
   Pipeline Oracle is published on the GitHub Marketplace as [daniil-lebedev/pipeline-oracle](https://github.com/daniil-lebedev/pipeline-oracle).  
   *(Replace with the actual link once published.)*

2. **Configure Your Workflow:**  
   Create a workflow file (e.g., `.github/workflows/on-failure.yaml`) in your repository with the following content:

   ```yaml
   name: Pipeline Oracle

   on:
     workflow_run:
       workflows: [ "Deploying to Prod", "Integration Tests", "Build Pipeline" ]
       types:
         - completed

   jobs:
     failure-analysis:
       runs-on: ubuntu-latest
       if: ${{ github.event.workflow_run.conclusion == 'failure' }}
       steps:
         - name: Run Pipeline Oracle Analysis
           uses: daniil-lebedev/pipeline-oracle@v1.0.4
           with:
             workflow-to-track: "Deploying to Prod"
             gh-pat: ${{ secrets.GH_PAT }}
             github-api-key: ${{ secrets.GITHUB_API_KEY }}
   ```

3. **Configure Secrets:**  
   In your repository settings, add the following secrets:
   - **OPENAI_API_KEY:** Your OpenAI API key.
   - **GH_PAT:** Your GitHub PAT.
   - **GITHUB_API_KEY:** Your GitHub API key.

---

## Running Pipeline Oracle Locally 💻

If you prefer, you can also run the analysis locally. Make sure you have a log file at `logs/full_log.txt`, then execute:

```bash
python pipeline-oracle.py
```

This will:
- Read the log file.
- Send the logs to OpenAI for analysis.
- Generate an `analysis_report.md` with AI-generated insights.

---

## Contributing 🙌

Contributions are welcome! Please fork this repository, create a new branch, and open a pull request with your changes.

---

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements 🙏

- [OpenAI](https://openai.com) for providing the powerful GPT-4 Turbo model.
- [GitHub](https://github.com) for enabling seamless CI/CD workflows with GitHub Actions.
