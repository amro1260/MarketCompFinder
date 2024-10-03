#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import json
import glob

import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

import spacy
from nltk.corpus import stopwords
import spacy.cli
spacy.cli.download("en_core_web_sm")

import pyLDAvis
import pyLDAvis.gensim_models

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Function: Lemmatization
def lemmatization(texts, allowed_postags=["NOUN", "ADJ", "VERB", "ADV"]):
    """Lemmatizes the text, reducing words to their base forms."""
    nlp = spacy.load("en_core_web_lg", disable=["parser", "ner"])
    texts_out = []
    for text in texts:
        doc = nlp(text)
        new_text = []
        for token in doc:
            if token.pos_ in allowed_postags:
                new_text.append(token.lemma_)
        final = " ".join(new_text)
        texts_out.append(final)
    return texts_out

# Function: Tokenization and Preprocessing
def gen_words(texts):
    """Tokenizes the text into individual words."""
    final = []
    for text in texts:
        new = gensim.utils.simple_preprocess(text, deacc=True)
        final.append(new)
    return final

# Function: Build LDA Model
def build_lda_model(corpus, id2word, num_topics=10):
    """Builds the LDA topic model."""
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=id2word,
                                                num_topics=num_topics,
                                                random_state=100,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                alpha="auto")
    return lda_model

# Fetch two URLs related to competitors (these functions need to be defined)
get_ipython().run_line_magic('run', 'url_f.ipynb')
get_ipython().run_line_magic('run', 'html-text.ipynb')

url1 = find_url(input())  # First URL
url2 = find_url(input())  # Second URL

# Extract HTML content from both URLs (these functions need to be defined)
text1 = extract_clean_text_from_related_urls(url1)
text2 = extract_clean_text_from_related_urls(url2)

# Preprocessing for URL1
lemmatized_texts1 = lemmatization(text1)
data_words1 = gen_words(lemmatized_texts1)
id2word1 = corpora.Dictionary(data_words1)
corpus1 = [id2word1.doc2bow(text) for text in data_words1]

# Preprocessing for URL2
lemmatized_texts2 = lemmatization(text2)
data_words2 = gen_words(lemmatized_texts2)
id2word2 = corpora.Dictionary(data_words2)
corpus2 = [id2word2.doc2bow(text) for text in data_words2]

# Train LDA models separately
lda_model1 = build_lda_model(corpus1, id2word1, num_topics=10)  # Model for URL1
lda_model2 = build_lda_model(corpus2, id2word2, num_topics=10)  # Model for URL2

# Output LDA topics for both URLs
print("Topics from URL1:")
print(lda_model1.print_topics())

print("\nTopics from URL2:")
print(lda_model2.print_topics())

# Visualize Topics Separately (Optional)
pyLDAvis.enable_notebook()
vis1 = pyLDAvis.gensim.prepare(lda_model1, corpus1, id2word1, mds="mmds", R=30)
vis2 = pyLDAvis.gensim.prepare(lda_model2, corpus2, id2word2, mds="mmds", R=30)

# Display the visualizations
print("\nURL1 Topics Visualization")
vis1

print("\nURL2 Topics Visualization")
vis2

# Compare Topics (Calculate Jaccard Similarity between topic words)
def jaccard_similarity(list1, list2):
    """Calculates the Jaccard similarity between two lists of words."""
    set1, set2 = set(list1), set(list2)
    return len(set1.intersection(set2)) / len(set1.union(set2))

# Extract words from topics
topics_url1 = [[word for word, _ in lda_model1.show_topic(topicid, topn=10)] for topicid in range(10)]
topics_url2 = [[word for word, _ in lda_model2.show_topic(topicid, topn=10)] for topicid in range(10)]

# Compare each topic from URL1 with each topic from URL2
similarity_scores = []
for i, topic1 in enumerate(topics_url1):
    for j, topic2 in enumerate(topics_url2):
        similarity = jaccard_similarity(topic1, topic2)
        similarity_scores.append((i, j, similarity))

# Print similarity scores for each topic pair
print("\nJaccard Similarity between URL1 and URL2 Topics:")
for i, j, sim in similarity_scores:
    print(f"Topic {i} from URL1 and Topic {j} from URL2 have Jaccard Similarity: {sim:.2f}")

