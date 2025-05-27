from db.db_helper import PLACEHOLDER

# user SQL definitions
USER_SQL = {
    'insert': 'INSERT INTO user (username) VALUES ({ph})',
    'select': 'SELECT id, username FROM user WHERE id = {ph}',
}

SQL_INSERT = USER_SQL['insert'].replace('{ph}', PLACEHOLDER)
SQL_SELECT = USER_SQL['select'].replace('{ph}', PLACEHOLDER)
