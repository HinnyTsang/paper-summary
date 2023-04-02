"""Example code for the paper summary script"""
from src.paper_summary import (
    download_paper,
    get_paper_summary,
    load_openai_api_key,
    save_paper_summary,
)


def main():
    """Main function"""

    paper_url = "shorturl.at/yBHTV"
    paper_out = "./download/zhuo.pdf"
    summary_out = "./output/zhuo_summary.txt"

    # Load the OpenAI API key
    load_openai_api_key()

    # Download the paper
    download_paper(paper_url, paper_out)

    # Get the summary of the paper
    paper_summary = get_paper_summary(paper_out)

    # Save the summary of the paper
    save_paper_summary(paper_summary, summary_out)


if __name__ == "__main__":
    main()
