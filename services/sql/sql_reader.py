import sqlalchemy
import json


def getPatientIds(db,queryText):
    if queryText[:6].lower() in ("select"):


        result = db.session.execute(sqlalchemy.text(f'{queryText}'))

        result=result.all()
        print(result)
        data = [x[0] for x in result]


        

        return str(data).replace("[","").replace("]","")

    return "Bad Sql Query Detected"
