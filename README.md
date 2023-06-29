Endpoint 1: Get the report of the number of times each store went inactive during its business hours
HTTP Method: GET
URL: /report
Response: Returns a JSON object containing the number of times each store went offline during its business hours. The store IDs are used as keys, and the corresponding values represent the count of inactive instances.



Endpoint 2: Get the store status for a specific store and timestamp
HTTP Method: GET
URL: /status
Query Parameters:
store_id: The ID of the store for which you want to retrieve the status.
timestamp_utc: The timestamp (in UTC) for which you want to retrieve the status.
Response: Returns a JSON object containing the store ID, timestamp, and status (active or inactive) for the specified store and timestamp. If no status is found for the given store ID and timestamp, an error message is returned.


The code also includes helper functions to read the data from CSV files and perform the necessary calculations. The read_store_status function reads the store status data from the CSV file and returns it as a list. The read_business_hours function reads the business hours data from the CSV file and returns it as a dictionary. The read_timezone_data function reads the timezone data from the CSV file and returns it as a dictionary.
The calculate_inactive_count function calculates the number of times a store was inactive during its business hours. It takes the store ID, store status data, business hours data, and timezone data as input and returns the count of inactive instances.
The code uses these helper functions and the Flask framework to create the endpoints and handle the API requests.

