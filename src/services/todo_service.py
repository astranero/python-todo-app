from entities.todo import Todo
from entities.user import User
from repositories.todo_repository import todo_repository
from repositories.user_repository import user_repository


class InvalidCredentials(Exception):
    pass


class UsernameExists(Exception):
    pass


class TodoService:
    def __init__(self):
        self.user = None

    def create_todo(self, content):
        todo = Todo(content=content, user=self.user)

        return todo_repository.create(todo)

    def get_undone_todos(self):
        if not self.user:
            return []

        todos = todo_repository.find_by_username(self.user.username)
        undone_todos = filter(lambda todo: not todo.done, todos)

        return list(undone_todos)

    def set_todo_done(self, todo_id):
        todo_repository.set_done(todo_id)

    def login(self, username, password):
        user = user_repository.find_by_username(username)

        if not user or user.password != password:
            raise InvalidCredentials('Invalid username or password')

        self.user = user

        return user

    def get_current_user(self):
        return self.user

    def logout(self):
        self.user = None

    def create_user(self, username, password):
        existing_user = user_repository.find_by_username(username)

        if existing_user:
            raise UsernameExists(f'Username {username} already exists')

        return user_repository.create(User(username, password))


todo_service = TodoService()