import os
from time import sleep


class Person:
    def __init__(self, name):
        self.name = name

while True:
    # Dictionary to store references
    people = {}

    # Create one instance and store references to it
    original_person = Person("John")
    people["person1"] = original_person  # Stores reference
    people["person2"] = original_person  # Stores another reference to the same object

    # Demonstrate that they're the same object in memory
    print(f"Original ID: {id(original_person)}")

    person1_id = id(people["person1"])
    person2_id = id(people["person2"])

    print(f"Reference 1 ID: {person1_id}")
    print(f"Reference 2 ID: {person2_id}")

    # Changing the name using any reference will affect all references
    people["person1"].name = "Mike"

    # All references show the updated name because they point to the same object
    print(f"Original name: {original_person.name}")  # Prints: Mike
    print(f"Reference 1 name: {people['person1'].name}")  # Prints: Mike
    print(f"Reference 2 name: {people['person2'].name}")  # Prints: Mike

    some_variable = people["person1"]
    some_variable_2 = people["person2"]

    print(
        f"References are the same? {person1_id == person2_id == id(some_variable) == id(some_variable_2)}")  # Prints: True

    os.system("clear")
    sleep(0.1)