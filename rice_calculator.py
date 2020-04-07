import sqlite3
from os import path
from tabulate import tabulate
# from tkinter import *

# This little program takes your input on what type of rice, in which device and how much you want too cook.
# It then calculates the amount of water you need! It also shows you neat little infos depending on what
# variety you cook!
#
# Authors: Velican Akcakaya and Nicklas Reincke, 6th of April 2020.


class RiceCalculator:

    def __init__(self):
        self.connection = None
        self.database_file_name = "rice_database.db"
        self.database_seed_file_name = "rice_database.sql"

        if not path.exists(self.database_file_name):
            query = open(self.database_seed_file_name, "r").read()

            self.connection = sqlite3.connect(self.database_file_name)

            cursor = self.connection.cursor()
            cursor.executescript(query)

            self.connection.commit()

        if self.connection is None:
            self.connection = sqlite3.connect(self.database_file_name)

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def show_all_rice_types(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, type FROM rice_types")
        rice_types = list(cursor.fetchall())

        headers = ["NUMBER", "RICE TYPE"]
        print(tabulate(rice_types, headers, tablefmt="fancy_grid"))

    def select_one_rice_type(self, rice_type_id: int) -> str:
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT type FROM rice_types WHERE id = {rice_type_id}")
        rice_type = cursor.fetchone()
        return rice_type[0]

    def show_all_cooking_devices(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT id, type FROM device_types")
        device_types = list(cursor.fetchall())

        headers = ["NUMBER", "DEVICE"]
        print(tabulate(device_types, headers, tablefmt="fancy_grid"))

    def select_one_cooking_device(self, cooking_device_id):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT type FROM device_types WHERE id = {cooking_device_id}")
        device_type = cursor.fetchone()
        return device_type[0]

    def calculate_steps(self, rice_type_id, cooking_device_id, rice_amount):
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT
  rt.type,
  dt.type,
  lt.type,
  rt.liquid_ratio,
  rttdt.cooking_time,
  rt.info_text
FROM
  rice_types rt
  JOIN rice_type_to_device_type rttdt ON rt.id = rttdt.rice_type_id
  JOIN device_types dt ON dt.id = rttdt.device_type_id
  JOIN liquid_types lt ON lt.id = rt.liquid_type_id
WHERE rt.id = {rice_type_id} AND dt.id = {cooking_device_id};""")

        calc_step_list = cursor.fetchone()
        rice_name, device_name, liquid_name, liquid_ratio, cooking_time, info_text = calc_step_list

        liquid_amount = int(rice_amount) * liquid_ratio
        liquid_name = liquid_name.lower()
        device_name = device_name.lower()

        steps = (f"Take {rice_amount}g of "
                 f"{rice_name} Rice and cook it in "
                 f"{liquid_amount}ml of "
                 f"{liquid_name} for "
                 f"{cooking_time} minutes in your "
                 f"{device_name}")

        if info_text is not None:
            steps += f"\n\nNOTE: {info_text}"

        return steps

    def start(self):
        print("Welcome to RiceCalculator™!\n")
        self.show_all_rice_types()
        rice_type_id = input("""Here's a list of the most common rice varieties.
Just select the one you want to cook!\n""")

        selected_rice_type = self.select_one_rice_type(int(rice_type_id))
        print(f"You decided to use this type of rice: {selected_rice_type}")

        rice_amount = input("Thank you! Now tell me how much you want to cook in grams\n")

        self.show_all_cooking_devices()
        cooking_device_id = input("Great! Now, what do you wan't too cook it in?\n")
        device_type_name = self.select_one_cooking_device(cooking_device_id)
        print(f"You decided to use this device: {device_type_name}")

        steps_to_take = self.calculate_steps(rice_type_id, cooking_device_id, rice_amount)
        print(f"""Thanks a lot!
Here are the steps you need to take: \n\n\n{steps_to_take}""")


rice_calculator = RiceCalculator()
rice_calculator.start()
rice_calculator.disconnect()
