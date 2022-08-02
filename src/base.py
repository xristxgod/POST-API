from abc import ABC, abstractmethod


class CRUD(ABC):
    @staticmethod
    @abstractmethod
    def create(data: object) -> bool:
        ...
