from flask import Flask,render_template
import pymongo
from settings import MONGO_URL,MONGO_DATABASE
app=Flask(__name__)

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DATABASE]
jokes=db["QiubaiItem"].find()
client.close()

@app.route("/")
def hello():
    return render_template("qiubai_index.html",p_jokes=jokes)

if __name__ =="__main__":
    app.run()
