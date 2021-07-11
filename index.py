# -----   ***fake review detector ***
import pymongo
import matplotlib.pyplot as plotter
import pandas as pd
import numpy as np
import server
Productid=[]
top_ids=[]
categorywise=[]
filtered_categorywise =[]
top_five_products=[]
file = []
positive =[]
negative =[]
neutral =[]
keys=[]
def database_cursor_obj():
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
    db = client['review']
    return db

db =  database_cursor_obj()
table = db['Amazon'].find()
i = 1
for record in table:
    i += 1
    if (i < 1000):
        file.append((record["asin"], record['reviewText']))
    else:
        table.close()
        del db
        break

def sorting_review_on_id(sentance, polarity):
    if sentance[0] not in Productid:
            Productid.append(sentance[0])
            categorywise.append({sentance[0]: [{"pos": 0, "neg": 0, "neu": 0}]})
    else:

        i = -1
        for recrd in categorywise:
            i += 1
            for key in recrd:

                if sentance[0] == key:
                    val=categorywise[i][key]
                    if polarity=="pos":
                        val[0]["pos"] += 1
                    elif polarity == "neg":
                        val[0]["neg"] += 1
                    else:
                        val[0]["neu"] += 1


def filtering():
    cnt = -1
    for i in categorywise:
        cnt+=1
        for key in i:
            val = categorywise[cnt][key]
            total_review=val[0]["pos"] + val[0]["neg"] + val[0]["neu"]
            if total_review > 30:
                filtered_categorywise.append(i)
                top_ids.append(key)



def pievalueextractor(search):

    cnt = -1
    for i in filtered_categorywise:
        cnt += 1
        for key in i:
            if key == search:
                val = filtered_categorywise[cnt][key]
                # print(val[0]["pos"] ,val[0]["neg"] ,val[0]["neu"])
                return (val[0]["pos"] ,val[0]["neg"] ,val[0]["neu"])


def top_five_calculator():
    cnt = -1
    for product in filtered_categorywise:
        cnt += 1
        for key in product:
            val = filtered_categorywise[cnt][key]
            positive.append(val[0]["pos"])
            negative.append( val[0]["neg"])
            neutral.append( val[0]["neu"])
            keys.append(key)
            # print(val[0]["pos"] ,val[0]["neg"] ,val[0]["neu"])
            # retu0rn (val[0]["pos"] ,val[0]["neg"] ,val[0]["neu"])

def data_frame_creation():
    df = pd.DataFrame({
                        'pid':keys,
                        'pos': positive,
                       'neg': negative,
                       'neu': neutral,
                       })
    a = df.nlargest(20, ['pos', 'neg'])
    a['total']=a['pos']+ a['neg']+a['neu']
    a['pos_per'] = (a['pos'] / a['total']) * 100
    a['neg_per'] =(a['neg'] / a['total']) * 100
    a['neu_per'] =(a['neu'] / a['total']) * 100
    b = a.nlargest(6,['pos_per'])
    return b

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentimentAnalyzer = SentimentIntensityAnalyzer()
newSentance = []
for sentence in file:
    sentiment_scores = sentimentAnalyzer.polarity_scores(sentence[1])
    cnt = 0
    for result in sentiment_scores:
        print(result)
        cnt += 1
        if (cnt >= 4):
            if (sentiment_scores[result] > 0):
                sorting_review_on_id(sentence,"pos")
            elif (sentiment_scores[result] < 0):
                sorting_review_on_id(sentence,"neg")
            else:
                sorting_review_on_id(sentence,"neu")

filtering()
top_five_calculator()
top_five=data_frame_creation()

def plot_top_five():
    N = 6
    pos1 = top_five['pos']
    neg1 = top_five['neg']
    neu1 = top_five['neu']
    ind = np.arange(N)  # the x locations for the groups
    width = 0.50  # the width of the bars: can also be len(x) sequence

    p1 = plotter.bar(ind, pos1, width)
    p2 = plotter.bar(ind, neg1, width, bottom=pos1)
    p3 = plotter.bar(ind, neu1, width, bottom=[i + j for i, j in zip(pos1, neg1)])
    plotter.ylabel('Scores')
    plotter.title('Top Five Products Graph Representation')
    plotter.xticks(ind)
    plotter.yticks(np.arange(0, 150, 20))
    plotter.legend((p1[0], p2[0], p3[0]), ('Positive', 'Negative', 'Neutral'))
    plotter.savefig('./images/top_five.png')
plot_top_five()

if __name__=="__main__":
    server.app.run(debug=True, port=6300, host='localhost')

