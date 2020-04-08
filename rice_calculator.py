import sqlite3
from os import path
import questionary


def dict_factory(cursor, row):
    dictionary = {}
    for index, column in enumerate(cursor.description):
        dictionary[column[0]] = row[index]
    return dictionary


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

        self.connection.row_factory = dict_factory

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_all_rice_types(self):
        """Gets all rice types from the rice_types table."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, type FROM rice_types")
        return cursor.fetchall()

    def select_one_rice_type(self, rice_type_id: int) -> str:
        """"Selects a specific type of rice.

        PARAMETERS:
        rice_type_id as an int

        RETURNS:
        Corresponding rice type name to the ID as a string.
        """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT type FROM rice_types WHERE id = {rice_type_id}")
        rice_type = cursor.fetchone()
        return rice_type["type"]

    def get_all_cooking_devices(self, rice_type_id: int):
        """Gets all usable cooking devices from the device_types table."""
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT
  dt.id AS id,
  dt.type AS type
FROM
  device_types dt
  JOIN rice_type_to_device_type rttdt ON rttdt.device_type_id = dt.id
WHERE rttdt.rice_type_id = {rice_type_id}
""")
        return cursor.fetchall()

    def select_one_cooking_device(self, cooking_device_id: int) -> str:
        """"Selects a specific cooking device.

        PARAMETERS:
        cooking_device_id as an int

        RETURNS:
        Corresponding device name to the ID as a string.
        """
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT type FROM device_types WHERE id = {cooking_device_id}")
        device_type = cursor.fetchone()
        return device_type["type"]

    def calculate_steps(self, rice_type_id, cooking_device_id, rice_amount):
        """"Joins multiple tables, gets a specific combination of parameters,
        calculates liquid_amount and puts everything together in a string.

        PARAMETERS:
        rice_type_id, cooking_device_id and rice_amount

        RETURNS:
        A string containing instructions for the user to cook their rice.
        """
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT
  rt.type AS rice_type,
  dt.type AS device_type,
  lt.type AS liquid_type,
  rt.liquid_ratio AS liquid_ratio,
  rttdt.cooking_time AS cooking_time,
  rt.info_text AS info_text
FROM
  rice_types rt
  JOIN rice_type_to_device_type rttdt ON rt.id = rttdt.rice_type_id
  JOIN device_types dt ON dt.id = rttdt.device_type_id
  JOIN liquid_types lt ON lt.id = rt.liquid_type_id
WHERE rt.id = {rice_type_id} AND dt.id = {cooking_device_id};""")

        calc_step_list = cursor.fetchone()

        liquid_amount = int(rice_amount) * calc_step_list["liquid_ratio"]
        rice_name = calc_step_list["rice_type"].lower()
        liquid_name = calc_step_list["liquid_type"].lower()
        device_name = calc_step_list["device_type"].lower()
        cooking_time = calc_step_list["cooking_time"]
        info_text = calc_step_list["info_text"]

        steps = (f"Take {rice_amount}g of "
                 f"{rice_name} Rice and cook it in "
                 f"{liquid_amount}ml of "
                 f"{liquid_name} for "
                 f"{cooking_time} minutes in your "
                 f"{device_name}.\n")

        if info_text is not None:
            steps += f"\nNOTE: {info_text}\n"

        return steps

    def greet_user(self):
        """Greets the user when starting the program."""
        print("Welcome to RiceCalculator™!\n")

    def rice_selection(self):
        """"Draws the rice-selection screen for the user.

        PARAMETERS:
        None

        RETURNS:
        Selected rice type's ID as an int and name as a string in a tuple.
        """
        rice_selection_text = (
            "Here's a list of the most common rice varieties.\n"
            " Just select the one you want to cook!\n")

        rice_types = self.get_all_rice_types()

        rice_type_names = [rice_type["type"] for rice_type in rice_types]

        chosen_rice_type_name = questionary.select(
            rice_selection_text,
            choices=rice_type_names
        ).ask()

        rice_type_id = None
        rice_type_name = None

        for rice_type in rice_types:
            if chosen_rice_type_name is rice_type["type"]:
                rice_type_id = rice_type["id"]
                rice_type_name = rice_type["type"]

        return rice_type_id, rice_type_name

    def get_rice_amount(self) -> int:
        """"Asks the user how much rice they want to cook.

        PARAMETERS:
        None

        RETURNS:
        Amount of rice wanted as an int.
        """
        try:
            return int(questionary.text("Thank you! Now tell me how much you want to cook in grams\n").ask())
        except Exception:
            print("Please input a number (without decimal points!)")
            return self.get_rice_amount()

    def device_selection(self, rice_type_id: int):
        """"Draws the device-selection screen for the user.

        PARAMETERS:
        None

        RETURNS:
        Selected device type's ID as an int and name as a string in a tuple.
        """
        device_types = self.get_all_cooking_devices(rice_type_id)
        device_type_names = [device_type["type"] for device_type in device_types]

        device_selection_text = "Great! Now, what usable device do you wan't too cook it in?\n"
        chosen_device_type_name = questionary.select(
            device_selection_text,
            choices=device_type_names
        ).ask()

        cooking_device_id = None
        cooking_device_name = None

        for device_type in device_types:
            if chosen_device_type_name is device_type["type"]:
                cooking_device_id = device_type["id"]
                cooking_device_name = device_type["type"]

        return cooking_device_id, cooking_device_name

    def return_final_steps(self, selected_rice_type_id: int, selected_device_type: int, rice_amount: int):
        """"Draws the device-selection screen for the user.

        PARAMETERS:
        selected_rice_type_id -> int, selected_device_type -> int, rice_amount -> int

        RETURNS:
        A print statement with the return string of calculate_steps()
        """
        steps_to_take = self.calculate_steps(selected_rice_type_id, selected_device_type, rice_amount)
        print(f"Thanks a lot! "
              f"Here are the steps you need to take: \n\n\n{steps_to_take}\n"
              f"Have a rice meal!\n")

    def start(self):
        """Starts the program."""
        self.greet_user()
        selected_rice_type = self.rice_selection()
        rice_amount = self.get_rice_amount()
        selected_device_type = self.device_selection(selected_rice_type[0])
        self.return_final_steps(selected_rice_type[0], selected_device_type[0], rice_amount)


rice_calculator = RiceCalculator()
rice_calculator.start()
rice_calculator.disconnect()
