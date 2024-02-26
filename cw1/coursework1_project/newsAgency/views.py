from django.shortcuts import render
from models import Author, Article
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.
def login(request):
	username = request.POST.get("username")
	password = request.POST.get("password")
	user = authenticate(request, username=username, password=password)
	if user is not None:
		# A backend authenticated the credentials
		login(request, user)

		http_response = HttpResponse("Login successful", content_type='text/plain', status=200, reason='OK')
		return http_response
	else:
		# No backend authenticated the credentials
		http_response = HttpResponse("Login failed", content_type='text/plain', status=401, reason='Unauthorized')
		return http_response

def logout(request):
	if not request.user.is_authenticated:
		http_response = HttpResponse("Not logged in", content_type='text/plain', status=400, reason='Bad request')
		return http_response
	else:
		logout(request)
		http_response = HttpResponse("Logout successful", content_type='text/plain', status=200, reason='OK')
		return http_response

def stories(request):
	if request.method == 'GET':
		return get_stories(request)
	if request.method == 'POST':
		return post_story(request)

	return render(request, 'stories.html')

def post_story(request):
    #checking if the user is logged in
	if not request.user.is_authenticated:
		http_response = HttpResponse("Not logged in", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response
	#checking if the user is an author
	try:
		author = Author.objects.get(user=request.user)
	except Author.DoesNotExist:
		#creating an author object for the user
		author = Author.objects.create(user=request.user)
	
	#creating the article object
	story_headline = request.POST.get("headline")
	story_catagory = request.POST.get("story_catagory")
	story_region = request.POST.get("story_region")
	story_details = request.POST.get("story_details")

	#validating params given
	if story_headline == None:
		http_response = HttpResponse("You must supply a headline", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response
	if story_catagory == None:
		http_response = HttpResponse("You must supply a story catagory", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response
	if story_region == None:
		http_response = HttpResponse("You must supply a story region", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response
	if story_details == None:
		http_response = HttpResponse("You must supply story details", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response

	#validating the story catagory
	if story_catagory not in ['pol', 'art', 'tech', 'trivia']:
		http_response = HttpResponse("Invalid story catagory", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response

	#validating the story region
	if story_region not in ['uk', 'eu', 'w']:
		http_response = HttpResponse("Invalid story region", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response

	#validating the story details
	if len(story_details) > 128:
		http_response = HttpResponse("Story details too long", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response

	#validating the story headline
	if len(story_headline) > 64:
		http_response = HttpResponse("Story headline too long", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response

	#creating the article object
	Article.objects.create(
		headline=story_headline,
		story_catagory=story_catagory,
		region=story_region,
		author=author,
		story_details=story_details
	)

	return HttpResponse(status=201, reason='Created')

def get_stories(request):
	story_catagory = request.GET.get("story_cat")
	story_region = request.GET.get("story_region")
	story_date = request.GET.get("story_date")
 
	stories = Article.objects.all()

	if story_catagory != "*" and story_catagory != None:
		stories = stories.filter(story_catagory=story_catagory)
	if story_region != "*" and story_region != None:
		stories = stories.filter(region=story_region)
	if story_date != "" and story_date != None:
		stories = stories.filter(created_at__gte=story_date)
  
	story_collection = []
	for story in stories:
		author = story.author
		author_name = author.user.first_name + " " + author.user.last_name
		item = {
			"key" : story.id,
			"headline" : story.headline,
			"story_cat" : story.story_catagory,
			"story_region" : story.region,
   			"author" : author_name,
			"story_date" : story.created_at,
			"story_details" : story.story_details
		}
		story_collection.append(item)
  
	if (len(story_collection) == 0):
		http_response = HttpResponse("No stories found matching the given criteria", content_type='text/plain')
		http_response.status_code = 404
		http_response.reason_phrase = 'Not Found'
		return http_response


	payload = {"stories" : story_collection}
 
	#creating the response
	http_response = HttpResponse(json.dumps(payload), content_type='application/json')
	http_response.status_code = 200
	http_response.reason_phrase = 'OK'
	return http_response

def delete_story(request, key : int):
	if not request.user.is_authenticated:
		http_response = HttpResponse("Not logged in", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response

	try:
		story = Article.objects.get(id=key)
	except Article.DoesNotExist:
		http_response = HttpResponse("Story not found", content_type='text/plain')
		http_response.status_code = 503
		http_response.reason_phrase = 'Service Unavailable'
		return http_response

	story.delete()

	return HttpResponse(status=200, reason='OK')


