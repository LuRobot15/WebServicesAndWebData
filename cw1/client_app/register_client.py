import requests

directory_service = "http://newssites.pythonanywhere.com/api/directory/"

def main():
	service = input("Enter service: ")

	news_agency_name = "Luke Roberts News Agency"
	newsAgencyIdentifyer = "LOR03"

	payload = {
		"agency_name" : news_agency_name,
		"url" : service,
		"agency_code" : newsAgencyIdentifyer
	}

	response = requests.post(directory_service, data=payload)

	if response.status_code == 201:
		print("Service registered")
	else:
		print("Service not registered")
		print("status code: " + str(response.status_code))
		print("reason: " + response.reason)	
	
 
if __name__ == "__main__":
	main()
