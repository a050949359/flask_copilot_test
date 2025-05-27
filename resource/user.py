"""
User API
---
post:
  summary: 新增使用者
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            username: {type: string}
  responses:
    201:
      description: 新增成功
      content:
        application/json:
          schema:
            type: object
            properties:
              id: {type: integer}
              username: {type: string}
    400:
      description: 缺少 username 或 username 已存在
get:
  summary: 取得單一使用者
  parameters:
    - in: path
      name: user_id
      schema:
        type: integer
      required: true
      description: 使用者ID
  responses:
    200:
      description: 成功取得使用者
      content:
        application/json:
          schema:
            type: object
            properties:
              id: {type: integer}
              username: {type: string}
    404:
      description: 使用者不存在
"""

from flask import request
from flask_restful import Resource
from db.db_helper import is_integrity_error, is_database_error
from db.user_sql import SQL_INSERT, SQL_SELECT

class User(Resource):
    def __init__(self, get_conn):
        self.get_conn = get_conn

    def post(self):
        data = request.get_json()
        username = data.get('username')
        if not username:
            return {'message': 'Username required'}, 400
        try:
            with self.get_conn() as conn:
                c = conn.cursor()
                c.execute(SQL_INSERT, (username,))
                conn.commit()
                user_id = c.lastrowid if hasattr(c, 'lastrowid') else c.lastrowid if hasattr(conn, 'insert_id') else None
        except Exception as e:
            if is_integrity_error(e):
                return {'message': 'Username already exists'}, 400
            if is_database_error(e):
                return {'message': f'Database error: {str(e)}'}, 500
            return {'message': f'Unknown error: {str(e)}'}, 500
        return {'id': user_id, 'username': username}, 201

    def get(self, user_id):
        try:
            with self.get_conn() as conn:
                c = conn.cursor()
                c.execute(SQL_SELECT, (user_id,))
                row = c.fetchone()
        except Exception as e:
            if is_database_error(e):
                return {'message': f'Database error: {str(e)}'}, 500
            return {'message': f'Unknown error: {str(e)}'}, 500
        if row:
            return {'id': row[0], 'username': row[1]}
        return {'message': 'User not found'}, 404
