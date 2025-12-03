from fastapi import Depends
from db.repositories import AbstractRepository


class UserService:
    
    def __init__(self):
        pass
    
    
def get_user_service(user_repo: AbstractRepository = Depends()) -> UserService:
    return UserService(user_repo)
