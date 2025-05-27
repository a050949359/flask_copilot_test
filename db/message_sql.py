from db.db_helper import PLACEHOLDER

# message SQL definitions
MESSAGE_SQL = {
    'select_one': 'SELECT id, user_id, content FROM message WHERE id = {ph}',
    'select_all': 'SELECT id, user_id, content FROM message',
    'insert': 'INSERT INTO message (user_id, content) VALUES ({ph}, {ph})',
    'update': 'UPDATE message SET content = {ph} WHERE id = {ph}',
    'delete': 'DELETE FROM message WHERE id = {ph}',
    'user_exists': 'SELECT 1 FROM user WHERE id = {ph}',
}

SQL_SELECT_ONE_MESSAGE = MESSAGE_SQL['select_one'].replace('{ph}', PLACEHOLDER)
SQL_SELECT_ALL_MESSAGE = MESSAGE_SQL['select_all']
SQL_INSERT_MESSAGE = MESSAGE_SQL['insert'].replace('{ph}', PLACEHOLDER)
SQL_UPDATE_MESSAGE = MESSAGE_SQL['update'].replace('{ph}', PLACEHOLDER)
SQL_DELETE_MESSAGE = MESSAGE_SQL['delete'].replace('{ph}', PLACEHOLDER)
SQL_USER_EXISTS = MESSAGE_SQL['user_exists'].replace('{ph}', PLACEHOLDER)
