import asyncio
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Load environment variables
load_dotenv()

# Ensure OpenAI API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("OpenAI API key not found. Please set it in the environment variable 'OPENAI_API_KEY'.")
    sys.exit(1)

# Initialize the AsyncOpenAI client
client = AsyncOpenAI(api_key=api_key)

# Define log file directory
LOG_DIR = Path("logs")


def find_log_file() -> Path:
    """
    Dynamically find the first .txt log file in LOG_DIR.
    Exits if directory or log file is not found.
    """
    if not LOG_DIR.exists():
        logging.error("Logs directory does not exist. Exiting.")
        sys.exit(1)
    log_files = list(LOG_DIR.glob("**/*.txt"))
    if not log_files:
        logging.error("No log files found in logs. Exiting.")
        sys.exit(1)
    logging.info(f"Found log file at: {log_files[0].resolve()}")
    return log_files[0]


def read_log_file(log_file: Path) -> str:
    """
    Reads and returns the content of the given log file.
    Exits if the file is not found or is empty.
    """
    if not log_file.exists():
        logging.error(f"Log file not found: {log_file}")
        sys.exit(1)
    logs = log_file.read_text(encoding="utf-8").strip()
    if not logs:
        logging.error("Log file is empty. Exiting.")
        sys.exit(1)
    return logs


def extract_error_snippet(logs: str) -> str:
    """
    Extracts an error snippet from the logs.
    Searches for a line containing "Traceback" or 'File "'
    and returns 3 lines before and 3 lines after that line.
    """
    lines = logs.splitlines()
    for i, line in enumerate(lines):
        if "Traceback" in line or 'File "' in line:
            start = max(0, i - 3)
            end = min(len(lines), i + 4)
            snippet = "\n".join(lines[start:end])
            logging.info("Error snippet extracted.")
            return snippet
    logging.info("No error snippet found in logs.")
    return ""


async def analyze_logs_with_ai(logs: str) -> str:
    """
    Sends the logs along with an extracted error snippet to OpenAI for analysis.
    The prompt instructs the AI to provide a detailed analysis, a proposed fix,
    and a diagram (in Mermaid syntax) illustrating how the error might have occurred.
    """
    error_snippet = extract_error_snippet(logs)
    prompt = (
        "Analyze the following logs from a GitHub Actions workflow failure and provide a detailed analysis, "
        "a proposed fix, and a diagram (in Mermaid syntax) illustrating how the error might have occurred.\n\n"
        "Full Logs:\n"
        f"{logs}\n\n"
        "Error Snippet (if any):\n"
        f"{error_snippet}\n\n"
        "Please format your response in Markdown with separate sections for **Analysis**, **Proposed Fix**, and **Diagram**."
    )
    try:
        logging.info("Sending logs and error snippet to OpenAI for analysis...")
        response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a DevOps and software engineering expert. Provide clear, actionable advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            timeout=60
        )
        logging.info("AI analysis complete.")
        logging.debug(f"Full AI response: {response}")
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            logging.error("No valid response received from OpenAI.")
            return ""
    except Exception as e:
        logging.error(f"Unexpected error during AI analysis: {e}")
        return ""


async def main() -> None:
    """
    Main async function to run the analysis and save the report.
    """
    log_file = find_log_file()
    logs = read_log_file(log_file)
    analysis = await analyze_logs_with_ai(logs)
    if analysis:
        logging.info("\n=== AI Analysis Report ===\n")
        logging.info(analysis)
        report_path = Path("analysis_report.md")
        report_path.write_text(analysis, encoding="utf-8")
        logging.info(f"Analysis report saved to '{report_path.resolve()}'")
    else:
        logging.error("No analysis report generated.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
