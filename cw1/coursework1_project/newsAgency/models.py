from django.db import models

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

class Article(models.Model):
	headline = models.CharField(max_length=64)
 
	POLITICS = 'pol'
	ART = 'art'
	TECH = 'tech'
	TRIVIA = 'trivia'
	story_catagory_choices = [
		(POLITICS, 'Politics'),
		(ART, 'Art'),
		(TECH, 'Tech'),
		(TRIVIA, 'Trivia'),
	]
	story_catagory = models.CharField(max_length=6, choices=story_catagory_choices, default=TRIVIA)
 
	UK = 'uk'
	EU = 'eu'
	WORLD = 'w'
	region_choices = [
		(UK, 'UK'),
		(EU, 'EU'),
		(WORLD, 'World'),
	]
	region = models.CharField(max_length=2, choices=region_choices, default=UK)

	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	story_details = models.TextField(max_length=128)
