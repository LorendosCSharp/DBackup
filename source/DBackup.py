import docker

client = docker.from_env()

def setJobs(container):
        print("=== Added Job ===")
        labels = container.labels
        if labels.get("dbackup.backup") == "true":
            print("Is backing up",container.name)

def main():

    ## List, finds and selects containers with label dbackup.backup=true
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
        container = client.containers.get(containerID)

        print("=== Starting Jobs ===")
        setJobs(container)

if __name__=="__main__":
    print("=== Started ===")
    main()