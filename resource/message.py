"""
Message API
---
get:
  summary: 取得所有訊息或單一訊息
  parameters:
    - in: path
      name: message_id
      schema:
        type: integer
      required: false
      description: 訊息ID（可選）
  responses:
    200:
      description: 成功取得訊息
      content:
        application/json:
          schema:
            oneOf:
              - type: object
                properties:
                  id: {type: integer}
                  user_id: {type: integer}
                  content: {type: string}
              - type: array
                items:
                  type: object
                  properties:
                    id: {type: integer}
                    user_id: {type: integer}
                    content: {type: string}
    404:
      description: 訊息不存在
post:
  summary: 新增訊息
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            user_id: {type: integer}
            content: {type: string}
  responses:
    201:
      description: 新增成功
      content:
        application/json:
          schema:
            type: object
            properties:
              id: {type: integer}
              user_id: {type: integer}
              content: {type: string}
    400:
      description: 缺少參數
    404:
      description: 使用者不存在
put:
  summary: 修改訊息內容
  parameters:
    - in: path
      name: message_id
      schema:
        type: integer
      required: true
      description: 訊息ID
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            content: {type: string}
  responses:
    200:
      description: 修改成功
    400:
      description: 缺少內容
    404:
      description: 訊息不存在
delete:
  summary: 刪除訊息
  parameters:
    - in: path
      name: message_id
      schema:
        type: integer
      required: true
      description: 訊息ID
  responses:
    200:
      description: 刪除成功
    404:
      description: 訊息不存在
"""

from flask import request
from flask_restful import Resource
from db_helper import is_database_error

class Message(Resource):
    SQL_SELECT_ONE = "SELECT id, user_id, content FROM message WHERE id=%s"
    SQL_SELECT_ALL = "SELECT id, user_id, content FROM message"
    SQL_INSERT = "INSERT INTO message (user_id, content) VALUES (%s, %s)"
    SQL_UPDATE = "UPDATE message SET content=%s WHERE id=%s"
    SQL_DELETE = "DELETE FROM message WHERE id=%s"
    SQL_USER_EXISTS = "SELECT id FROM user WHERE id=%s"

    def __init__(self, get_conn):
        self.get_conn = get_conn

    def get(self, message_id=None):
        try:
            with self.get_conn() as conn:
                c = conn.cursor()
                if message_id:
                    c.execute(self.SQL_SELECT_ONE, (message_id,))
                    row = c.fetchone()
                    if row:
                        return {'id': row[0], 'user_id': row[1], 'content': row[2]}
                    return {'message': 'Message not found'}, 404
                else:
                    c.execute(self.SQL_SELECT_ALL)
                    rows = c.fetchall()
                    return [{'id': r[0], 'user_id': r[1], 'content': r[2]} for r in rows]
        except Exception as e:
            if is_database_error(e):
                return {'message': f'Database error: {str(e)}'}, 500
            return {'message': f'Unknown error: {str(e)}'}, 500

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        content = data.get('content')
        if not user_id or not content:
            return {'message': 'user_id and content required'}, 400
        try:
            with self.get_conn() as conn:
                c = conn.cursor()
                c.execute(self.SQL_USER_EXISTS, (user_id,))
                if not c.fetchone():
                    return {'message': 'User not found'}, 404
                c.execute(self.SQL_INSERT, (user_id, content))
                conn.commit()
                message_id = c.lastrowid if hasattr(c, 'lastrowid') else c.lastrowid if hasattr(conn, 'insert_id') else None
            return {'id': message_id, 'user_id': user_id, 'content': content}, 201
        except Exception as e:
            if is_database_error(e):
                return {'message': f'Database error: {str(e)}'}, 500
            return {'message': f'Unknown error: {str(e)}'}, 500

    def put(self, message_id):
        data = request.get_json()
        content = data.get('content')
        if not content:
            return {'message': 'Content required'}, 400
        try:
            with self.get_conn() as conn:
                c = conn.cursor()
                c.execute(self.SQL_UPDATE, (content, message_id))
                if c.rowcount == 0:
                    return {'message': 'Message not found'}, 404
                conn.commit()
            return {'id': message_id, 'content': content}
        except Exception as e:
            if is_database_error(e):
                return {'message': f'Database error: {str(e)}'}, 500
            return {'message': f'Unknown error: {str(e)}'}, 500

    def delete(self, message_id):
        try:
            with self.get_conn() as conn:
                c = conn.cursor()
                c.execute(self.SQL_DELETE, (message_id,))
                if c.rowcount == 0:
                    return {'message': 'Message not found'}, 404
                conn.commit()
            return {'message': 'Deleted'}
        except Exception as e:
            if is_database_error(e):
                return {'message': f'Database error: {str(e)}'}, 500
            return {'message': f'Unknown error: {str(e)}'}, 500
