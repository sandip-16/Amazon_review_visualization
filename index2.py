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
def limiting_number_of_records_to_process():  # 11.681
    db =  database_cursor_obj()
    collection_containt = db['Amazon'].find()
    for index, review in enumerate(collection_containt):
        if index < 1000:
            yield review["asin"], review['reviewText']
    # return [(record["asin"], record['reviewText']) for index,record in enumerate(collection_containt,start=1) if index < 10000]   # 11.689
def calculating_review_id_total_score(product_id, polarity):  # 15.260
    if not product_id in product_id_and_overall_result:
        product_id_and_overall_result[product_id] = [0,0,0] # we are skipping first result so work on it later
    else:
        if polarity == "pos":
            product_id_and_overall_result[product_id][0] += 1
        elif polarity == "neg":
            product_id_and_overall_result[product_id][1] += 1
        else:
            product_id_and_overall_result[product_id][2] += 1
        
def calculate_sentiment_scores_of_each_record():
    sentimentAnalyzer = SentimentIntensityAnalyzer()
    for id, review in limiting_number_of_records_to_process():
        sentiment_scores = sentimentAnalyzer.polarity_scores(review)
        if sentiment_scores['compound'] < 0:
            calculating_review_id_total_score(id, "neg")
        elif sentiment_scores['compound'] > 0:
            calculating_review_id_total_score(id, "pos")
        else:
            calculating_review_id_total_score(id, "neu")

def eliminationg_product_having_less_reviews():
    return {key: value for key, value in product_id_and_overall_result.items() if sum(value) > 30}
def top_n_review_calculator(dict_after_elimination):
    df_Obj = pd.DataFrame.from_dict(dict_after_elimination, orient='index')
    top_n = df_Obj.nlargest(5, [0, 1])  # 0 for positive 1 for negative and 2 for neutral
    return top_n
def pie_chart_value_extractor(product_id):
    return tuple(dict_after_elimination[product_id])

def plot_vertical_bar_graph_for_top_five(top_n):
    N = 5
    pos = top_n[0]
    neg = top_n[1]
    neu = top_n[2]
    ind = np.arange(N)  # the x locations for the groups
    width = 0.50  # the width of the bars: can also be len(x) sequence
    p1 = plotter.bar(ind, pos, width)
    p2 = plotter.bar(ind, neg, width, bottom=pos)
    p3 = plotter.bar(ind, neu, width, bottom=[i + j for i, j in zip(pos, neg)])
    plotter.ylabel('Scores')
    plotter.title('Top Five Products Graph Representation')
    plotter.xticks(ind)
    plotter.yticks(np.arange(0, 150, 20))
    plotter.legend((p1[0], p2[0], p3[0]), ('Positive', 'Negative', 'Neutral'))
    plotter.savefig('./images/top_five.png')

from flask import Flask, request,render_template
app = Flask(__name__, static_folder='images')

@app.route('/')
def lets_start():
    return render_template("lets_start.html")

@app.route('/login',methods=["POST"])
def login():
    return render_template("form_ex.html")
@app.route('/login1',methods=["POST"])
def Authenticate():
    username = request.form['email']
    password = request.form['password']
    db= database_cursor_obj()
    query_result = db['user_auth'].find({"uname": username, "passwd": int(password)}).count()
    del db
    if not query_result:
        return "email-id or password is wrong"
    else:
        return render_template('chart.html', keys=top_ids)

@app.route('/chart',methods=["GET","POST"])
def chart():
    abc =request.form.get("id1")
    pieLabels = 'Positive','Negative','Neutral'
    pievalue = pie_chart_value_extractor(abc)
    populationShare = pievalue
    figureObject, axesObject = plotter.subplots()
    axesObject.pie(populationShare,labels=pieLabels,autopct='%1.2f',startangle=90)
    axesObject.axis('equal')
    plotter.savefig('./images/'+abc+'.png')
    path2='./images/top_five.png'
    path='./images/'+abc+'.png'
    return render_template('plot.html', path=path,path1=path2)


# function calls
if __name__=="__main__":
    calculate_sentiment_scores_of_each_record()
    dict_after_elimination = eliminationg_product_having_less_reviews()
    top_ids = dict_after_elimination.keys()
    top_n = top_n_review_calculator(dict_after_elimination)
    plot_vertical_bar_graph_for_top_five(top_n)
    app.run(debug=True, port=6300, host='localhost')

