from app.repositories.user_repo import UserRepo

class UserManager:
    def __init__(self, token_provider):
        self.repo = UserRepo()
        self.auth = token_provider

    def register_user(self, username, password):
        user_id = self.repo.add_user(username, password)
        return user_id

    def login_user(self, username, password):
        user_id = self.repo.authenticate_user(username, password)
        
        if user_id:
            token = self.auth.generate_token(user_id, username)
            return token
        return None