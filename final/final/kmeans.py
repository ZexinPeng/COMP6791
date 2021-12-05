from bs4 import BeautifulSoup
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans

import scrapy
import logging
from optparse import OptionParser
import sys
import os
from time import time

import numpy as np

documents = []
cluster_num = 6
for root, dirs, files in os.walk(r"files"):
    for file in files:
        file_path = os.path.join(root, file)
        f = open(file_path, "r", encoding='utf-8')
        documents.append(BeautifulSoup(f.read(), features="lxml").get_text().replace('\n', '').replace('\r', ''))
        f.close()
print("%d documents" % len(documents))
print("%d categories" % cluster_num)

print("Extracting features from the training dataset using a sparse vectorizer")
t0 = time()

vectorizer = TfidfVectorizer(
    max_df=0.5,
    min_df=2,
    stop_words="english",
    use_idf=True,
)
X = vectorizer.fit_transform(documents)
print(X)
print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X.shape)
print()

km = KMeans(
    n_clusters=cluster_num,
    init="k-means++",
    max_iter=100,
    n_init=1,
    verbose=True,
)

print("Clustering sparse data with %s" % km)
t0 = time()
km.fit(X)
print("done in %0.3fs" % (time() - t0))
print()

print("Top terms per cluster:")

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()
for i in range(cluster_num):
    print("Cluster %d:" % i, end="")
    for ind in order_centroids[i, :20]:
        print(" %s" % terms[ind], end="")
    print()