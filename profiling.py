import pymongo
import matplotlib.pyplot as plotter
import pandas as pd
import numpy as np

from nltk.sentiment.vader import SentimentIntensityAnalyzer

product_id_and_overall_result = dict()


def database_cursor_obj():
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    db = client['review']
    return db


def limiting_number_of_records_to_process():
    print("working")
    # 11.681
    db = database_cursor_obj()
    collection_containt = db['Amazon'].find()
    # return [(record["asin"], record['reviewText']) for index, record in enumerate(collection_containt, start=1) if
    #         index < 1000]
    for index, value in enumerate(collection_containt):
        if index < 1000000:
            yield value




obj = limiting_number_of_records_to_process()
for k, v in enumerate(obj):
    print(k)
    #calculate_sentiment_scores_of_each_record()