import os, sys

from flask import Flask, render_template, request
import numpy as np

# to convert plot
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


# append this path so that the lmpm module is found
# another option would be installing it with pip, but for debugging this is faster
sys.path.append('/')
import lmpm
import lmpm.unirep as unirep

##Alternative
## import lmpm.submodule_ex as submod

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
    try:
        prediction = lmpm.localization_score(seqs,'ecoli')
    except Exception as e:
        return render_template("input_error.html", error=e)

    return render_template('results.html', data=data_arr, prediction = pred, seqs=seqs, uni_reps=unirep.get_UniReps(seqs), first_char=prediction)


@app.route('/improve', methods=['POST'])
def mutate():
    allf = request.form
    seqs = request.form['seqs']
    specie = request.form['species']
    localization = request.form['location']
    add_feats = request.form.get('add_feat') != None #if it is checeked is not empty so get True
    # positions = request.form['positions']
    positions = ['1','2']
    mutated_scores, initial_score = lmpm.optimize_sequence(seqs, specie, localization, include_dg=add_feats, positions=positions)
    # example: AYAYAYAYAYAYYAYAAYAYAYA h sapiens cytoplasm
    plot_f = lmpm.improve_sec.plot_optimization(mutated_scores, initial_score, dpi=300)

    # help of https://gitlab.com/snippets/1924163 and https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
    pngImage = io.BytesIO()
    FigureCanvas(plot_f).print_png(pngImage)

    # Encode PNG image to base64 string
    b64plot = str("data:image/png;base64,")+str(base64.b64encode(pngImage.getvalue()).decode('utf8'))

    return render_template('improve.html', seqs=seqs, specie=specie, loc=localization, add_feats=add_feats, forms=allf, plot=b64plot)


@app.route('/guide')
def get_guide():
    return render_template('guide.html')

@app.route('/about')
def get_about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == "__main__":
    # use this when running in the website
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port = port)
    # this is used if you run it as flask app to debug (Specifying port explicity lis important in this case)
    app.run(debug=True,host='0.0.0.0',port=5000)
    app.run(debug=True)