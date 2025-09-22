# -*- coding: utf-8 -*-

# from module_human_written import Profile, User
from module_generated import Profile, User

user_data = {
    "user_id": 1,
    "profile": {
        "firstname": "John",
        "lastname": "Doe",
        "status": "active",
    },
    "tags": {"role": "admin"},
}
user = User.new(user_data)

print(f"{user.user_id = }")
print(f"{user.profile = }")
print(f"{user.labels = }")
print(f"{user.tags = }")

print(f"{user.profile.firstname = }")
print(f"{user.profile.lastname = }")
print(f"{user.profile.phone_number = }")
print(f"{user.profile.status = }")
