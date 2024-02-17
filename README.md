# MA Manual Downloader

## Description

This project is a tool to bulk download PDFs linked to pages in a section of a website. By default, it will download the files that make up the Motorsport Australia manual.

## Installation

This project uses [Poetry](https://python-poetry.org/) as a dependency manager.

### Prerequisites

- Python 3.7 or higher
- Poetry

If you haven't installed Poetry yet, you can do so by running the following command:

```bash
curl -sSL https://install.python-poetry.org | python -
```

## Installing the Project

1. Clone the Project: Clone the project from the repository using git:

   ```bash
   git clone https://github.com/nickperkins/manual-downloader.git
   ```

2. Navigate to the Project Directory: Change your current directory to the project's directory:

    ```bash
    cd manual-downloader
    ```

3. **Install Dependencies**: Install the project dependencies using Poetry:

    ```bash
    poetry install
    ```

## Run the Project

You can run the project using Poetry.

```bash
poetry run manual_downloader
```
