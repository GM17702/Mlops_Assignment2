# Mlops_Assignment2

## Overview
This Assignment focuses on building a robust data extraction and processing pipeline using Python, BeautifulSoup for web scraping, and Apache Airflow for workflow automation. The pipeline extracts data from dawn.com and BBC.com, preprocesses it, and stores it for further analysis.

## Tasks Completed
1. **Data Extraction:**
   - Utilized dawn.com and BBC.com as data sources.
   - Extracted links from the landing pages.
   - Extracted titles and descriptions from articles displayed on the homepages.

2. **Data Transformation:**
   - Preprocessed the extracted text data to clean and format it appropriately for analysis.

3. **Data Storage and Version Control:**
   - Stored the processed data in a JSON file.
   - Implemented Data Version Control (DVC) to track versions of the data.
   - Ensured each version is accurately recorded as changes are made.
   - Integrated with Google Drive for data storage.

4. **Apache Airflow DAG Development:**
   - Developed an Airflow DAG to automate the processes of extraction, transformation, and storage.
   - Ensured the DAG handles task dependencies and error management effectively.

## Project Structure

- **extractionscript.py:** Contains functions for data extraction, preprocessing, and storage.
- **my_dag.py:** Defines the Airflow DAG for workflow automation.
- **README.md:** Project overview, instructions, and documentation.
- **data.json:** Stored processed data.
- **.dvc/**: DVC directory for version control metadata.
- **dags/**: Airflow DAG directory.
- **requirements.txt:** Required dependencies for the project.

## Instructions

1. Set up Airflow and place `dag.py` in the `dags` folder.
2. Modify configurations in `dag.py` as needed (e.g., schedule interval, start date).
3. Run Airflow scheduler and web server.
4. Data will be automatically extracted, preprocessed, and stored according to the defined DAG.

## Notes

- For version control using DVC, initialize a DVC repository (`dvc init`) and link it with a GitHub repository.
- Use `dvc add` to track data files and `dvc push` to version them in the GitHub repository.
- Ensure proper error handling and logging in the Airflow DAG for monitoring and debugging.
