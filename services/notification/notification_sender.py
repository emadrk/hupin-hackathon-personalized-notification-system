import sqlalchemy
import requests
import threading
import json


def sendNotifications(reqBody,db):
    patients = str(reqBody.get("patientIds"))
    patients = patients.replace("[","")
    patients =patients.replace("]","")

    query = f'select device_token,patient_id from trusteddevice where patient_id in ({patients});'
    print(f"query:{query}")

    # for patientId in patients:
    result = db.session.execute(sqlalchemy.text(query))

    result=result.all()
    device_tokens = {}

    if(len(result)>0):
        
        for data in result:
            device_tokens[data[0]] = data[1]
        # print(f"device token:{device_tokens}")
        triggerApi(device_tokens,reqBody)   

    
def _execTHREAD(_F):
    def _execProc(*_ARGV, **_KW):
        threading.Thread(target=_F, args=_ARGV, kwargs=_KW).start()
    return _execProc

    

@_execTHREAD
def triggerApi(device_tokens,reqBody):
    if device_tokens:
        for token in device_tokens.keys():
            # private String title;
            # private String message;
            # private String topic;
            # private String token;
            # private HashMap data;
            data = {
                "message":reqBody.get("message"),
                "title":reqBody.get("title"),
                "token":token
            }
            # print(f"calling api with data:{data}")
            response = requests.post("https://dev-py-api-mgmt.azure-api.net/notifications/push/token",data=json.dumps(data),headers = {"Content-Type": "application/json; charset=utf8","Ocp-Apim-Subscription-Key":"c0095fe383f44b988100ecf62a5ccd9e"})
            if response.status_code == 200:
                # Print the response content (usually JSON or HTML)
                print(response.json())
            else:
                # Print an error message if the request was not successful
                print(f"Request failed with status code {response.status_code} :{response.json()}")
            


    



