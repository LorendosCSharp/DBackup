from abc import ABC, abstractmethod

class IRepository(ABC):
    
    @abstractmethod
    async def upload(self,path:str):
        """Uploads the file to a repository"""
        pass