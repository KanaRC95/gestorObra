from flask import Flask, render_template, request, url_for, flash, redirect
from pyravendb.store import document_store

# sudo /opt/lampp/lampp start
# sudo /opt/lampp/lampp stop

store = document_store.DocumentStore(urls=["http://localhost:8080"], database="gestorObra")
store.initialize()

app = Flask(__name__, template_folder="templates")
@app.route('/')
def index ():
    data = []
    return render_template('index.html', contacts=data)

if __name__=="__main__":
        app.run(port=3000,debug=True)