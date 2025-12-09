from dataclasses import dataclass


@dataclass
class Connessione:
    r1: int
    r2: int
    anno: str
    distanza: float
    difficolta: str


    def __eq__(self, other):
        return isinstance(other, Connessione) and self.r1 == other.r1 and self.r2 == other.r2

    def __str__(self):
        return f"Tratta: {self.r1} - {self.r2}"

    def __repr__(self):
        return f"Tratta: {self.r1} - {self.r2}"