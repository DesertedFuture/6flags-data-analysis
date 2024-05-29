#!/usr/bin/env python4

from database_helper import DatabaseHelper
from ride_api_call import APIClient


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
            print("x. Maybe delete database from bad values? ")
            print("x. maybe operations menu to do operations on specific data ")
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
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_instance = Main()
    main_instance.main()
