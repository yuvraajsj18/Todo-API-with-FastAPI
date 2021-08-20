import random
import string


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=random.randint(1, 32)))
