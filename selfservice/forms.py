import re
from typing import List

from fastapi import Request


class EduroamUserForm:
    def __init__(self, request: Request):
        self.request = request
        self.errors: List = []
        self.username: str = ""
        self.password: str = ""
        self.password2: str = ""
        self.re_username = (
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
        self.password2 = form.get("password2")

    def is_valid(self):
        if not self.username:
            self.errors.append("Invalid username")
        if not self.password:
            self.errors.append("Invalid password")
        if not self.password2:
            if "Invalid password" not in self.errors:
                self.errors.append("Invalid password")
        if not self.username:
            self.errors.append("Username must not be empty")
        if not re.match(self.re_username, self.username):
            self.errors.append("Invalid e-mail adress")
        if len(self.password) < 8:
            self.errors.append("Password too short")
        if len(self.password2) < 8:
            if "Password too short" not in self.errors:
                self.errors.append("Password too short")
        if self.password != self.password2:
            self.errors.append("Passwords do not match")
        return self.errors
