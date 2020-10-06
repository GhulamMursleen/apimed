import flask
from werkzeug.utils import secure_filename
from flask import  abort,request,send_file,jsonify, make_response
from ModelCode import Model
model=Model()

from flask_cors import CORS, cross_origin
app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
@app.route('/append', methods = ['GET', 'POST'])
def append_file():
    
   print("coming",request)
   if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
   elif request.method == 'POST':
      print("coming")
      f = request.files['fisier']
      f.save("Data/append.csv")
      response=model.append()
      return _corsify_actual_response(jsonify(response))
   else:
      return "error"
@app.route('/replace', methods = ['GET', 'POST'])
def replace_file():
    
   #print("coming",request)
   if request.method == "OPTIONS": # CORS preflight
        print("optionho")
        return _build_cors_prelight_response()
   elif request.method == 'POST':
      f = request.files['fisier']
      f.save("Data/append.csv")
      response=model.replace()
      return _corsify_actual_response(jsonify(response))
   else:
      return "error"

@app.route('/inputfile', methods = ['GET', 'POST'])
def downloadFile():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    elif request.method == 'POST':
        path = "Data/input.csv"
        return send_file(path)
    else:
        return _corsify_actual_response(jsonify("Post not good"))
@app.route('/train', methods = ['GET', 'POST'])
def train():
    print("Train")
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    elif request.method == 'POST':
        response=model.train()
        return _corsify_actual_response(jsonify(response))
    else:
        return _corsify_actual_response(jsonify("Post not good"))
@app.route('/predict', methods = ['GET', 'POST'])
def predict():

    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    elif request.method == 'POST':
        lst=[]
        lst.append(request.form['a'])
        lst.append(request.form['b'])
        lst.append(request.form['c'])
        lst.append(request.form['d'])
        lst.append(request.form['e'])
        lst.append(request.form['f'])
        lst.append(request.form['g'])
        lst.append(request.form['h'])
        lst.append(request.form['i'])
        lst.append(request.form['j'])
        lst.append(request.form['k'])
        lst.append(request.form['l'])
        lst.append(request.form['m'])
        print(lst)
        if len(lst)==13:
            res=model.predict(lst)
            return _corsify_actual_response(jsonify(str(res)))
        else:
            return _corsify_actual_response(jsonify("Error in input parameters"))

@app.route('/formData', methods = ['GET', 'POST'])
def forms():
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    elif request.method == 'POST':
        
        path = "Data/inputforms.csv"
        return send_file(path)
    else:
            return _corsify_actual_response(jsonify("POST NOT GOOD"))

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)