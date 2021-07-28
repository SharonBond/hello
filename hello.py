#!/usr/bin/env python

#import necessary libraries
# pip install flask 
#export FLASK_APP=hello
#flask run
from flask import Flask, json, render_template, request, redirect,url_for
import os


#create instance of Flask app
app = Flask(__name__)

#decorator 
@app.route("/")#, methods=['GET', 'POST'])
def intro():
    return render_template('index.html')

@app.route("/all")
def nobel():
    json_url = os.path.join(app.static_folder,"","nobel.json")
    data_json = json.load(open(json_url))
    #render_template is always looking in templates folder
    return render_template('work.html',data=data_json)


#@app.route("/year?id=<year>")

@app.route("/<year>",methods=['GET','POST'])#allows for get and post options
def nobel_year(year):
    json_url = os.path.join(app.static_folder,"","nobel.json")
    data_json = json.load(open(json_url))
    data = data_json['prizes']
    year = request.view_args['year']
    if request.method == 'GET':
        output_data = [x for x in data if x['year']==year]
        #render template is always looking in tempates folder
        return render_template('work.html',data=output_data)


    elif request.method == 'POST':
        year = request.form["year"]
       	category = request.form["category"]
        id = request.form["id"]
        firstname = request.form["firstname"]
        surname = request.form["surname"]
        motivation = request.form["motivation"]
        share = request.form["share"]
        new= { 'year':year,'category':category,'laureates':[{'id':id,
                                'firstname':firstname,
                                'surname':surname,
                                'motivation':motivation,
                                'share':share}]}
        with open('./static/nobel.json','r+') as nobel_file:
          # get it to dictionary
            nobel_data = json.load(nobel_file)
            # append with new data
            nobel_data['prizes'].append(new)
            nobel_file.seek(0)
            # json
            json.dump(nobel_data, nobel_file)
    
        return redirect(url_for("nobel_year",year=year))
      
      


if __name__ == "__main__":
    app.run(debug=True)

