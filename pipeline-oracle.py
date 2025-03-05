import asyncio
import logging
import os
import sys
from pathlib import Path
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Configuration from Environment Variables
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

# Log Processing Configuration
MAX_LINES = int(os.getenv('MAX_LOG_LINES', '200'))
MAX_LOG_SIZE = int(os.getenv('MAX_LOG_SIZE', '10000'))

# Define log directory
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "full_log.txt"

# Validate API Key
if not API_KEY:
    logging.error("OpenAI API key not found. Please set it in the environment variable 'OPENAI_API_KEY'.")
    sys.exit(1)

# Initialize OpenAI Client with flexible configuration
client = AsyncOpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


def configure_logging():
    """
    Configure logging with dynamic log level and format.
    """
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_format = os.getenv('LOG_FORMAT', '%(levelname)s: %(message)s')

    try:
        logging.basicConfig(
            level=getattr(logging, log_level),
            format=log_format
        )
    except (ValueError, AttributeError):
        logging.warning(f"Invalid log level '{log_level}'. Defaulting to INFO.")
        logging.basicConfig(level=logging.INFO)


def find_failed_step_log() -> str:
    """
    Reads logs, extracts the failed step logs, and returns them.
    Supports customizable log extraction.
    """
    # Validate log file
    if not LOG_FILE.exists():
        logging.error("Log file not found. Exiting.")
        sys.exit(1)

    # Read logs
    logs = LOG_FILE.read_text(encoding="utf-8").strip()

    if not logs:
        logging.error("Log file is empty. Exiting.")
        sys.exit(1)

    # Configurable failure keywords
    failure_keywords = os.getenv(
        'FAILURE_KEYWORDS',
        'failed,error,exception,command exited with'
    ).lower().split(',')

    # Extract logs
    lines = logs.splitlines()
    failed_step_logs = []
    capture = False

    for line in lines:
        # Check for failure keywords
        if any(keyword in line.lower() for keyword in failure_keywords):
            capture = True
            failed_step_logs.append(line)
        elif capture:
            failed_step_logs.append(line)
            if len(failed_step_logs) >= MAX_LINES:
                break

    # Determine log extraction strategy
    if failed_step_logs:
        extracted_logs = "\n".join(failed_step_logs)
        logging.info("Extracted logs from the failed step.")
    else:
        extracted_logs = "\n".join(lines[-MAX_LINES:])  # Get last N lines
        logging.warning("Could not identify a specific failed step, using last lines of log.")

    # Limit log size
    return extracted_logs[:MAX_LOG_SIZE]


async def analyze_logs_with_ai(logs: str) -> str:
    """
    Sends the logs to AI for analysis with configurable prompt.
    """
    # Custom prompt from environment, with fallback
    default_prompt = (
        "Analyze the following GitHub Actions workflow failure logs. "
        "Identify the root cause, suggest a fix, and outline debugging steps.\n\n"
        "Logs:\n"
        f"{logs}\n\n"
        "Please format your response with sections for **Analysis**, **Proposed Fix**, and **Next Steps**."
    )

    prompt = os.getenv('CUSTOM_PROMPT', default_prompt)

    try:
        logging.info(f"Sending logs to AI using model: {MODEL}")
        logging.info(f"Base URL: {BASE_URL}")

        response = await asyncio.wait_for(
            client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": os.getenv(
                            'SYSTEM_PROMPT',
                            "You are a CI/CD and DevOps expert. Provide clear, actionable debugging insights."
                        )
                    },
                    {"role": "user", "content": prompt}
                ]
            ),
            timeout=float(os.getenv('API_TIMEOUT', '90'))  # Configurable timeout
        )

        logging.info("AI analysis complete.")
        return response.choices[0].message.content if response.choices else ""

    except asyncio.TimeoutError:
        logging.error("AI API call timed out.")
        return "AI analysis timed out. Try running again with a smaller log file."

    except Exception as e:
        logging.error(f"Error during AI analysis: {e}")
        return f"AI analysis failed due to an unexpected error: {e}"


async def main() -> None:
    """
    Main function to process logs and run AI analysis.
    """
    # Configure logging based on environment
    configure_logging()

    # Process logs
    logs = find_failed_step_log()
    analysis = await analyze_logs_with_ai(logs)

    # Report generation
    if analysis:
        logging.info("\n=== AI Analysis Report ===\n")
        logging.info(analysis)

        report_path = Path(os.getenv('REPORT_PATH', 'analysis_report.md'))
        report_path.write_text(analysis, encoding="utf-8")

        logging.info(f"Analysis report saved to '{report_path.resolve()}'")
    else:
        logging.error("No analysis report generated.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())