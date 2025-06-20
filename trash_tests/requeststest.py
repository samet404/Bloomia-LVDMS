import requests

def fetch_todo():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error: {response.status_code}"


if __name__ == "__main__":
    result = fetch_todo()
    print(result)