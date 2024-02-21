from flask import Flask, request
from autocompleter import Autocomplete


app = Flask(__name__)
ac = Autocomplete('data/data.csv', 'data/attributes.csv')


@app.route('/')
def index():
    return f'Welcome to the prefix autocomplete web service. \
            To try it just use /api?query= <br> For example <a href=/api?query=sin>/api?query=sin</a>'


@app.route('/api')
def api():
    query = request.args.get('query')

    if not query:
        return 'Query is empty. To specify it use /api?query='

    return ac.get_suggestions(query)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
