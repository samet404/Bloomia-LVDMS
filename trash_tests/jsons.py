import json

def json_demo():
    # Create a Python dictionary
    data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York",
        "hobbies": ["reading", "hiking", "photography"],
        "address": {
            "street": "123 Main St",
            "zip": "10001"
        }
    }

    # Encoding (Python object to JSON string)
    json_string = json.dumps(data, indent=4)
    print("Encoded JSON:")
    print(json_string)
    print("\n")

    # Writing JSON to a file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Decoding (JSON string to Python object)
    decoded_data = json.loads(json_string)
    print("Decoded data:")
    print(f"Name: {decoded_data['name']}")
    print(f"Age: {decoded_data['age']}")
    print(f"Hobbies: {', '.join(decoded_data['hobbies'])}")
    print("\n")

    # Reading JSON from a file
    with open('data.json', 'r') as f:
        file_data = json.load(f)
    print("Data read from file:")
    print(file_data)

if __name__ == "__main__":
    json_demo()