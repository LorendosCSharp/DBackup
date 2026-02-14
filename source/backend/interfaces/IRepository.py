from abc import ABC, abstractmethod

class IRepository(ABC):
    
    @abstractmethod
    async def upload(self,path:str):
        """Uploads the file to a repository"""
        pass
    @abstractmethod
    async def instance():
        """Method to instanciate the repo. 
        In other words this is method to connect to the right repo origin"""
        pass