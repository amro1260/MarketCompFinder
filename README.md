
# Business Competitors Finder using HTML Data
This project idea focuses on identifying and analyzing potential business competitors by extracting and processing textual data from their websites. Using web scraping and natural language processing (NLP), the system identifies relevant competitors by comparing the content of different company websites. The project implements Latent Dirichlet Allocation (LDA) for topic modeling, allowing users to analyze and compare topics across various competitors' websites.

## Features
Competitor URL Finder: Automatically search for and identify URLs related to a business domain or industry.
HTML Content Extraction: Extract and clean text from HTML pages of potential competitors’ websites.
Topic Modeling: Perform topic modeling using LDA to uncover common themes and topics from competitor websites.
Competitor Comparison: Compare competitors based on topic distributions, enabling businesses to understand where they overlap or differ in their offerings or content.
Document Similarity: Calculate and visualize document similarity between competitors based on their website content using Cosine Similarity and Jaccard Similarity.
How It Works

### Find Competitor URLs:
The find_url() function searches for URLs related to a business or industry based on a search query.

### Extract HTML Content:
Using extract_clean_text_from_related_urls(), HTML content from the identified URLs is extracted and cleaned for analysis.

### Perform Topic Modeling:
LDA models are trained on the text extracted from competitor websites to reveal key topics and themes across different competitors.

### Compare Competitors:
Topics from each competitor are compared to identify similarities and differences in their website content.

### Document Similarity:
Measure the similarity between competitors using Cosine Similarity and Jaccard Similarity to quantify the overlap in content.
