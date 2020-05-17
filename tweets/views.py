import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.

from .models import Tweet


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def tweet_list_view(request, *args, **kwargs):
    query = Tweet.objects.all()
    tweets_list = [{"id": tweet.id, "content": tweet.content, "likes": random.randint(0,12)} for tweet in query]
    data = {
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API
    """
    
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.object.get(id=tweet_id)
        data['content'] =obj.content
    except:
        data['message'] = "Not found"
        status = 400


    
    return JsonResponse(data, status=status)