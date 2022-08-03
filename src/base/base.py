from typing import Any


class CRUD:
    @staticmethod
    def create(data: object) -> bool:
        raise NotImplementedError

    @staticmethod
    def read(**kwargs: Any) -> object:
        raise NotImplementedError

    @staticmethod
    def update(data: object) -> bool:
        raise NotImplementedError

    @staticmethod
    def delete(**kwargs: Any) -> bool:
        raise NotImplementedError
