from fastapi import Depends
from db.repositories import BaseRepository


class UserService:
    
    def __init__(self):
        pass
    
    
def get_user_service(user_repo: BaseRepository = Depends()) -> UserService:
    return UserService(user_repo)
