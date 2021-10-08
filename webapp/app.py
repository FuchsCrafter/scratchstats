from flask import Flask, render_template
import requests
import json

class projects:
    def __init__(self, id):
        self.id = id
    def getStats(self, stat):
        if stat == "loves" or stat == "faves" or stat == "views" or stat == "remixes":
            if stat == "loves":
                r = requests.get(
                    "https://api.scratch.mit.edu/projects/"+str(self.id))
                data = r.json()
                return data['stats']['loves']
            else:
                if stat == "faves":
                    r = requests.get(
                        "https://api.scratch.mit.edu/projects/"+str(self.id))
                    data = r.json()
                    return data['stats']['favorites']
                else:
                    if stat == "remixes":
                        r = requests.get(
                            "https://api.scratch.mit.edu/projects/"+str(self.id))
                        data = r.json()
                        return data['stats']['remixes']
                    else:
                        if stat == "views":
                            r = requests.get(
                                "https://api.scratch.mit.edu/projects/"+str(self.id))
                            data = r.json()
                            return data['stats']['views']
    
    def getComments(self):
        uname = requests.get(
            "https://api.scratch.mit.edu/projects/"+str(self.id)).json()
        if uname != {"code": "NotFound", "message": ""}:
            uname = uname['author']['username']
            data = requests.get("https://api.scratch.mit.edu/users/" +
                                str(uname)+"/projects/"+str(self.id)+"/comments").json()
            comments = []
            if data != {"code": "ResourceNotFound", "message": "/users/"+str(uname)+"/projects/175/comments does not exist"} and data != {"code": "NotFound", "message": ""}:
                x = ""
                for i in data:
                    if "content" in i:
                        x = i['content']
                    else:
                        if "image" in i:
                            x = i['image']
                        else:
                            x = "None"
                    comments.append(str('Username: '+str(uname))+(str(', Content: ')+str(x)))
                return data
    def getInfo(self):
        r = requests.get(
            'https://api.scratch.mit.edu/projects/'+str(self.id)
        ).json()
        return r
    def fetchAssets(self, type='img'):
        '''
        You may have problems with fetching assets since some projects may not have any assets, or are fetched as binary code and not JSON
        '''
        r = json.loads(requests.get(
            'https://projects.scratch.mit.edu/'+str(self.id)
        ).text.encode('utf-8'))
        
        assets = []
        for i in range(len(r['targets'])):
            if type == 'img':
                assets.append('https://cdn.assets.scratch.mit.edu/internalapi/asset/'+str(r['targets'][i]['costumes'][0]['md5ext'])+'/get')
            elif type == 'snd':
                assets.append('https://cdn.assets.scratch.mit.edu/internalapi/asset/'+str(r['targets'][i]['sounds'][0]['md5ext'])+'/get')
        return assets


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/kuchen')
def cakes():
    return 'Kuchen? Kuchen. Kuchen! KUCHEN!'

@app.route('/user/<username>')
def user(username):
    return render_template('user.html', username=username)

@app.route('/project/<projectid>')
def project(projectid):
    try: 
        fetchedProject = projects(projectid)
        views = fetchedProject.getStats("views")
        loves = fetchedProject.getStats("loves")
        faves = fetchedProject.getStats("faves")
        remixes = fetchedProject.getStats("remixes")
        return render_template("project.html", projectid=projectid, views=views, loves=loves, faves=faves, remixes=remixes)
    except:
        return render_template("error_project.html", projectid=projectid)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)