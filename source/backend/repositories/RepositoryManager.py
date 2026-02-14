import asyncio
import os
from backend.interfaces.IRepository import IRepository
from backend.repositories.TelegramRepository import TelegramRepository

class RepositoryManager():
    def __init__(self):
        self.repos:list[IRepository]=[]
        self.reposEnv = os.getenv("REPOS","").split(",")  
        self.REPO_MAP = {
            "telegram": TelegramRepository,
            "discord": "",
            "google_drive": "",
            "scp": "",
        }    
    
    async def instanciateAll(self):
        print("=== Instanciating Repos ===")
        tasks=[]
        for repo in self.reposEnv:
            repoClass=self.REPO_MAP.get(repo.strip())
            if repoClass:
                tasks.append(self.instanciate(repoClass))
        await asyncio.gather(*tasks)
                
    
    async def instanciate(self,repoClass:IRepository):
        
        repo:IRepository = repoClass()
        await repo.instance()
        self.repos.append(repo)
        print("=== Added Repo ===")
        
        
    
    async def uploadAll(self,path):
        tasks=[]
        for repo in self.repos:
            tasks.append(self.upload(repo,path))
            print(f"=== Upload task {repo} ===")
                
        await asyncio.gather(*tasks)

    async def upload(self, repo:IRepository, path):
        
        print(f"=== Strarted uploading for {repo} ===")
        await repo.upload(path)