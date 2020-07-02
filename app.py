import flask
import pickle


app = flask.Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
	if flask.request.method == 'GET':
		return 'mems-speech-recognition'
        
	if flask.request.method == 'POST':
		with open('model.pkl', 'rb') as fh:
			loaded_model = pickle.load(fh)
       



if __name__ == '__main__':
    app.run()