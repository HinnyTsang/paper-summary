"""This module contains functions to download papers and summarize them
Copy from https://medium.com/geekculture/summarize-papers-with-chatgpt-8737ed520a07
"""
import logging
import os
from typing import Optional, cast
import urllib.request
from PyPDF2 import PageObject, PdfReader
from dotenv import load_dotenv
import openai

from .config import OPEN_AI_MODEL, system_message, user_content

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


def get_page_summary(page: PageObject) -> Optional[str]:
    """Get the summary of a page
    :param page: page to summarize
    :return: summary of the page
    """
    page_text = page.extract_text().lower()

    logging.info("Calling OPENAI API...")

    response: Optional[str] = None
    maximum_attempts: int = 5

    while response is None and maximum_attempts > 0:
        try:
            raw = openai.ChatCompletion.create(
                model=OPEN_AI_MODEL,
                messages=[system_message(), user_content(page_text)],
            )
            response = cast(
                str,
                raw["choices"][0]["message"]["content"],
            )
        except Exception as exception:
            logging.error(
                f"OPENAI API call failed with message {exception}, attempting again..."
            )
            maximum_attempts -= 1

    return response


def get_paper_summary(paper: str):
    """Get the summary of a paper
    :param paper: path to the paper
    :return: summary of the paper
    """
    with open(paper, "rb") as file:
        pdf_reader = PdfReader(file)
        responses = [get_page_summary(page) for page in pdf_reader.pages]
        paper_summary = [page for page in responses if page is not None]

    return "\n".join(paper_summary)


def save_paper_summary(paper_summary: str, summary_out: str) -> None:
    """Save the summary of a paper to a file
    :param paper_summary: summary of the paper
    :param paper_out: path to save the summary
    :return: None
    """
    with open(summary_out, "w", encoding="utf-8") as file:
        file.write(paper_summary)
