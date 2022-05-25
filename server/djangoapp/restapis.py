import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import json
# from ibm_watson import NaturalLanguageUnderstandingV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm_watson.natural_language_understanding_v1 \
#     import Features, SentimentOptions
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, api_key=None, **kwargs):
    print("GET from {} ".format(url), "apikey=", api_key, "kwargs=", kwargs)
    try:
        if api_key:            
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
            
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    # print('response', response.json)
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # print(kwargs['dealerId'])
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=str(kwargs['dealerId']))
    # print("json_result-", json_result)
    if json_result:
        # Get the row list in JSON as dealers
        if "reviews" in json_result:
            reviews = json_result["reviews"]
            # For each dealer object
            for review in reviews:
                # Get its content in `doc` object
                # print("review obj-", review)
                # Create a DealerReview object with values in `review` object
                if 'sentiment' in review:
                    sentiment = review["sentiment"]
                else:
                    sentiment = analyze_review_sentiments(review["review"])
                if review["purchase"]:
                    review_obj = DealerReview(car_make=review["car_make"], car_model=review["car_model"], 
                                            car_year=review["car_year"],
                                        id=review["id"], dealership=review["dealership"], 
                                        purchase_date=review["purchase_date"],
                                        name=review["name"],
                                        purchase=review["purchase"], review=review["review"], sentiment=sentiment)
                else:
                    review_obj = DealerReview(car_make='', car_model='', 
                                            car_year='',
                                        id=review["id"], dealership=review["dealership"], 
                                        purchase_date='',
                                        name=review["name"],
                                        purchase=review["purchase"], review=review["review"], sentiment=sentiment)              
                results.append(review_obj)
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/41f7b2da-a2cc-4030-8598-690aeaba4476/v1/analyze'
    api_key = '0e645WXGWWxO5DaR7Ly6XSjF-SnlVAr_Nr9CpdM8HwFa'
    version = "2022-04-07" 
    feature = {
                "sentiment": {}
            }
 
    return_analyzed_text = True 
    result_json = get_request(url, api_key=api_key, text=text,  version=version, 
        features=feature, return_analyzed_text=return_analyzed_text)
    # print(result_json)
    # print ("review sentiment-", result_json["sentiment"]["document"]["label"])
    if 'sentiment' in result_json:
        return result_json["sentiment"]["document"]["label"]
    else:
        return ''
