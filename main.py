from flask import Flask, render_template
from flask import request
from flask import jsonify
from pymongo import MongoClient
import os
import bcrypt
from datetime import datetime, timedelta
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
user_data = db["user_data"]

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

def verify_password(password, stored_salt, stored_hash):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), stored_salt)
    return hashed_password == stored_hash

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

@app.route('/login', methods=('GET', 'POST', 'OPTIONS'))
def post():
    try:
        global code
        info = request.get_json(force=True)
        try:
            result = user_data.find_one({"username": info['username']})
            print(result)
            if result == None:
                code = 100
            else:
                if verify_password(info['password'], result['salt'], result['hashed_password']):
                    code = 300
                else:
                    code = 100
        except:
            print(traceback.print_exc())
            code = 400
        data = {
            "status": code
        }
        response = jsonify(data)
        print(data)

        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    except:
        print(traceback.print_exc())

def options():
    response = jsonify({'message': 'OK'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/list', methods=('GET', 'POST', 'OPTIONS'))
def post():
    try:
        project_ids = []
        all_projects_times = []
        time_list = []
        data = []

        # Get all projects and their corresponding timestamps
        distinct_Projects = collection.distinct("project")
        for id in distinct_Projects:
            timestamps = []
            project_ids.append(id)
            selected_documents = collection.find({"project": id})
            for doc in selected_documents:
                timestamps.append(doc["timestamp"]//1000)
            all_projects_times.append(timestamps)

        # Convert all timestamps to date objects for each project
        for i in range(len(all_projects_times)):
            for project_time in all_projects_times[i]:
                time_list.append(datetime.fromtimestamp(project_time))

            # Find the earliest and latest dates
            min_date = min(time_list).date()
            max_date = max(time_list).date()

            # Generate date strings and initialize counts
            date_strings = [(min_date + timedelta(days=i)).strftime('%b %d') for i in
                            range((max_date - min_date).days + 1)]
            counts = [0] * len(date_strings)

            # Count the occurrences of each date
            for dt in time_list:
                index = (dt.date() - min_date).days
                counts[index] += 1

            data.append({"project": project_ids[i], "date_strings": date_strings, "counts": counts})

        response = {
            "data": data
        }
        response = jsonify(response)
        print(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    except:
        print(traceback.print_exc())

@app.route('/')
def index():
    return render_template('index.html')

