import requests

from configuration import conf


def fetch_todo():
    response = requests.get(
        f"{conf.auth_server_uri}/api/auth/get-session",
        cookies={
            "better-auth.session_token": "1BpJi7LZtXfxWCG94QroYSoTr8Oq1wpM.U6%2FX62B7XwjjWIn8T1t4GaJdFT12JLT21KJs80N%2BJS8%3D"
        }
    )


    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error: {response.status_code}"


if __name__ == "__main__":
    result = fetch_todo()
    print(result)