from datetime import datetime
import os
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
        
        for attribute in container.attrs["Mounts"]:
            container.pause()            
                
            self.save(attribute.get("Source") or attribute["Name"],container.name,attribute["Destination"].replace("/","_"),attribute["Type"])
                
            container.unpause()        

    def save(self, path:str, containerName:str, destinationPath:str, dataTime:str):
        
        time = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        filename= f"{time}[=]{containerName}[=]{destinationPath}[=]Bind.tar.gz"
        target = os.path.join("/temp",filename)
        
        print(f"=== Coping Data To {target} ===")
        
        savePath=os.path.join(self.basePath,"temp")
        
        self.client.containers.run(
            image="alpine",
            command=f"tar czf {target} -C /data .",
            remove=True,
            volumes={
                path: {"bind": "/data", "mode": "ro"},
                savePath: {"bind": "/temp", "mode": "rw"},
            }
        )  
        
        print(f"=== Saved {target} ===")

    def initialScan(self):
        
        print("=== Initial scan ===")
        for c in self.client.containers.list():
            self.setJobs(c)

    def generate(self):
        
        self.setBasePath()
        os.makedirs(self.basePath, exist_ok=True)
        os.makedirs(os.path.join(self.basePath,"backups"), exist_ok=True)
        os.makedirs(os.path.join(self.basePath,"temp"), exist_ok=True)
        

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
        
