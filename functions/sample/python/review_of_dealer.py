from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(dict):
    databaseName = "reviews"

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        dealerid = dict['dealerId']
        my_database = client[databaseName]
        #  Retrieve documents where the name field is 'foo'
        selector = {'dealership': {'$eq': dealerid}}
        exp_fields = ['id', "name", "dealership", "review","purchase","purchase_date","car_make","car_model","car_year" ]
        docs = my_database.get_query_result(selector, fields=exp_fields)
        docList = []
        for doc in docs:
            docList.append(doc)
        if docList:
            print(docList)
            return docList
        else:
            print("dealerId does not exist")
            return {"error": "dealerId does not exist"}
        # print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}