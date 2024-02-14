from flask import Flask

app = Flask(__name__)
app.testing = True
@app.route('/')

def home_page():
	return 'Welcome to Wiki Search homepage'

import controllers.wiki_search_controller as wiki_search_controller
# main driver function
if __name__ == '__main__':
      app.run(debug=True, port=5000)


