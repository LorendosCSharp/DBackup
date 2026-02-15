import asyncio
import os

import docker
import dotenv
from backend.BackupsGenerator import BackupGenerator

class Entry():
    
    def __init__(self):
        self.dockerClient=docker.from_env()
        self.backupGenerator = BackupGenerator(self.dockerClient)
    
    async def main(self):
        
        await self.backupGenerator.init()
        
        ## First scan, after booting the container
        
        await self.backupGenerator.scan()
        backupGeneratorTasks=[]
        ## Periodic scan
        if os.getenv("PERIODIC_SCAN","true") == "true":
            backupGeneratorTasks.append(self.timedScan())
        
        ## Scans on docker events that are start and update
        ## Uses docker client here
        
        if os.getenv("ON_EVENTS_BACKUP","false")=="true":
            backupGeneratorTasks.append(self.eventScan())
            
        await asyncio.gather(*backupGeneratorTasks)
       
    async def timedScan(self):
        while True:
            print("=== Running timed Scan ===")
            try:
                await self.backupGenerator.scan()
            except Exception as e:
                print(f"--- Error in timedScan: {e} ---")
            interval = int(os.getenv("RUN_TASK", "604800"))  # default 7 days
            await asyncio.sleep(interval)

            
    async def eventScan(self):
        loop = asyncio.get_running_loop()
        
        def event_stream():
            for event in self.dockerClient.events(decode=True):
                asyncio.run_coroutine_threadsafe(
                    self.handle_event(event),
                    loop
                )

        await asyncio.to_thread(event_stream)
        
    async def handle_event(self, event):
        print("=== Checking ===")
        if event.get("Type") != "container":
            return

        if event.get("Action") not in ("start","update"):
            return

        containerID = event["Actor"]["ID"]

        print("=== Found Container ===")

        try:
            container = self.dockerClient.containers.get(containerID)
        except docker.errors.NotFound:
            return

        print("=== Starting Jobs ===")
        await self.backupGenerator.setJobs(container)  
                         
if __name__=="__main__":
    entry = Entry()
    asyncio.run(entry.main())
    
    
    
    

