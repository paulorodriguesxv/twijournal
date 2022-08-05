from abc import ABCMeta, abstractmethod
from pydantic import BaseModel

class ICrudRepository(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, entity: BaseModel) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> BaseModel:
        pass

    @abstractmethod
    async def add(self, entity: BaseModel) -> BaseModel:
        pass    

    @abstractmethod
    async def update(self, id: str, entity: BaseModel) -> BaseModel:
        pass        

    @abstractmethod
    async def delete(self, id: str):        
        pass
           