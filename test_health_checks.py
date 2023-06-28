import requests
import yaml
import time

def check_health(endpoints):
    availability = {}  # Dictionary to store availability data for each endpoint

    while True:
        for endpoint in endpoints:
            url = endpoint['url']
            name = endpoint.get('name', url)
            headers = endpoint.get('headers', {})
            body = endpoint.get('body')

            availability.setdefault(name, {
                'tests': 0,
                'success': 0
            })

            try:
                start_time = time.time()  # Start time of the HTTP request
                response = requests.request("GET", url, headers=headers, data=body)
                end_time = time.time()  # End time of the HTTP request

                # Check if the response code is within the 2xx range and response latency is less than 500 milliseconds
                if response.status_code >= 200 and response.status_code < 300 and end_time - start_time < 0.5:
                    availability[name]['success'] += 1  # Increment success count if conditions are met

            except requests.exceptions.RequestException:
                pass  # Ignore any exceptions (e.g., connection errors)

            availability[name]['tests'] += 1  # Increment total test count for the endpoint

            # Calculate availability percentage for the endpoint
            availability_percentage = (availability[name]['success'] / availability[name]['tests']) * 100

            # Print the availability percentage for the endpoint
            print(f"{name} has {availability_percentage}% availability percentage")

        print("---------------------------")
        time.sleep(15)  # Wait for 15 seconds before testing the endpoints again

if __name__ == "__main__":
    file_path = input("Enter the file path: ")
    with open(file_path, 'r') as file:
        endpoints = yaml.safe_load(file)

    check_health(endpoints)
