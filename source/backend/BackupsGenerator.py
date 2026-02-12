from datetime import datetime
import os
import tarfile
import docker



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
                if attribute["Type"]=="bind" and attribute["Destination"]=="/app/backups":
                    self.basePath=attribute["Source"]
                    
        if not self.basePath:
            raise RuntimeError("=== No valid host folder found for runner container ===")   
        
        print(f"=== BASE PATH {self.basePath} ===")
    
    def setJobs(self,container):
    
        labels = container.labels
        if labels.get("dbackup.on") != "true":
            return
        
        print("=== Backup In Progress For %s ===" % container.name)
        self.manageMounts(container)
            

    def manageMounts(self,container):
        
        print("=== Attributes of this container === \n",container.attrs["Mounts"])
        
        for attribute in container.attrs["Mounts"]:
            if attribute["Type"]=="bind":
                self.saveBind(attribute["Source"],container.name,attribute["Destination"].replace("/","-"))
            if attribute["Type"]=="volume":
                self.saveVolume(attribute["Name"],container.name)


    def saveVolume(self,volumeName, containerName):
        
        time = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        archiveName = f"{time}[=]{containerName}[=]{volumeName}[=]Volume.tar.gz"
        target = f"/backups/{archiveName}"

        print(f"=== Coping Data To {target} ===")

        self.packTar(volumeName,target)
        
        print(f"=== Saved {target} ===")
        
        
                
    def saveBind(self,path,containerName,directoryToCopy):
        
        time = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        filename= f"{time}[=]{containerName}[=]{directoryToCopy}[=]Bind.tar.gz"
        target = os.path.join("/backups",filename)
        
        print(f"=== Coping Data To {target} ===")
        
        self.packTar(path,target)
        
        print(f"=== Saved {target} ===")
        

    def packTar(self,volumeName,target):
        
        
        self.client.containers.run(
            image="alpine",
            command=f"tar czf {target} -C /data .",
            remove=True,
            volumes={
                volumeName: {"bind": "/data", "mode": "ro"},
                self.basePath: {"bind": "/backups", "mode": "rw"},
            },
        )  

    def generate(self):
        self.setBasePath()
        os.makedirs(self.basePath, exist_ok=True)

        ## List, finds and selects containers with label dbackup.on=true
        ## works one time after starting

        print("=== Initial scan ===")
        for c in self.client.containers.list():
            self.setJobs(c)
            
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
