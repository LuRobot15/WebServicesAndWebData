import requests
import tabulate
import random
from datetime import datetime

directory_service = "http://newssites.pythonanywhere.com/api/directory/"

def main():
	session = requests.Session()
	service_logged_into = None
    
	while True:
		command = input("Please input a command: \n")
		input_command = command.split(" ")
    
		if input_command[0] == "login":
			service_logged_into = login(input_command[1], session)
		elif input_command[0] == "logout":
			if logout(service_logged_into, session):
				service_logged_into = None
		elif input_command[0] == "post":
			post_story(service_logged_into, session)
		elif input_command[0] == "news":
			get_stories(input_command)
		elif input_command[0] == "delete":
			delete_story(service_logged_into, input_command[1], session)
		elif input_command[0] == "list":
			list_services()
		else:
			print("Invalid command")


def login(url : str, session : requests.Session):
	success = False
	
	login_url = url + "/api/login"
	
	while not success:
		username = input("Enter username: ")
		password = input("Enter password: ")
	
		payload = {"username": username, "password": password}
	
		response = session.post(login_url, data=payload)

		if response.status_code == 200:
			success = True
			print("Login successful")
		elif response.status_code == 404:
			print("Service not found")
			break
		else:
			print("Login failed")
			print("status code: " + str(response.status_code))
			print("reason: " + response.reason)
			if response.content_type == "text/plain":
				print("response: " + response.text)

	if success:
		return url
	else:
		return None


def logout(url : str, session : requests.Session):
	if url == None:
		print("Please login to a service first")
		return

	logout_url = url + "/api/logout"
    
	response = session.post(logout_url)
    
	if response.status_code == 200:
		print("Logout successful")
		return True
	else:
		print("Logout failed")
		print("status code: " + str(response.status_code))
		print("reason: " + response.reason)
		if response.content_type == "text/plain":
			print("response: " + response.text)
		return False


def post_story(url : str, session : requests.Session):
	if url == None:
		print("Please login to a service first")
		return
    
	post_story_url = url + "/api/stories"

	headline = input("Headline: ")
	story_cat = input("Story catagory: ")
	stroy_reg = input("Story region: ")
	stroy_details = input("Story details: ")
	payload = {"headline": headline, "category": story_cat, "region": stroy_reg, "details": stroy_details}
 
	response = session.post(post_story_url, data=payload)
 
	if response.status_code == 201:
		print("Story posted successfully")
	else:
		print("Story post failed")
		print("status code: " + str(response.status_code))
		print("reason: " + response.reason)
		if response.content_type == "text/plain":
			print("response: " + response.text)


def delete_story(url : str, key : int, session : requests.Session):
	if url == None:
		print("Please login to a service first")
		return
	
	delete_story_url = url + "/api/stories/" + str(key)
 
	response = session.delete(delete_story_url)
 
	if response.status_code == 200:
		print("Story deleted successfully")
	else:
		print("Story delete failed")
		print("status code: " + str(response.status_code))
		print("reason: " + response.reason)
		if response.content_type == "text/plain":
			print("response: " + response.text)


def get_stories(input_command : list):
	params = {}
	params["service_id"] = ""
	params["story_cat"] = "*"
	params["story_region"] = "*"
	params["story_date"] = "*"

    
	for option in input_command:
		if option == "news":
			continue
		
		elif option.startswith("-id="):
			params["service_id"] = option[4:]
		elif option.startswith("-cat="):
			params["story_cat"] = option[5:]
		elif option.startswith("-reg="):
			params["story_region"] = option[5:]
		elif option.startswith("-date="):
			date = datetime.strptime(option[6:], "%d/%m/%Y")
			params["story_date"] = date.strftime("%d/%m/%Y")
 
	services = get_services()
	services_to_query = get_desired_services(services, params["service_id"])
	if services_to_query == None:
		return

	api_params = {"story_cat": params["story_cat"], "story_region": params["story_region"], "story_date": params["story_date"]}

	stories = []
	for service in services_to_query:
		try:
			response = requests.get(service["url"] + "/api/stories", params=api_params)
			if response.status_code == 200:
				stories += response.json().get("stories")
			else:
				print("Get stories failed on ", service["url"] + "/api/stories")
				print("status code: " + str(response.status_code))
				print("reason: " + response.reason)
				if response.content_type == "text/plain":
					print("response: " + response.text)
		except Exception as e:
			print("Get stories failed on ", service["url"] + "/api/stories")
			print("reason: " + str(e))
			continue

	print_stories(stories)
 

def get_desired_services(services : list, service_id : str) -> list:
	services_to_query = []
 
	if service_id != "":
		for service in services:
			if service["agency_code"] == service_id:
				services_to_query.append(service)
				break
	else:
		random.shuffle(services)
		for i in range(20):
			services_to_query.append(services[i])

	if len(services_to_query) == 0:
		print("No services found")
		return None
	return services_to_query


def print_stories(stories : list):
	if len(stories) == 0:
		print("No stories found matching the given criteria")
		return

	headers = stories[0].keys()
	rows = [x.values() for x in stories]
	
	print(tabulate.tabulate(rows, headers, tablefmt="grid"))


def list_services():
	services = get_services()
	print_services(services)
 

def get_services():
	response = requests.get(directory_service)
	
	if response.status_code != 200:
		print("Failed to get service list")
		print("status code: " + str(response.status_code))
		print("reason: " + response.reason)
		if response.content_type == "text/plain":
			print("response: " + response.text)
		return

	return response.json()


def print_services(service_list : list):
	headers = service_list[0].keys()
	rows = [x.values() for x in service_list]
    
	print(tabulate.tabulate(rows, headers, tablefmt="grid"))
 
if __name__ == "__main__":
	main()