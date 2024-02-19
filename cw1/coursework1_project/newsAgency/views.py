from django.shortcuts import render
from models import Author, Article

# Create your views here.
def login(request):
	return render(request, 'login.html')

def logout(request):
	return render(request, 'logout.html')

def stories(request):
	if request.method == 'GET':
		return get_stories(request)
	if request.method == 'POST':
		return post_story(request)

	return render(request, 'stories.html')

def post_story(request):
	return render(request, 'post_story.html')

def get_stories(request):
	return render(request, 'get_stories.html')

def delete_story(request, key : int):
	return render(request, 'delete_story.html')


