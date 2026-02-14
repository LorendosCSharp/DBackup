import asyncio
from datetime import datetime
import os
from backend.repositories.RepositoryManager import RepositoryManager
import docker
from docker.models.containers import Container

class BackupGenerator():
    
    def __init__(self):
        
        self.client = docker.from_env()
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
    
    def setJobs(self,container:Container):
    
        labels = container.labels
        if labels.get("dbackup.on") != "true":
            return
        
        print("=== Backup In Progress For %s ===" % container.name)
        self.manageMounts(container)
            

    def manageMounts(self,container:Container):
        
        print("=== Attributes of this container === \n",container.attrs["Mounts"])
        
        container.pause()            
        for attribute in container.attrs["Mounts"]:
                
            path=self.save(attribute.get("Source") or attribute["Name"],container.name,attribute["Destination"].replace("/","_"),attribute["Type"])
        
            asyncio.run(self.repositoryManager.uploadAll(path))
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
            raise RuntimeError(f"=== Container Failed ===")
        
        savedFilePath="/app/work"+target
        print(savedFilePath)
        if not os.path.exists(savedFilePath):
            raise RuntimeError(f"=== Backup couldn't be found after generating it {savedFilePath} ===")
        
        print(f"=== Saved {target} ===")
        return savedFilePath

    def initialScan(self):
        
        print("=== Initial scan ===")
        for c in self.client.containers.list():
            self.setJobs(c)

    def generate(self):
        
        self.setBasePath()
        os.makedirs(self.basePath, exist_ok=True)
        os.makedirs(os.path.join(self.basePath,"backups"), exist_ok=True)
        os.makedirs(os.path.join(self.basePath,"temp"), exist_ok=True)
        
        self.repositoryManager = RepositoryManager()
        asyncio.run(self.repositoryManager.instanciateAll())

        ## List, finds and selects containers with label dbackup.on=true
        ## works one time after starting
        
        self.initialScan()
            
        ## List, finds and selects containers with label dbackup.backup=true
        ## Works only if something has changed (event based)

        for event in self.client.events(decode=True):
            print("=== Checking ===")
            if event.get("Type") != "container":
                continue

            if event.get("Action") not in ("start","update"):
                continue

            containerID = event["Actor"]["ID"]

            print("=== Found Container ===")

            try:
                container = self.client.containers.get(containerID)
            except docker.errors.NotFound:
                continue

            print("=== Starting Jobs ===")
            self.setJobs(container)
        
