import string
import random


def random_slug() -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(4))
