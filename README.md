
# LDA Topic Modeling for Document Comparison

This project implements **Latent Dirichlet Allocation (LDA)** to perform **topic modeling** on two sets of documents from two different URLs, allowing users to compare the topic distributions and measure the similarity between them. The project includes functionality for automatically finding related URLs and extracting clean text from them, as well as visualizations to help better understand the topics and similarities between documents.

## Features
- **LDA Model**: Train an LDA model on text data from URL1 and predict topics for documents from URL2.
- **URL Finder**: Automatically find and extract URLs related to a company or domain.
- **Text Extractor**: Extract clean text from HTML pages for analysis.
- **Topic Visualization**: Visualize topics using interactive PyLDAvis.
- **Topic Distribution Comparison**: Plot and compare topic distributions between two documents.
- **Document Similarity**: Calculate and visualize document similarity based on topic distributions using cosine similarity.
