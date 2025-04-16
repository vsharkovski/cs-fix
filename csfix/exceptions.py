class DatabaseError(Exception):
    pass


class DatabaseNotConnectedError(DatabaseError):
    pass
