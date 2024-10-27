class User:
    def __init__(self, id: int, username: str, salt: str, password: str, is_scout:bool):
        self.id = id
        self.username = username
        self.salt = salt
        self.password = password
        self.is_scout=is_scout

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', is_scout='{self.is_scout}')>"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        return False

