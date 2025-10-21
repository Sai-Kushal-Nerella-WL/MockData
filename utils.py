import random
import string
from datetime import date, timedelta
from typing import Optional

from faker import Faker


def get_faker(seed: int) -> Faker:
    fake = Faker()
    Faker.seed(seed)
    random.seed(seed)
    return fake


def clamp_decimal(value, min_value=None, max_value=None):
    if min_value is not None and value < min_value:
        value = min_value
    if max_value is not None and value > max_value:
        value = max_value
    return value


def ensure_max_length(s: Optional[str], max_len: Optional[int]) -> Optional[str]:
    if s is None or max_len is None:
        return s
    if len(s) <= max_len:
        return s
    return s[:max_len]


def random_state_us(fake: Faker) -> str:
    return fake.state_abbr(include_territories=False)


def random_sex() -> str:
    return random.choice(["M", "F"])


def future_date(fake: Faker, years_ahead_min=1, years_ahead_max=5) -> date:
    today = date.today()
    delta_years = random.randint(years_ahead_min, years_ahead_max)
    try:
        return date(today.year + delta_years, today.month, today.day)
    except ValueError:
        return today + timedelta(days=365 * delta_years)


def past_date(fake: Faker, years_back_min=0, years_back_max=30) -> date:
    days = random.randint(years_back_min * 365, years_back_max * 365)
    return date.today() - timedelta(days=days)


def dob_for_age(fake: Faker, min_age=18, max_age=90) -> date:
    age = random.randint(min_age, max_age)
    days = age * 365 + random.randint(0, 364)
    return date.today() - timedelta(days=days)


def random_phone(fake: Faker) -> str:
    return f"{random.randint(200,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"


def random_cc_number() -> str:
    return ''.join(random.choices(string.digits, k=16))
