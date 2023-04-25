"""
This module contains functions to download papers and summarize them
Copy from medium:
https://medium.com/geekculture/summarize-papers-with-chatgpt-8737ed520a07
"""
import logging
import os
from typing import Optional, Tuple, cast
from time import sleep
import urllib.request
from PyPDF2 import PageObject, PdfReader
from dotenv import load_dotenv
import openai

from .config import OPEN_AI_MODEL, system_message, user_content
from .models import OpenAPIResponse
from .utils import build_rate_limiter

logging.basicConfig(level=logging.INFO)


def load_openai_api_key() -> None:
    """Load the OpenAI API key from the .env file"""
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")


def download_paper(paper_url: str, paper_out: str) -> None:
    """Download a paper from a url and save it to a file
    :param paper_url: url of the paper
    :param paper_out: path to save the paper
    :return: None
    """
    logging.info(f"Downloading paper from {paper_url}... to {paper_out}...")

    urllib.request.urlretrieve(paper_url, paper_out)


def get_page_text(page: PageObject) -> str:
    """Get the text of a page
    :param page: page to get the text from
    :return: text of the page
    """
    page_text = page.extract_text().lower()
    return page_text


def get_page_summary(page_text: str, rate_limit: int = 3) -> Optional[str]:
    """Get the summary of a page
    :param page: page to summarize
    :param rate_limit: rate limit for the API call (requests / minute)
    :return: summary of the page
    """

    logging.info("Calling OPENAI API...")

    response: Optional[str] = None
    maximum_attempts: int = 5
    rate_limiter = build_rate_limiter(rate_limit)

    while response is None and maximum_attempts > 0:
        try:
            raw: OpenAPIResponse = cast(
                OpenAPIResponse,
                openai.ChatCompletion.create(
                    model=OPEN_AI_MODEL,
                    messages=[system_message(), user_content(page_text)],
                ),
            )
            response = raw["choices"][0]["message"]["content"]
        except Exception as exception:
            logging.error(f"OPENAI API call failed with message {exception}.")
            maximum_attempts -= 1
        rate_limiter()  # Sleep for 20 seconds to avoid rate limit (3 / minute)

    return response


def get_paper_summary(paper: str) -> Tuple[str, str]:
    """Get the summary of a paper
    :param paper: path to the paper
    :return: summary of the paper
    """
    with open(paper, "rb") as file:
        pdf_reader = PdfReader(file)
        pages_text = [get_page_text(page) for page in pdf_reader.pages]

    responses = [get_page_summary(page) for page in pages_text]
    paper_summary = [page for page in responses if page is not None]

    return "\n".join(pages_text), "\n".join(paper_summary)


def save_text_to_file(paper_summary: str, summary_out: str) -> None:
    """Save the summary of a paper to a file
    :param paper_summary: summary of the paper
    :param paper_out: path to save the summary
    :return: None
    """
    with open(summary_out, "w", encoding="utf-8") as file:
        file.write(paper_summary)
