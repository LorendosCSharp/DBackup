from datetime import datetime
import os
import tarfile
import docker

client = docker.from_env()
basePath="/home/lorendos/Projects/Docker Backup/backups"
## All those print statments were writen by me. I like to see info about everything. Bleh >:3

def setJobs(container):
    
        labels = container.labels
        if labels.get("dbackup.on") != "true":
            return
        
        print("=== Backup In Progress For %s ===" % container.name)
        manageMounts(container)
            

def manageMounts(container):
    
    print("=== Attributes of this container === \n",container.attrs["Mounts"])
    
    for attribute in container.attrs["Mounts"]:
        if attribute["Type"]=="bind":
            saveBind(attribute["Source"],container.name,attribute["Destination"].replace("/","-"))
        if attribute["Type"]=="volume":
            saveVolume(attribute["Name"],container.name)


def saveVolume(volumeName, containerName):
    
    time = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    archiveName = f"{time}[=]{containerName}[=]{volumeName}[=]Volume.tar.gz"
    target = f"/backups/{archiveName}"

    print(f"=== Coping Data To {target} ===")

    packTar(volumeName,target)
    
    print(f"=== Saved {target} ===")
    
       
            
def saveBind(path,containerName,directoryToCopy):
    
    time = datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    filename= f"{time}[=]{containerName}[=]{directoryToCopy}[=]Bind.tar.gz"
    target = os.path.join("/backups",filename)
    
    print(f"=== Coping Data To {target} ===")
    
    packTar(path,target)
    
    print(f"=== Saved {target} ===")
    

def packTar(volumeName,target):
    client.containers.run(
        image="alpine",
        command=f"tar czf {target} -C /data .",
        remove=True,
        volumes={
            volumeName: {"bind": "/data", "mode": "ro"},
            basePath: {"bind": "/backups", "mode": "rw"},
        },
    )  
def main():

    os.makedirs(basePath, exist_ok=True)

    ## List, finds and selects containers with label dbackup.on=true
    ## works one time after starting

    print("=== Initial scan ===")
    for c in client.containers.list():
        setJobs(c)
        
    ## List, finds and selects containers with label dbackup.backup=true
    ## Works only if something has changed (event based)

    for event in client.events(decode=True):
        print("=== Checking ===")
        if event.get("Type") != "container":
            continue

        if event.get("Action") not in ("start","update"):
            continue

        containerID = event["Actor"]["ID"]

        print("=== Found Container ===")

        try:
            container = client.containers.get(containerID)
        except docker.errors.NotFound:
            continue

        print("=== Starting Jobs ===")
        setJobs(container)

if __name__=="__main__":
    
    print("=== Started ===")
    main()