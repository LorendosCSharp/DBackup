from abc import ABC, abstractmethod

class IRepository(ABC):
    
    @abstractmethod
    def upload(self,path:str):
        """Uploads the file to a repository"""
        pass