from flask import Flask, render_template, request
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def load_seqs():
    seqs = request.form['seqs']
    data1 = request.form['a']
    data2 = request.form['b']
    data3 = request.form['c']
    data_arr = np.array([data1, data2, data3])
    pred = np.random.random(1)
    return render_template('results.html', data=data_arr, prediction = pred, seqs=seqs)


@app.route('/guide')
def get_guide():
    return render_template('guide.html')

@app.route('/about')
def get_about():
    return render_template('about.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port)
    # this is used if you run it as flask app to debug
    #app.run(debug=True, host='0.0.0.0')
