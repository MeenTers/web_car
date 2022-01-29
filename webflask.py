
from flask import Flask, request ,  render_template ,url_for,redirect
import json
import pandas as pd
import os
from werkzeug.utils import secure_filename
import subprocess


UPLOAD_FOLDER = 'file'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_files():
#    if request.method == 'POST':
#       f = request.files['file']
#       filename = secure_filename(f.filename)
#       f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#       return 'file uploaded successfully'


# @app.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)

##webapp
@app.route("/index",methods = ['POST','GET'])
def index():
    return render_template("index.html")

@app.route("/home",methods = ['POST','GET'])
def home():
    dbpd = pd.read_csv('webdb.csv')
    if request.method == "POST":
        car_id = request.form.get('car_id')
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        insu = request.form.get('insurance')
        f = request.files['file']
        filename = car_id + '.obj'
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        dbpd = dbpd.append({'car_id':car_id,'fname':first_name
                            ,'lname':last_name,'insurance':insu
                            ,'modelname':filename},ignore_index=True)
        dbpd.to_csv('webdb.csv',index=False)
        return redirect(url_for('show'))

    

@app.route("/show",methods = ['POST','GET'])
def show():
    data = pd.read_csv('webdb.csv')
    data = data.to_numpy()

    return render_template("showdata.html",datas= data)

@app.route("/view",methods = ['POST','GET'])
def view():
    car_id = request.form.get('car_id')
    insu = request.form.get('insurance')
    pro = subprocess.Popen(["python","compare.py","--c",str(car_id)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout,stderr) = pro.communicate()
    text = str(stdout,'utf-8')
    text = text.rstrip("\n")
    if insu == "ประกันภัยชั้น1":
        return render_template("view.html",outs = text)
    if insu == "ประกันภัยชั้น2":
        return render_template("insu2.html",outs = text)
    if insu == "ประกันภัยชั้น3":
        return render_template("insu3.html",outs = text)
    if insu == "ประกันภัยชั้น4":
        return render_template("insu4.html",outs = text)
    if insu == "ประกันภัยชั้น2+" :
        return render_template("insu5.html",outs = text)
    if insu == "ประกันภัยชั้น3+" :
        return render_template("insu6.html",outs = text)

@app.route("/homepage",methods = ['POST','GET'])
def homepage():
    return render_template("home.html")

# @app.route("/output",methods = ['POST','GET'])
# def output():
#     car_id = request.form.get('car_id')
#     pro = subprocess.Popen(["python","compare.py","--c",str(car_id)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     (stdout,stderr) = pro.communicate()
#     text = str(stdout,'utf-8')
#     text = text.rstrip("\n")
#     return render_template("out.html",outs = text)

if __name__ == "__main__":
    app.run(debug = True)# host ='0.0.0.0',port=5001 