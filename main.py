"""Example code for the paper summary script"""
from src.paper_summary import (
    download_paper,
    get_paper_summary,
    load_openai_api_key,
    save_text_to_file,
)


def main():
    """Main function"""

    paper_url = "shorturl.at/yBHTV"
    paper_out = "./download/zhuo.pdf"
    summary_out = "./output/zhuo_summary.txt"
    text_out: Optional[str] = ".output/summary/text_out"

    # Load the OpenAI API key
    load_openai_api_key()

    # Download the paper
    if paper_url is not None:
        download_paper(paper_url, paper_out)

    # Get the summary of the paper
    paper_text, paper_summary = get_paper_summary(paper_out)

    # Save the summary of the paper
    save_text_to_file(paper_summary, summary_out)

    # Save the paper text
    if text_out is not None:
        save_text_to_file(paper_text, text_out)


if __name__ == "__main__":
    main()
