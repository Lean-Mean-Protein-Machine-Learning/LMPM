import os, sys

from flask import Flask, render_template, request
import numpy as np

# to convert plot
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


# append this path so that the lmpm module is found
# another option would be installing it with pip
sys.path.append('/')
import lmpm
import lmpm.unirep as unirep


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def load_seqs():
    seqs = request.form['seqs']
    specie = request.form['species']
    localization = request.form['location']
    add_feats = request.form.get('add_feat') != None

    try:
        prediction = lmpm.predict_location(seqs, specie, localization, add_feats, pred_all = True)
    except Exception as e:
        return render_template("input_error.html", error=e)

    return render_template('results.html', seqs=seqs, pred=prediction, prev_species=specie, prev_loc=localization, prev_add_feats=add_feats, tables=[prediction.all_predictions.to_html(classes='data', header="true")])


@app.route('/improve', methods=['POST'])
def mutate():
    seqs = request.form['seqs']
    specie = request.form['species']
    localization = request.form['location']
    add_feats = request.form.get('add_feat') != None #if it is checeked is not empty so get True
    positions = request.form['positions']
    
    try:
        mutated_scores, initial_score = lmpm.optimize_sequence(seqs, specie, localization, include_dg=add_feats, positions=positions)
        plot_f = lmpm.improve_sec.plot_optimization(mutated_scores, initial_score, plot_inplace=False, dpi=300)
        mut_table = lmpm.top_mutations(mutated_scores, initial_score,15)
        # help of https://gitlab.com/snippets/1924163 and https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
        pngImage = io.BytesIO()
        FigureCanvas(plot_f).print_png(pngImage)
        # Encode PNG image to base64 string
        b64plot = str("data:image/png;base64,")+str(base64.b64encode(pngImage.getvalue()).decode('utf8'))
    except Exception as e:
        return render_template("input_error.html", error=e)

    return render_template('improve.html', seqs=seqs, specie=specie, loc=localization, add_feats=add_feats, plot=b64plot, tables=[mut_table.to_html(classes='data', header="true")])


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
    # use this when running in the website (heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port)
    # this is used if you run it as flask app to debug (Specifying port explicity is important in this case)
    # app.run(debug=True,host='0.0.0.0',port=5000)
    # app.run(debug=True)
