from CDNHTMLHelper import CDNHTMLHelper
from flask import Flask


app = Flask(__name__)


cdn_html_helper = CDNHTMLHelper(app, local=True)

cdn_html_helper.use("jquery", "3.6.0", {"js": "/dist/jquery.js"})

print(cdn_html_helper.get())

if __name__ == '__main__':
    app.run(debug=True)
