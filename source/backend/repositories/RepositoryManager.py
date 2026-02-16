import asyncio
import os
from backend.interfaces.IRepository import IRepository
from backend.repositories import TelegramRepository, SCPRepository

class RepositoryManager():
    def __init__(self):
        self.repos:list[IRepository]=[]
        self.reposEnv = os.getenv("REPOS","").split(",")  
        self.REPO_MAP = {
            "telegram": TelegramRepository.TelegramRepository,
            "discord": "",
            "google_drive": "",
            "scp": SCPRepository.SCPRepository,
        }    
    
    async def instanciateAll(self):
        print("=== Instanciating Repos ===")
        tasks=[]
        for repo in self.reposEnv:
            print(f"=== Repo Class {repo}")
            repoClass=self.REPO_MAP.get(repo.strip())
            if repoClass:
                tasks.append(self.instanciate(repoClass))
        await asyncio.gather(*tasks)
                
    
    async def instanciate(self,repoClass:IRepository):
        
        repo:IRepository = repoClass()
        await repo.instance()
        self.repos.append(repo)
        print("=== Added Repo ===")
        
        
    
    async def uploadAll(self,paths:list[str]):
        tasks=[]
        for repo in self.repos:
            tasks.append(self.upload(repo,paths))
            print(f"=== Upload task {repo} ===")
                
        await asyncio.gather(*tasks)

    async def upload(self, repo:IRepository, paths:list[str]):
        
        try:
            print(f"=== Strarted uploading for {repo} ===")
            await repo.upload(paths)
        except Exception as e:
            print(f"--- Error occurred while uploading {e} ---")