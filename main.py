#!/usr/bin/python3
from model.base_model import User, Jobs
from model import storage
obj = storage.all(User)
obj1= storage.all(Jobs)
print(obj[0].first_name)
print(obj1[0].title)
