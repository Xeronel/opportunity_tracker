class QueryGroup:
    def __init__(self, db):
        self.execute = db.execute
        self.parse_query = db.parse_query
        self.pool = db.pool
        self.connect = db.connect
