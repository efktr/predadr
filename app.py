from flask import Flask, jsonify, abort
from src.predadr import Predadr

predictor = Predadr()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def test():
    adrs, _ = predictor.predict("CCCCOC(=O)COC1=C(C=C(C=C1)Cl)Cl.CCCCOC(=O)COC1=CC(=C(C=C1Cl)Cl)Cl")
    return jsonify(adrs)

@app.route('/smiles/<string:smiles>')
def show_post(smiles):
    try:
        adrs, _ = predictor.predict(smiles)
    except:
        abort(500)
    return jsonify(adrs)

if __name__ == '__main__':
    app.run()