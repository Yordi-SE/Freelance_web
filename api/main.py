from model.base_model import User, Jobs
from model import storage
obj = storage.query('lemmaworkyotdanos@gmail.com')
print(obj)
print(obj.password)
print(obj.jobs)
