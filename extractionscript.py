import requests
from bs4 import BeautifulSoup
import json
import re

# Function to preprocess Dawn links
def preprocess_dawn_links(links):
    dawn_links = []
    for link in links:
        if link.startswith("/"):
            dawn_links.append("https://www.dawn.com" + link)
        else:
            dawn_links.append(link)
    return dawn_links

# Function to preprocess Dawn articles
def preprocess_dawn_articles(articles):
    processed_articles = []
    for article in articles:
        title = re.sub(r'\\u[0-9A-Fa-f]{4}', lambda x: bytes(x.group(), 'utf-8').decode('unicode-escape'), article['title'])
        description = re.sub(r'\\u[0-9A-Fa-f]{4}', lambda x: bytes(x.group(), 'utf-8').decode('unicode-escape'), article['description'])
        processed_articles.append({'title': title.strip(), 'description': description.strip()})
    return processed_articles

# Function to preprocess BBC links
def preprocess_bbc_links(links):
    bbc_links = []
    for link in links:
        if link.startswith("/"):
            bbc_links.append("https://www.bbc.com" + link)
        else:
            bbc_links.append(link)
    return bbc_links

# Function to preprocess BBC articles
def preprocess_bbc_articles(articles):
    processed_articles = []
    unique_titles = set()
    for article in articles:
        title = re.sub(r'\\u[0-9A-Fa-f]{4}', lambda x: bytes(x.group(), 'utf-8').decode('unicode-escape'), article['title'])
        description = re.sub(r'\\u[0-9A-Fa-f]{4}', lambda x: bytes(x.group(), 'utf-8').decode('unicode-escape'), article['description'])
        if title not in unique_titles:
            processed_articles.append({'title': title.strip(), 'description': description.strip()})
            unique_titles.add(title)
    return processed_articles

# Function to extract data from dawn.com
def extract_dawn_data():
    dawn_url = "https://www.dawn.com/"
    response = requests.get(dawn_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extracting links
        dawn_links = [link.get('href') for link in soup.find_all('a', href=True)]
        dawn_links = preprocess_dawn_links(dawn_links)
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
        dawn_articles_data = preprocess_dawn_articles(dawn_articles_data)
        return dawn_links, dawn_articles_data
    else:
        print("Failed to fetch data from Dawn.com")
        return [], []

# Function to extract data from bbc.com
def extract_bbc_data():
    bbc_url = "https://www.bbc.com/"
    response = requests.get(bbc_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extracting links
        bbc_links = [link.get('href') for link in soup.find_all('a', href=True)]
        bbc_links = preprocess_bbc_links(bbc_links)
        # Extracting titles and descriptions
        articles = soup.find_all('div')
        bbc_articles_data = []
        for article in articles:
            try:
                heading = article.find("h2", {"data-testid": "card-headline"}).text.strip()
                # description = article.find("p", class_="media__summary").text.strip()
                description = article.find("p", {"data-testid": "card-description"}).text.strip()
            except Exception as e:
                continue
            bbc_articles_data.append({'title': heading, 'description': description})
        bbc_articles_data = preprocess_bbc_articles(bbc_articles_data)
        return bbc_links, bbc_articles_data
    else:
        print("Failed to fetch data from BBC.com")
        return [], []

# Main function to run the extraction
def main():
    dawn_links, dawn_articles_data = extract_dawn_data()
    bbc_links, bbc_articles_data = extract_bbc_data()
    
    # Store the extracted data in a JSON file
    data = {
        "dawn": {
            "links": dawn_links,
            "articles": dawn_articles_data
        },
        "bbc": {
            "links": bbc_links,
            "articles": bbc_articles_data
        }
    }

    # Convert the special characters back to their original form
    data_str = json.dumps(data, ensure_ascii=False, indent=4)
    
    with open('extracted_data.json', 'w', encoding='utf-8') as f:
        f.write(data_str)
    print("Extracted data stored successfully in 'extracted_data.json'")

if __name__ == "__main__":
    main()
