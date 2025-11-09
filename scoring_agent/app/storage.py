from threading import RLock
from typing import List

from .schemas import CompanyIn, LeadIn


class InMemoryStore:
    def __init__(self):
        self._lock = RLock()
        self._leads: List[LeadIn] = []
        self._companies: List[CompanyIn] = []

    def add_many_leads(self, leads: List[LeadIn]) -> int:
        with self._lock:
            self._leads.extend(leads)
            return len(leads)

    def add_many_companies(self, companies: List[CompanyIn]) -> int:
        with self._lock:
            self._companies.extend(companies)
            return len(companies)

    def leads(self) -> List[LeadIn]:
        with self._lock:
            return list(self._leads)

    def companies(self) -> List[CompanyIn]:
        with self._lock:
            return list(self._companies)

    def counts(self):
        with self._lock:
            return len(self._leads), len(self._companies)
