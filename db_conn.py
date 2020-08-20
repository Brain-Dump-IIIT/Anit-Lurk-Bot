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
        """Adds a person to db or ignores if already present"""
        query = '''
            INSERT OR IGNORE INTO user_stats (user_id, message_count, 
                                                character_count, score_count)
            VALUES (?, 0, 0, 0)
        '''
        
        self.conn.execute(query, (user_id,))
        self.conn.commit()

    def remove_person(self, user_id):
        """Removes a person from db"""
        query = '''
            DELETE FROM user_stats
            WHERE user_id = ?
        '''

        self.conn.execute(query, (user_id,))
        self.conn.commit()

    def message_count_increment(self, user_id, mess_count, char_count, score_count):
        """Updates values for users"""
        query = '''
            UPDATE user_stats SET message_count = message_count + ?,
                        character_count = character_count + ?,
                        score_count = score_count + ?
            WHERE user_id = ?
        '''

        self.conn.execute(query, (mess_count, char_count, score_count, user_id, ))
        self.conn.commit()

    def reset(self):
        """Reset score of all people in db"""
        query = '''
            UPDATE user_stats SET score_count = 0
        '''

        self.conn.execute(query)
        self.conn.commit()
