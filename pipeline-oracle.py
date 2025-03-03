import os
import sys
import logging
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from openai import AsyncOpenAI

# Configure logging for better output
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Load environment variables from .env file
load_dotenv()

# Ensure OpenAI API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("OpenAI API key not found. Please set it in the environment variable 'OPENAI_API_KEY'.")
    sys.exit(1)

# Initialize AsyncOpenAI client with the API key
client = AsyncOpenAI(api_key=api_key)

# Define log file directory
LOG_DIR = Path("logs")


def find_log_file() -> Path:
    """
    Dynamically find the first .txt log file in the LOG_DIR.
    Exits if the directory does not exist or no log file is found.
    """
    if not LOG_DIR.exists():
        logging.error("Logs directory does not exist. Skipping analysis.")
        sys.exit(1)

    log_files = list(LOG_DIR.glob("**/*.txt"))
    if not log_files:
        logging.error("No log files found in logs/. Skipping analysis.")
        sys.exit(1)

    logging.info(f"Found log file at: {log_files[0].resolve()}")
    return log_files[0]


def read_log_file(log_file: Path) -> str:
    """
    Reads and returns the content of the provided log file.
    Exits if the file is not found or is empty.
    """
    if not log_file.exists():
        logging.error(f"Log file not found: {log_file}")
        sys.exit(1)

    logs = log_file.read_text(encoding="utf-8").strip()
    if not logs:
        logging.error("Log file is empty. Skipping analysis.")
        sys.exit(1)
    return logs


async def analyze_logs_with_ai(logs: str) -> str:
    """
    Asynchronously sends the provided logs to OpenAI for analysis using AsyncOpenAI
    and returns the AI-generated response.
    """
    try:
        logging.info("Sending logs to OpenAI for analysis...")
        response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant analyzing CI/CD pipeline logs. "
                        "Provide clear, actionable advice on how to fix any failures."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Analyze the following logs from a GitHub Actions workflow and "
                        f"suggest specific fixes for any failures:\n\n{logs}"
                    )
                }
            ],
            timeout=60
        )
        logging.info("AI analysis complete.")
        logging.debug(f"Full AI response: {response}")

        # Use attribute access instead of .get()
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            logging.error("No valid response received from OpenAI.")
            return ""
    except Exception as e:
        logging.error(f"Unexpected error during AI analysis: {e}")
        return ""


async def main():
    """
    Main async function to analyze logs and output AI-generated insights.
    """
    log_file = find_log_file()
    logs = read_log_file(log_file)
    analysis = await analyze_logs_with_ai(logs)

    if analysis:
        logging.info("\n=== AI Analysis Report ===\n")
        logging.info(analysis)
        report_path = Path("analysis_report.md")
        report_path.write_text(f"# CI/CD Pipeline Failure Analysis\n\n{analysis}", encoding="utf-8")
        logging.info(f"Analysis report saved to '{report_path.resolve()}'")
    else:
        logging.error("No analysis report generated.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
