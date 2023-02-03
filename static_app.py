from flask import Flask, redirect

def create_app():
	app = Flask(__name__, static_folder='dist', static_url_path="/")

	@app.route('/')
	def index():
		return redirect('/index.html')
	return app

if __name__ == '__main__':
	app = create_app()
	app.run(debug=True, port='5173')