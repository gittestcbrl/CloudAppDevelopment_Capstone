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
        
        my_database = client[databaseName]
        reviewdata = dict['review']

        # Create a document using the Database API
        my_document = my_database.create_document(data)
        print(my_document)
        # Check that the document exists in the database
        if my_document.exists():
            print('SUCCESS!!')
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

