import requests
import tabulate

directory_service = "http://newssites.pythonanywhere.com/api/directory/"

def main():
	service = input("Enter service: ")
	if service == "":
		list_services()
	session = requests.Session()
	login(session, service)
    
	logged_in = True
	while logged_in:
		print("1. Post story")
		print("2. Get stories")
		print("3. Delete story")
		print("4. Logout")
		print("5. Exit")
		print("list: List services")
		choice = input("Enter choice: ")
		
		if choice == "1":
			post_story(session, service)
		elif choice == "2":
			get_stories(session, service)
		elif choice == "3":
			delete_story(session, service)
		elif choice == "4" or choice == "5":
			logout(session, service)
			logged_in = False
		elif choice == "list":
			list_services()
		else:
			print("Invalid choice")

    
def login(session : requests.Session, url : str):
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
		else:
			print("Login failed")
			print("status code: " + str(response.status_code))
			print("reason: " + response.reason)
   
def logout(session : requests.Session, url : str):
	logout_url = url + "/api/logout"
 
	response = session.post(logout_url)
 
	if response.status_code == 200:
		print("Logout successful")
	else:
		print("Logout failed")
		print("status code: " + str(response.status_code))
		print("reason: " + response.reason)
  
def post_story(session : requests.Session, url : str):
	post_story_url = url + "/api/stories"

	headline = input("Headline: ")
	story_cat = input("Story catagory: ")
	stroy_reg = input("Story region: ")
	stroy_details = input("Story details: ")
	payload = {"headline": headline, "category": story_cat, "region": stroy_reg, "details": stroy_details}
 
	response = session.post(post_story_url, data=payload)
 
	if response.status_code == 200:
		print("Story posted successfully")
	else:
		print("Story post failed")
		print("status code: " + str(response.status_code))
		print("reason: " + response.reason)
		print("response: " + response.text) 
  
def get_stories(session : requests.Session, url : str):
	get_stories_url = url + "/api/stories"

	story_cat = input("Story catagory: ")
	stroy_reg = input("Story region: ")
	story_date = input("Story date: ")

	if story_cat == "":
		story_cat = "*"
	if stroy_reg == "":
		stroy_reg = "*"
	if story_date == "":
		story_date = "*"

	payload = {"category": story_cat, "region": stroy_reg, "date": story_date}
	response = session.get(get_stories_url, params=payload)
 
	if response.status_code == 200:
		print(response.json())
	else:
		print("Get stories failed")
		print("status code: " + str(response.status_code))
		print("reason: " + response.reason)
		print("response: " + response.text) 
  
def delete_story(session : requests.Session, url : str):
	delete_story_url = url + "/api/stories/"

	delete_story_url += input("Enter story id to delete: ")
 
	response = session.delete(delete_story_url)
 
	if response.status_code == 200:
		print("Story deleted successfully")
	else:
		print("Story delete failed")
		print("status code: " + str(response.status_code))
		print("reason: " + response.reason)
  
def list_services():
	response = requests.get(directory_service)
    
	if response.status_code != 200:
		print("Failed to get service list")
		print("status code: " + str(response.status_code))
		print("reason: " + response.reason)
		return

	print(response)
	service_list =response.json()
    
	headers = service_list[0].keys()
	rows = [x.values() for x in service_list]
    
	print(tabulate.tabulate(rows, headers, tablefmt="grid"))
    
  

if __name__ == "__main__":
    main()