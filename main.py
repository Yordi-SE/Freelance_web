#!/usr/bin/python3
from model.base_model import User, Jobs
from model import storage
obj = storage.job()
for objs in obj:
    print(objs)
