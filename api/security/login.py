from fastapi import Depends, APIRouter, Security
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

# Fake DB
DB = {
    'users': {
        'johndoe@mail.com': {
            'name': 'John Doe',
            'password': 'hunter2'
        }
    }
}


# Login Manager
SECRET = "super-secret-key"
manager = LoginManager(SECRET, '/login')

@manager.user_loader()
def query_user(user_id: str):
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    return DB['users'].get(user_id)


# Init Routes
login_route = APIRouter()


# Routes
@login_route.post('/login')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = query_user(email)
    if not user:
        # you can return any response or error of your choice
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={'sub': email}
    )
    return {'token': access_token}


@login_route.get('/proteced')
def protected_route(user=Depends(manager)):
    return {'user': user}
