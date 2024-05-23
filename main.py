#!/usr/bin/env python4

from ride_api_call import api_call, print_clean, clean_input
from database_helper import DatabaseHelper


class main:
    def create_url(self, url_pre, land_id, url_suff):
        return f"{url_pre}/{land_id}/{url_suff}"

    def __init__(self):
        print("start of main")
        url_pre = "https://queue-times.com/parks"
        land_id = "32"
        url_suff = "queue_times.json"
        self.url = self.create_url(url_pre, land_id, url_suff)
        self.db_helper = DatabaseHelper("amusement_park.db")

    def run(self):
        print("running main functions")
        print(self.url)
        api_response = api_call(self.url)
        # print(api_response)
        # print_clean(api_response)
        output = clean_input(api_response)
        # print(output)
        # self.db_helper.drop_table("rides")
        self.db_helper.create_database()
        self.db_helper.validate_database()
        self.db_helper.insert_list(output)
        self.db_helper.print_table("rides")


if __name__ == "__main__":
    main_class = main()
    main_class.run()
