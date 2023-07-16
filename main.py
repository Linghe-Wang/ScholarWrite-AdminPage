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
database = 'flask_db'
collection = "activity"
# Connect to MongoDB
connection_string = f"mongodb://{host}:{port}"
# connection_string = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.9.1"
client = MongoClient(connection_string)
db = client[database]
collection = db[collection]


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

def generate(projectID):
    actions = []
    diffs_htmls = []
    users = []
    overall_htmls = []
    data = collection.find({'project': projectID})
    # print(collection.find({'project': projectID}))
    for j in range(collection.count_documents({'project': projectID})):
        try:
            actions.append({"file": data[j]["file"], "text": data[j]['text'], "timestamp": data[j]["timestamp"]})
            users.append(data[j]['username'])
            # actions[index].append(data[j])
        except:
            users.append(data[j]['username'])
            actions.append({"file": data[j]["file"], 'suggestion': data[j]['suggestion'], "timestamp": data[j]["timestamp"]})
    # print(actions[0]['text'])
    diffs_htmls = []
    for i in range(len(actions)-1):
        try:
            if actions[i]['text'] != actions[i+1]['text']:
                diffs = dmp.diff_main(actions[i]['text'], actions[i+1]['text'])
                dmp.diff_cleanupSemantic(diffs)
                diffs_htmls.append(diff_prettyHtml(diffs))
        except:
            diffs_htmls.append("lol")
            print([key for key in actions[i+1]])
    # overall_htmls.append(diffs_htmls)
    
    info = []
    print(len(users))
    print(len(actions))
    print(len(diffs_htmls))
    for i in range(0, len(users)):
        if i == 0:
            info.append({"users": users[i], "actions": actions[i], "htmls": actions[0]['text']})
        if i > 0:
            info.append({"users": users[i], "actions": actions[i], "htmls": diffs_htmls[i-1]})
        
    return info

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
            projectID = info["projectID"]
            
            # project_ids, actions, overall_htmls = generate(projectID)
            info = generate(projectID)
            # print(info)
            # print(project_ids, actions, overall_htmls)
            return {"status": "ok", "info": info}
            # return {"status": "ok", "projectIDs": project_ids, "diff_htmls": overall_htmls}
    except:
        print(traceback.print_exc())
    return {"status": "no", "projectIDs": "", "diff_htmls": ""}

@app.route('/')
def index():
    return render_template('index.html')

