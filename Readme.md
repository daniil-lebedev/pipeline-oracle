Below is an updated README for **Pipeline Oracle v1.1.0** that reflects the latest changes—using a GitHub PAT for authentication, generating a comprehensive CI/CD summary, and optionally creating a GitHub issue from the report.

---

# Pipeline Oracle 🚀

**Pipeline Oracle** is a cutting-edge CI/CD failure analysis tool that leverages the power of AI (via OpenAI's GPT-4 Turbo) to provide clear, actionable insights for fixing pipeline issues. Integrated with GitHub Actions, Pipeline Oracle automatically fetches logs from failed workflows, analyzes them, and generates detailed reports to help your team quickly diagnose and resolve issues. 🔧🤖

---

## Features ✨

- **Automated Log Collection:** 📂  
  Automatically collects logs from failed GitHub Actions workflows.

- **AI-Powered Analysis:** 🤖  
  Uses OpenAI's GPT-4 Turbo to analyze logs and provide actionable remediation suggestions.

- **CI/CD Summary Generation:** 📊  
  Produces a comprehensive summary of pipeline failures, which is uploaded as an artifact and appended to the GitHub Actions summary.

- **Optional GitHub Issue Creation:** 📝  
  If enabled, automatically creates a GitHub issue with the analysis report—assigning it to the merging user for prompt follow-up.

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

4. **Artifact Upload & Summary:** 📤  
   The analysis report and logs are uploaded as artifacts, and the report is appended to the GitHub Actions summary.

5. **Optional Issue Creation:** 📝  
   Depending on configuration, a GitHub issue can be created with the analysis report.

---

## Setup and Installation 🔧

### Prerequisites

- A GitHub repository with workflows using GitHub Actions.
- An **OpenAI API key** (set as the repository secret `OPENAI_API_KEY`). 🔑
- A **GitHub Personal Access Token (PAT)** with the required permissions (set as the repository secret `GH_PAT`). 🔒  
  *Make sure the PAT has sufficient scopes (for example, `repo` and `workflow` scopes) and that your workflow permissions include `issues: write` if you want to create issues.*

---

## Quick Start: Add Pipeline Oracle via a Composite GitHub Action ⚡

Pipeline Oracle is available as a reusable composite GitHub Action. Follow these steps to integrate it:

1. **Publish/Install the Action:**  
   Pipeline Oracle is published on the GitHub Marketplace as [daniil-lebedev/pipeline-oracle](https://github.com/daniil-lebedev/pipeline-oracle).  
   *(Replace with the actual link once published.)*

2. **Configure Your Workflow:**  
   Create a workflow file (e.g., `.github/workflows/on-failure.yaml`) in your repository with the following content:

   ```yaml
   name: Pipeline Oracle

   permissions:
     contents: read
     actions: write
     issues: write

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
           uses: daniil-lebedev/pipeline-oracle@v1.1.0
           with:
             workflow-to-track: "Deploying to Prod"
             gh-pat: ${{ secrets.GH_PAT }}
             openai-api-key: ${{ secrets.OPENAI_API_KEY }}
             create-github-issue: "Y"  # Set to "Y" to create a GitHub issue, or "N" to disable
   ```

3. **Configure Secrets:**  
   In your repository settings, add the following secrets:
   - **OPENAI_API_KEY:** Your OpenAI API key.
   - **GH_PAT:** Your GitHub Personal Access Token.

---

## Running Pipeline Oracle Locally 💻

If you prefer, you can run the analysis locally. Make sure you have a log file at `logs/full_log.txt`, then execute:

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

---

By packaging Pipeline Oracle as a composite GitHub Action, new projects can integrate it by simply adding one minimal workflow file and configuring their own credentials via repository secrets. This plug-and-play approach keeps your CI/CD failure analysis powerful yet easy to adopt.

---

## Pipeline Oracle v1.1.0 Release Note

### Overview
Pipeline Oracle v1.1.0 introduces major enhancements to our CI/CD failure analysis tool. This version removes the need for a custom PAT by leveraging it only for authentication and includes features to generate a comprehensive CI/CD summary. Optionally, it can create a GitHub issue from the report—assigning it to the merging user.

### What’s New
- **PAT Dependency (for now):**  
  The action still uses a GitHub Personal Access Token (PAT) for GitHub CLI commands, ensuring the necessary permissions are available.
  
- **CI/CD Summary Generation:**  
  Generates a detailed summary from failed workflows, uploading the report as an artifact and appending it to the GitHub Actions summary.
  
- **Optional Issue Creation:**  
  An input flag (`create-github-issue`) allows you to choose whether to create a GitHub issue from the analysis report.
  
- **Improved Error Handling & Cleanup:**  
  Every run step now specifies `shell: bash`, and a cleanup step removes temporary log files.

### How to Upgrade
1. **Update Your Workflow Reference:**  
   Change your action reference to `v1.1.0` in your workflow file.
   
2. **Configure Secrets:**  
   Set the **OPENAI_API_KEY** and **GH_PAT** secrets in your repository.
   
3. **Deploy & Monitor:**  
   The updated action will automatically generate a CI/CD summary upon workflow failures and, if enabled, create a GitHub issue with the report.

### Known Limitations
- **Token Permissions:**  
  Ensure your PAT has the necessary scopes (e.g., `repo`, `workflow`) and your workflow permissions include `issues: write` for issue creation.
- **Mermaid Diagram Rendering:**  
  AI-generated Mermaid diagrams might occasionally have syntax issues. Verify using the [Mermaid Live Editor](https://mermaid.live/).
- **Complex Workflows:**  
  The current log-fetching logic might require further customization for very complex or multi-stage pipelines.

### Feedback & Contributions
- **Report Issues:**  
  Submit bugs or feature requests via [GitHub Issues](../../issues).
- **Contribute:**  
  Fork the repository, create a branch, and submit a pull request with improvements.

---

Thank you for using Pipeline Oracle! We hope v1.1.0 enhances your CI/CD failure analysis process by providing clear insights and streamlined troubleshooting using a secure, PAT-based approach. Enjoy faster insights and more effective automation!

---

This updated README and release note should now reflect the current state of Pipeline Oracle v1.1.0 while using a PAT for authentication and generating a comprehensive CI/CD summary.
