from flask import Flask, request
from pymilvus import MilvusClient

from Env import Env

app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)

    client = MilvusClient(
        uri = Env("MILVUS_URI")
    )

    @app.route('/init-user', methods=['POST'])
    def init_user():
        data = request.get_json()
        print("initilizing user...")
        print(data)

        client.create_database(
            db_name=data['user_id'] ,
            properties={
                "database.diskQuota.mb": 512,
            }
        )

