import asyncio
import os
from backend.interfaces.IRepository import IRepository
from backend.repositories.TelegramRepository import TelegramRepository

class RepositoryManager():
    def __init__(self):
        self.repos = os.getenv("REPOS","").split(",")  
        self.REPO_MAP = {
            "telegram": TelegramRepository,
            "discord": "",
            "google_drive": "",
            "scp": "",
        }    
     
    async def uploadAll(self,path):
        tasks=[]
        
        for repo in self.repos:
            repoClass=self.REPO_MAP.get(repo.strip())
            if repoClass:
                tasks.append(self.upload(repo=repoClass,path=path))
                
        await asyncio.gather(*tasks)

    async def upload(self, repo:IRepository, path):
        
        await repo.upload(path)