from os import abort
from flask import Flask, request, send_from_directory
from requests import exceptions
from html_parser import Parser
from save_file import save_file
app = Flask(__name__)

DOWNLOAD_DIRECTORY = "data"

@app.route('/')
def index():
    if request.method == "GET":
        url = request.args.get("url")
        width = request.args.get("width",0)
        images = request.args.get("images",False)
        use_cached = request.args.get("cached",False)
        short_uri = url.split("/")[-1]
        if not isinstance(width,int):
            try:
                width = int(width)
            except ValueError:
                width = 0
        if use_cached:
            try:
                return send_from_directory(DOWNLOAD_DIRECTORY, f"{short_uri}.txt", as_attachment=True)
            except FileNotFoundError:
                abort(404)
        else:
            parser = Parser(url, width, images)
            data = parser.parse()
            save_file(data, url)
            return send_from_directory(DOWNLOAD_DIRECTORY, f"{short_uri}.txt", as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)