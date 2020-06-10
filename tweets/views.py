import random
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

# Create your views here.
from .forms import TweetForm
from .models import Tweet

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # form related logic
        obj.save()
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form/form.html', context={"form": form})

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