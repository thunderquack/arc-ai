from flask import Flask
from flask_cors import CORS
import ptvsd

app = Flask(__name__)
ptvsd.enable_attach(address=('0.0.0.0', 5679))
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010)
