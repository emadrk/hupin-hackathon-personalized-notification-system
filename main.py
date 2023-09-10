from flask import Flask, request, jsonify,render_template
import threading


from sqlalchemy.sql import func
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy

from services.sql import sql_reader
from services.notification.notification_sender import sendNotifications


app = Flask(__name__)






# url ='postgresql://nrzlppgvzcreqh:9aa9fcc9bdd35ba405654b9a30d18b71a0424344c5fa08893cbd2aedee6cfe28@ec2-34-235-198-25.compute-1.amazonaws.com:5432/dbnu9bnpvc38nj'

# database="dbnu9bnpvc38nj", user="nrzlppgvzcreqh", password="9aa9fcc9bdd35ba405654b9a30d18b71a0424344c5fa08893cbd2aedee6cfe28", host="ec2-34-235-198-25.compute-1.amazonaws.com", port="5432"
# url=os.environ['DATABASE_URL']
# url=url.replace("postgres","postgresql")
# platform: postgres
# url: jdbc:postgresql://localhost:5499/patients
# username: postgres
# password: Lupin123
url ='postgresql://postgres:Lupin123@localhost:5499/patients'
print(url)
app.config['SQLALCHEMY_DATABASE_URI'] =url

# app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://nrzlppgvzcreqh:9aa9fcc9bdd35ba405654b9a30d18b71a0424344c5fa08893cbd2aedee6cfe28@ec2-34-235-198-25.compute-1.amazonaws.com:5432/dbnu9bnpvc38nj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------- ---------------
@app.route("/getPatientIds", methods=['POST'])
def getPatientIds():
    
    reqBody = request.get_json()

    print(f"reqBody===>{reqBody}")
    sql = reqBody.get("sql","")
    print(f"sql===>{sql}")
    data = sql_reader.getPatientIds(db,sql)
   
    return jsonify(statusCode=200,msgCode="",msgText="",data=data)

@app.route("/sendNotifications", methods=['POST'])
def sendnotifications():
    
    reqBody = request.get_json()

    # print(f"reqBody===>{reqBody}")
    # patientIds = reqBody.get("patientIds","")
    sendNotifications(reqBody,db)
   
    return jsonify(statusCode=200,msgCode="",msgText="",data="")

@app.route("/", methods=['GET'])
def UI():
   
    return render_template('ui.html')


if __name__ == '__main__':
    app.run(port=5000, debug=False,threaded=True)
