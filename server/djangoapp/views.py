from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from .models import CarModel
from django.forms.models import model_to_dict
import random
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html")


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html")


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    # return render(request, 'djangoapp/registration.html')
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context=context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context=context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    if request.method == "GET":
        url = "https://29a9b6d6.eu-gb.apigw.appdomain.cloud/view-dealerships/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = {}
        context['dealership_list'] = dealerships
        # print(context)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context=context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://29a9b6d6.eu-gb.apigw.appdomain.cloud/getallreviews/api/review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        # print(reviews)
        context ={}
        context["dealer_id"] = dealer_id
        context['reviews'] = reviews
        # Return a list of reviews
        return render(request, 'djangoapp/dealer_details.html', context=context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if not request.user.is_authenticated:
        return HttpResponse("Only logged in users can post a review")
    context = {}
    context["dealer_id"] = dealer_id
    cars = CarModel.objects.filter(dealerId=dealer_id)
    context['cars'] = cars
    if request.method == 'GET':
        return render(request, "djangoapp/add_review.html", context=context)
     
    review = {}
    review["id"] = random.randint(6,1000)
    review["time"] = datetime.utcnow().isoformat()
    review["dealership"] = dealer_id
    review["review"] = request.POST['content']
    review["purchase"] = True if request.POST['purchasecheck'] == 'on' else False
    review["name"] = f'{request.user.first_name} {request.user.last_name}'
    carid = request.POST['car']
    # if review['purchase']:
    #     if carid == '':
    #         context['message'] = "Select the car purchased"
    #         print("car error")
    #         return render(request, 'djangoapp/add_review.html', context=context)
    #     elif request.POST['purchasedate'] == '':
    #         context['message'] = "Select the car purchased"
    #         print("date errir")
    #         return render(request, 'djangoapp/add_review.html', context=context)
    #     else:
    car = CarModel.objects.get(pk=carid)
    review['car_make'] = car.make.name
    review['car_model'] = car.name
    review['car_year'] = car.year.year
    review["purchase_date"] = request.POST['purchasedate']

    json_payload ={}
    json_payload["reviews"] = review
    response = post_request("https://29a9b6d6.eu-gb.apigw.appdomain.cloud/post-review/api/review", json_payload, dealerId=dealer_id)
    print("post request send")
    if 'status' in response:
        print(response["status"])
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        print(response["message"])
        return HttpResponse(response["message"])
    
