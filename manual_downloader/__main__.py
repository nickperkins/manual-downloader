import requests
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import argparse
import tempfile
import filecmp
import logging


def download_pdf(url, save_path):
    """
    Downloads a PDF file from the given URL and saves it to the specified path.

    Args:
        url (str): The URL of the PDF file to download.
        save_path (str): The path where the downloaded PDF file should be saved.

    Returns:
        None
    """

    response = requests.get(url)
    # mkdir if the directory does not exist
    save_dir = "/".join(save_path.split("/")[:-1])
    os.makedirs(save_dir, exist_ok=True)

    # save the PDF to the specified path

    with open(save_path, 'wb') as file:
        file.write(response.content)
    logging.debug(f"PDF downloaded and saved to {save_path}")


def get_child_pages(url):
    """
    Retrieves the child pages of a given URL recursively.

    Args:
        url (str): The URL of the main page.

    Returns:
        list: A list of links that are children of the main page.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # find each link in the response
    child_pages = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith(url):
            child_pages.append(href)

    # recursively call this function for each child page
    # if the child page is not already in the list
    for page in child_pages:
        if page not in child_pages:
            child_pages.extend(get_child_pages(page))

    # return a list of links that are children of the main page
    return child_pages


def get_pdf_list(child_pages):
    """
    Download PDF files from a list of child pages.

    Args:
        child_pages (list): List of URLs of child pages.
        save_dir (str): Directory path to save the downloaded PDF files.

    Returns:
        None
    """
    downloads = []
    for page in child_pages:
        response = requests.get(page)
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            filename = urlparse(href).path.split("/")[-1]
            # check if the file is a PDF
            if filename.endswith(".pdf") and href not in downloads:
                downloads.append(href)

    return downloads


def download_pdfs(pdf_list, save_dir):
    """
    Download PDF files from a list of URLs.

    Args:
        pdf_list (list): List of URLs of PDF files to download.
        save_dir (str): Directory path to save the downloaded PDF files.

    Returns:
        None
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        for pdf in pdf_list:
            filename = urlparse(pdf).path.split("/")[-1]
            tmp_save_path = os.path.join(tmpdir, filename)
            download_pdf(pdf, tmp_save_path)
            save_path = os.path.join(save_dir, filename)
            if os.path.exists(save_path):
                if filecmp.cmp(tmp_save_path, save_path):
                    logging.info(f"PDF already exists at {save_path}, skipping.")
                    continue
            os.rename(tmp_save_path, save_path)
            logging.info(f"PDF saved to {save_path}")

    print("All PDFs downloaded successfully.")


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(
        description='PDF Grabber for Motorsport Australia Manual.')
    parser.add_argument('-u', '--url', type=str, help='Base URL of the manual',
                        default="https://www.motorsport.org.au/regulations/manual")
    parser.add_argument('-s', '--save_dir', type=str, help='Directory path to save the downloaded PDF files',
                        default=os.path.join(os.getcwd(), "pdfs"))
    args = parser.parse_args()

    child_pages = get_child_pages(args.url)
    pdf_list = get_pdf_list(child_pages)
    download_pdfs(pdf_list, args.save_dir)
