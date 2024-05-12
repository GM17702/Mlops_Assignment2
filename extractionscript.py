import requests
from bs4 import BeautifulSoup
import json
import re
from airflow import __version__ as AIRFLOW_VERSION

# Importing ti if using Airflow version >= 2
if AIRFLOW_VERSION.startswith('2'):
    from airflow.operators.python import task
else:
    from airflow.models import TaskInstance

    def task(func):
        def inner(*args, **kwargs):
            ti = TaskInstance(args[0], args[1], args[2])
            return func(ti, *args[3:], **kwargs)
        return inner

# Function to extract data from dawn.com
@task
def extract_dawn_data(ti):
    dawn_url = "https://www.dawn.com/"
    response = requests.get(dawn_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extracting links
        dawn_links = [link.get('href') for link in soup.find_all('a', href=True)]
        # Extracting titles and descriptions
        articles = soup.find_all('article')
        dawn_articles_data = []
        for article in articles:
            try:
                # Extract title
                title = article.find('h2', class_='story__title').text.strip()
                # Extract description
                description = article.find('div', class_='story__excerpt').text.strip()
            except Exception as e:
                continue
            dawn_articles_data.append({'title': title, 'description': description})
        return dawn_links, dawn_articles_data
    else:
        print("Failed to fetch data from Dawn.com")
        return [], []

# Function to extract data from bbc.com
@task
def extract_bbc_data(ti):
    bbc_url = "https://www.bbc.com/"
    response = requests.get(bbc_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extracting links
        bbc_links = [link.get('href') for link in soup.find_all('a', href=True)]
        # Extracting titles and descriptions
        articles = soup.find_all('div')
        bbc_articles_data = []
        for article in articles:
            try:
                heading = article.find("h2", {"data-testid": "card-headline"}).text.strip()
                description = article.find("p", {"data-testid": "card-description"}).text.strip()
            except Exception as e:
                continue
            bbc_articles_data.append({'title': heading, 'description': description})
        return bbc_links, bbc_articles_data
    else:
        print("Failed to fetch data from BBC.com")
        return [], []

# Function to preprocess links
def preprocess_links(links, base_url):
    processed_links = []
    for link in links:
        if link.startswith("/"):
            processed_links.append(base_url + link)
        else:
            processed_links.append(link)
    return processed_links

# Function to preprocess articles
def preprocess_articles(articles):
    processed_articles = []
    unique_titles = set()
    for article in articles:
        title = re.sub(r'\\u[0-9A-Fa-f]{4}', lambda x: bytes(x.group(), 'utf-8').decode('unicode-escape'), article['title'])
        description = re.sub(r'\\u[0-9A-Fa-f]{4}', lambda x: bytes(x.group(), 'utf-8').decode('unicode-escape'), article['description'])
        if title not in unique_titles:
            processed_articles.append({'title': title.strip(), 'description': description.strip()})
            unique_titles.add(title)
    return processed_articles

# Function to preprocess Dawn data
@task
def preprocess_dawn_data(ti, data):
    dawn_links, dawn_articles_data = data
    # Preprocess dawn data here
    dawn_links = preprocess_links(dawn_links, "https://www.dawn.com")
    dawn_articles_data = preprocess_articles(dawn_articles_data)
    return dawn_links, dawn_articles_data

# Function to preprocess BBC data
@task
def preprocess_bbc_data(ti, data):
    bbc_links, bbc_articles_data = data
    # Preprocess bbc data here
    bbc_links = preprocess_links(bbc_links, "https://www.bbc.com")
    bbc_articles_data = preprocess_articles(bbc_articles_data)
    return bbc_links, bbc_articles_data
@task
def store_data_function(**kwargs):
    ti = kwargs['ti']
    dawn_data = ti.xcom_pull(task_ids='preprocess_dawn_data')
    bbc_data = ti.xcom_pull(task_ids='preprocess_bbc_data')
    
    # Combine or use the data as needed
    combined_data = {
        "dawn": dawn_data,
        "bbc": bbc_data
    }
    
    # Store data in a JSON file
    with open('data.json', 'w') as json_file:
        json.dump(combined_data, json_file)

    print("Data stored successfully in 'data.json'")