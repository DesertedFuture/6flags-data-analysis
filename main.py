#!/usr/bin/env python3

from database_helper import DatabaseHelper
from ride_api_call import APIClient
from DataAnalyzer import DataAnalyzer

class Main:
    def create_url(self, url_pre, land_id, url_suff):
        return f"{url_pre}/{land_id}/{url_suff}"

    def __init__(self):
        url_pre = "https://queue-times.com/parks"
        land_id = "32"
        url_suff = "queue_times.json"
        self.url = self.create_url(url_pre, land_id, url_suff)
        self.db_helper = DatabaseHelper("amusement_park.db")
        self.api_client = APIClient(self.url)
        self.data_analyzer = DataAnalyzer("amusement_park.db")

    def main(self):
        print("start of main")
        while True:
            print("\nWhat would you like to do?")
            print("1. api call")
            print("2. Print all data")
            print("3. Print available ride IDs and names")
            print("4. Print specific ride data")
            print("5. Quit")
            print("6. Create / Validate Database")
            print("7. AVerage_wait times")
            print("8. wait time trends")
            # print("x.  ")

            choice = input("Enter your choice: ")

            if choice == "1":
                output = self.api_client.api_call()
                clean = self.api_client.clean_input(output)
                self.db_helper.insert_rides(clean)
            elif choice == "2":
                self.db_helper.print_table("rides")
            elif choice == "3":
                print(self.db_helper.fetch_ride_ids_and_names())
            elif choice == "4":
                requested_id = input("Enter ride_id: ")
                print(self.db_helper.fetch_ride_by_id(requested_id))
            elif choice == "5":
                print("Quitting...")
                break
            elif choice == "6":
                self.db_helper.create_database()
                self.db_helper.validate_database()
            elif choice == "7":
                print(self.data_analyzer.average_wait_time())
            elif choice == "8":
                print(self.data_analyzer.wait_time_trends())
                
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()
