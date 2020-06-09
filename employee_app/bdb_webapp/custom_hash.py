from django.contrib.auth.hashers import Argon2PasswordHasher


class MyArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = Argon2PasswordHasher.time_cost * 10  # default 2
    memory_cost = Argon2PasswordHasher.memory_cost * 10  # default 512 KiB
    parallelism = Argon2PasswordHasher.parallelism * 2  # default 2
