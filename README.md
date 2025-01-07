# Research Paper Processing Pipeline

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Install Dependencies](#install-dependencies)
  - [Set Up Google Cloud Credentials](#set-up-google-cloud-credentials)
- [Running the Application](#running-the-application)
- [Limitations and Known Issues](#limitations-and-known-issues)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

---

## Description

This project implements a robust pipeline designed to process research papers in PDF format. The pipeline performs the following tasks:

1. **Ingests** a research paper in PDF format.
2. **Extracts** raw text and metadata from the PDF.
3. **Processes** the content using a Language Model (LLM) to generate:
   - Metadata (title, authors, publication date, etc.).
   - Key findings and methodology.
   - Global summary and keywords.
4. **Stores** the processed results in [Google BigQuery](https://cloud.google.com/bigquery) for scalable storage and easy access.

---

## Features

- **Automated PDF Ingestion**: Seamlessly upload and process research papers.
- **Metadata Extraction**: Retrieve essential details like title, authors, and publication date.
- **Advanced Text Processing**: Utilize LLMs to summarize content and extract key insights.
- **Scalable Storage**: Store processed data efficiently in Google BigQuery for easy access and analysis.
- **Extensible Pipeline**: Easily extend the pipeline to incorporate additional processing steps or integrate with other services.

---

## Setup Instructions

### Prerequisites

Ensure you have the following installed and configured on your system:

- **Python 3.9+**
- **pip** (Python package installer)
- **Google Cloud SDK**: [Installation Guide](https://cloud.google.com/sdk/docs/install)
- A **Google Cloud Service Account Key** with permissions for BigQuery

### Clone the Repository

1. Open your terminal or command prompt.
2. Clone the repository and navigate into it:

   ```bash
   git clone https://github.com/Julijnv/challenge-two.git
   cd challenge-two


## Install Dependencies

    To install the required dependencies, run the following command in the root directory of the project:

        ```bash
        pip install -e .
         
## Set up Google Cloud Credentials

    1. **Install the Google Cloud SDK**  
    - Download and install the Google Cloud SDK from the official page:  
        [Google Cloud SDK Documentation](https://cloud.google.com/sdk/docs/install)

    2. **Initialize Google Cloud**  
    - Run the following command to initialize Google Cloud:  
        ```bash
        gcloud init
        
    - This command will guide you through:  
        - Logging in with your Google account.  
        - Selecting the appropriate Google Cloud project.

    3. **Update the Project in Your Code**  
    - Open the `main.py` file in the `src` directory.
    - Locate the line where the BigQuery table is defined:
        ```python
        table_id = "your_project_id.your_dataset_id.your_table_name"
        
    - Replace `your_project_id` with your Google Cloud project ID.  
        For example:  
            ```python
            table_id = "my-project-id.paper_summarize.papers"
        

    4. **Create a Service Account Key**  
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).  
    - Navigate to **IAM & Admin > Service Accounts**.  
    - Select your project, click **Create Service Account**, and follow these steps:  
        - Provide a name for the service account.  
        - Assign it the role **BigQuery Admin**.  
        - Click **Done** and then **Manage Keys**.  
        - Add a new key in JSON format and download the file.  

    5. **Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable**  
    - Use the downloaded JSON key file to set the environment variable:

    On Linux/Mac:  
        ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service_account.json"

    On Windows(CMD):  
        ```bash
        set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\service_account.json"

## Run the Application

    To execute the application, run the following command:

    ```bash
    python src/main.py
     
## Limitations and Known Issues
### Prototype Limitations

    The language model (LLM) used is not fine-tuned for academic papers. As a result:
    - Metadata (e.g., title, authors, and publication date) may be incomplete or inaccurate.
    - Summaries and extracted findings may not fully capture the essence of the paper.



