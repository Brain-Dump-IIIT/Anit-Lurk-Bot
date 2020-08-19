import sqlite3

class DbConn:
    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
        self.create_tables()

    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS user_stats (
            user_id         TEXT PRIMARY KEY,
            message_count   INTEGER,
            character_count INTEGER,
            score_count     INTEGER
            )
        ''')

    def add_person(self, user_id):
        query = '''
            INSERT OR IGNORE INTO user_stats (user_id, message_count, 
                                                character_count, score_count)
            VALUES (?, 0, 0, 0)
        '''
        
        self.conn.execute(query, (user_id,))
        self.conn.commit()

    def message_count_increment(self, user_id, char_count, score_count):
        query = '''
            UPDATE user_stats SET message_count = message_count + 1,
                        character_count = character_count + ?,
                        score_count = score_count + ?
            WHERE user_id = ?
        '''

        self.conn.execute(query, (char_count, score_count, user_id, ))
        self.conn.commit()
