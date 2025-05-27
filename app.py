from flask import Flask
from flask_restful import Api
from db.db import init_db
from db.db_helper import get_conn
from resource.user import User
from resource.message import Message

app = Flask(__name__)
api = Api(app)

api.add_resource(User, '/user', '/user/<int:user_id>', resource_class_kwargs={'get_conn': get_conn})
api.add_resource(Message, '/message', '/message/<int:message_id>', resource_class_kwargs={'get_conn': get_conn})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)