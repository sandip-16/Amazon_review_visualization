import index2
from flask import Flask, request,render_template
import matplotlib.pyplot as plotter
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
    db= index2.database_cursor_obj()
    query_result = db['user_auth'].find({"uname": username, "passwd": int(password)}).count()
    del db
    if not query_result:
        return "email-id or password is wrong"
    else:
        return render_template('chart.html', keys=index2.top_ids)

@app.route('/chart',methods=["GET","POST"])
def chart():
    abc =request.form.get("id1")
    pieLabels = 'Positive','Negative','Neutral'
    pievalue=index2.pie_chart_value_extractor(abc)
    populationShare = pievalue
    figureObject, axesObject = plotter.subplots()
    axesObject.pie(populationShare,labels=pieLabels,autopct='%1.2f',startangle=90)
    axesObject.axis('equal')
    plotter.savefig('./images/'+abc+'.png')
    path2='./images/top_five.png'
    path='./images/'+abc+'.png'
    return render_template('plot.html', path=path,path1=path2)

