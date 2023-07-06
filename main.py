from flask import Flask, render_template
from flask import request
from flask import jsonify
from pymongo import MongoClient
import os
import diff_match_patch as dmp_module
dmp = dmp_module.diff_match_patch()
import traceback

app = Flask(__name__)

host = 'localhost'
port = 27017
database = 'mydatabase'
# Connect to MongoDB
connection_string = f"mongodb://{host}:{port}/{database}"
client = MongoClient(connection_string)
db = client['mydatabase']
collection = db['mycollection']


def diff_prettyHtml(diffs):
    """Convert a diff array into a pretty HTML report.

Args:
  diffs: Array of diff tuples.

Returns:
  HTML representation.
"""
    html = []
    for (op, data) in diffs:
        text = (
            data.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\n", "&para;<br>")
        )
        if op == 1:
            html.append('<ins style="background:#82E0AA;">%s</ins>' % text)
        elif op == -1:
            html.append('<del style="background:#F1948A;">%s</del>' % text)
        elif op == 0:
            html.append("<span>%s</span>" % text)
    return "".join(html)

def generate(username):
    actions = []
    diffs_htmls = []
    project_ids = []
    overall_htmls = []
    data = collection.find({'username': username})
    for j in range(collection.count_documents({'username': username})):
        try:
            index = project_ids.index(data[j]['project'])
            actions[index].append(data[j])
        except ValueError:
            project_ids.append(data[j]['project'])
            actions.append([data[j]])

    for i in range(len(actions)):
        diffs_htmls = []
        for k in range(len(actions[i]) - 1):
            if actions[i][k]['text'] != actions[i][k + 1]['text']:
                diffs = dmp.diff_main(actions[i][k]['text'], actions[i][k + 1]['text'])
                dmp.diff_cleanupSemantic(diffs)
                diffs_htmls.append(diff_prettyHtml(diffs))
        overall_htmls.append(diffs_htmls)

    return project_ids, overall_htmls

class LocalStore:
    def __call__(self, f: callable):
        f.__globals__[self.__class__.__name__] = self
        return f

@app.route('/create', methods=('GET', 'POST'))
@LocalStore()
def create():
    try:
        print(request.method)
        if request.method == 'POST':
            info = request.get_json(force=True)
            print("THIS IS THE REQUEST", info)
            Username = info["Username"]
            project_ids, overall_htmls = generate(Username)
            print(project_ids, overall_htmls)
            return {"status": "ok", "projectIDs": project_ids, "diff_htmls": overall_htmls}
    except:
        print(traceback.print_exc())
    return {"status": "no", "projectIDs": "", "diff_htmls": ""}

@app.route('/')
def index():
    return render_template('index.html')

