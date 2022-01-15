from dataclasses import dataclass
from datetime import date

@dataclass
class User:
    "User Class Repr"
    id: int = 0
    language: str = "en"

