from datetime import datetime
import os
import shutil
from backend.repositories.RepositoryManager import RepositoryManager
from docker.models.containers import Container

class BackupGenerator():
    
    def __init__(self,dockerClient):
        
        self.client=dockerClient
        self.basePath=""
        


    ## All those print statments were writen by me. I like to see info about everything. Bleh >:3
    
    def setBasePath(self):
        
        ## For now I will find it like this. I will try to find more elegant way
        
        runnerContainers = self.client.containers.list(filters={"label": "dbackup.runner=this"})
        if not runnerContainers:
            raise RuntimeError("=== No runner container found ===")
        
        if runnerContainers is not None:
            runner= runnerContainers[0]
            for attribute in runner.attrs["Mounts"]:
                if attribute["Type"]=="bind" and attribute["Destination"]=="/app/work":
                    self.basePath=attribute["Source"]
                    
        if not self.basePath:
            raise RuntimeError("=== No valid host folder found for runner container ===")   
        
        print(f"=== BASE PATH {self.basePath} ===")
    
    async def setJobs(self,container:Container):
    
        labels = container.labels
        if labels.get("dbackup.on") != "true":
            return
        
        print("=== Backup In Progress For %s ===" % container.name)
        await self.manageMounts(container)
            

    async def manageMounts(self,container:Container):
        
        print("=== Attributes of this container === \n",container.attrs["Mounts"])
        
        
        paths=[]
        container.pause()            
        for attribute in container.attrs["Mounts"]:
                
            path=self.save(attribute.get("Source") or attribute["Name"],container.name,attribute["Destination"].replace("/","_"),attribute["Type"])
            paths.append(path)
        await self.repositoryManager.uploadAll(paths)
        container.unpause() 
            
        
               

    def save(self, path:str, containerName:str, destinationPath:str, dataType:str)->str:
        
        currentTime = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        filename= f"{currentTime}[=]{containerName}[=]{destinationPath}[=]{dataType}.tar.gz"
        target = os.path.join("/temp",filename)
        
        print(f"=== Coping Data To {target} ===")
        
        savePath=os.path.join(self.basePath,"temp")
        
        tempContainer:Container=self.client.containers.run(
            image="alpine",
            command=f"tar czf {target} -C /data .",
            volumes={
                path: {"bind": "/data", "mode": "ro"},
                savePath: {"bind": "/temp", "mode": "rw"},
            },
            detach=True
        )  
        
        result=tempContainer.wait()
        tempContainer.remove()
        
        if result.get("StatusCode") !=0:
            raise RuntimeError(f"--- Container Failed {result}---")
        
        savedFilePath="/app/work"+target
        print(savedFilePath)
        if not os.path.exists(savedFilePath):
            raise RuntimeError(f"=== Backup couldn't be found after generating it {savedFilePath} ===")
        
        print(f"=== Saved {target} ===")
        return savedFilePath

    async def scan(self):
        
        print("=== Scan started ===")
        for c in self.client.containers.list():
            await self.setJobs(c)
        allFiles = os.listdir("/app/work/temp")
        for file in allFiles:
            srcPath=os.path.join("/app/work/temp",file)
            destPath=os.path.join("/app/work/backups",file)
            
            shutil.move(srcPath,destPath)
        

    async def init(self):
        
        self.setBasePath()
        os.makedirs(self.basePath, exist_ok=True)
        os.makedirs("/app/work/backups", exist_ok=True)
        os.makedirs("/app/work/temp", exist_ok=True)
        
        self.repositoryManager = RepositoryManager()
        await self.repositoryManager.instanciateAll()

        
