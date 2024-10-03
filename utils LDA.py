#!/usr/bin/env python
# coding: utf-8

# In[11]:


from bs4 import BeautifulSoup
import urllib3
from urllib.error import HTTPError
import re
from googlesearch import search
import socket  # for checking the internet connection
import requests
from tld import get_tld
import html2text
from bs4 import BeautifulSoup
import requests


def find_url(search_query):
    
    # Function to perform Google search and return results
    def perform_search(query):
        search_results = []
        for result in search(query, num=20, stop=20, pause=2):
            search_results.append(result)
        return search_results

    # Clean and tokenize the search query
    search_query = [search_query]
    for query in search_query:
        cleaned_query = re.sub('[^a-zA-Z0-9]', ' ', query)
        search_terms = [term for term in cleaned_query.split(" ") if term != ""]
        formatted_search_terms = [''.join(filter(str.isalnum, term[0])) for term in search_terms]
        
        search_results = perform_search(cleaned_query)
        
        if not search_results:
            result_status = "no result"
        else:
            result_status = search_results

    # Regex to filter unwanted URLs
    unwanted_url_pattern = re.compile(
        ".*linkedin.com|.*twitter|.*owler|.*youtube|.*manta.com|.*cbinsights.com|.*opensecrets.org|.*pitchbook.com|"
        ".*buzzfile.com|.*massinvestordatabase.com|.*bciq.biocentury.com|.*google|.*youtube|.*wikipedia|.*www.eu-startups|"
        ".*btech.eu|.*facebook|.*finance.yahoo.com|.*business.site|.*github.io|.*newswire.com|.*cutestat.com|.*wlinkedin.com|"
        ".*bloomberg.com|.*deutsche-startups.de|.*marketwatch.com|.*[.]ft.com|.*money.cnn.com|.*wsj.com|.*economist.com|"
        ".*getrichslowly.org|.*twitter.com|.*crunchbase.com|.*xing|.*github.com|.*workable.com|.*glassdoor|.*startupgermany|"
        ".*berlinstartupjobs|.*jobs|.*https://shop.|.*https://job.", re.IGNORECASE)

    filtered_urls = list(filter(unwanted_url_pattern.match, result_status))
    filtered_result_status = [url for url in result_status if url not in filtered_urls]

    # Extract domain names from URLs
    domain_names = []
    for url in filtered_result_status:
        domain_info = get_tld(url, as_object=True)
        domain_names.append(domain_info.domain)

    # Clean up the domain names
    clean_domains = [re.sub('[^a-zA-Z0-9]', ' ', domain) for domain in domain_names]
    cleaned_domain_list = [''.join(domain.split(" ")) for domain in clean_domains]


    # Find best match
    best_match = []
    match_status = []

    # Exact match search
    exact_match_pattern = re.compile(r'^' + ''.join(str(i) for i in cleaned_query.split(" ")), re.IGNORECASE)
    exact_match = list(filter(exact_match_pattern.match, cleaned_domain_list))

    if exact_match:
        best_match = exact_match
        match_status = "exact match+"
    else:
        semi_match = list(filter(re.compile(search_terms[0], re.IGNORECASE).findall, cleaned_domain_list))
        if semi_match:
            for z in range(len(search_terms)):
                partial_match_pattern = re.compile(r'^' + ''.join(str(i) for i in search_terms[:len(search_terms)-z]), re.IGNORECASE)
                partial_match = list(filter(partial_match_pattern.match, cleaned_domain_list))

                if partial_match:
                    best_match = partial_match
                    match_status = ("semi match -", z)
                    break

    # If no matches found, assign a no result message
    if not best_match:
        match_status = "no result"

    # Find the shortest domain match based on character length
    matching_indexes = []
    for matched_domain in best_match:
        matching_indexes.extend([i for i, val in enumerate(cleaned_domain_list) if val == matched_domain])

    if not matching_indexes:
        best_url = "-"
        match_status = "no result"
    else:
        best_url = min([filtered_result_status[i] for i in matching_indexes], key=len)
        match_status = "exact match" if match_status == "exact match+" else match_status

    # Fetch HTML title from the best match URL
    try:
        best_url_title = BeautifulSoup(requests.get(best_url).content, features="lxml").title.string
        best_url_title = re.sub(r'[\t\r\n\x8f]', '', best_url_title)
    except:
        best_url_title = "-"

    # Final verification
    if best_url_title != "-" and re.search(str(search_query).strip("[]|'"), best_url_title, re.IGNORECASE):
        verification_result = "fine"
    else:
        verification_result = "check"

    return best_url






def extract_clean_text_from_related_urls(base_url):
    """Fetch URLs from a webpage, filter related URLs, and extract clean text."""
    
    # Set up headers to simulate a real browser request
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    # Fetch the base URL content
    response = requests.get(base_url, headers=headers)
    page_content = response.text
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    all_links = []
    
    # Extract all links from the page
    for link in soup.find_all('a'):
        href = link.get('href')
        all_links.append(href)
    
    # Filter the links to include only related URLs
    related_urls = []
    for link in all_links:
        if link is not None and base_url in link:
            related_urls.append(link)

                    
    # Extract and clean text from the filtered URLs
    extracted_texts = []
    for related_url in related_urls:
        related_page_content = requests.get(related_url, headers=headers).text
        
        # Use html2text to convert HTML to plain text
        html_to_text_converter = html2text.HTML2Text()
        
        # Ignore converting HTML links to plain text
        html_to_text_converter.ignore_links = True
        
        # Convert the related URL content to plain text
        plain_text = html_to_text_converter.handle(related_page_content)
        
        # Clean the text by removing non-alphanumeric characters and normalizing spaces
        regex = re.compile('[^a-zA-Z0-9]')
        cleaned_text = regex.sub(' ', plain_text)
        cleaned_text = " ".join(re.split(r"\s+", cleaned_text, flags=re.UNICODE))
        
        # Append the cleaned text to the list
        extracted_texts.append(cleaned_text)
    
    return extracted_texts


# In[12]:





# In[ ]:




