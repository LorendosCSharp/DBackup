import asyncio
import os
from backend.interfaces import IRepository 

class SCPRepository(IRepository.IRepository):
    
    def __init__(self):
        self.remotes=os.getenv("REMOTE_ADDRESSES","").split(",")
        pass
    
    async def upload(self,paths:list[str]):
        
        print("=== SCP Repo ===")
        
        
        print("=== Uploading ===")        
        for remote in self.remotes:
            print(f"=== Sending to {remote} ===")

            process = await asyncio.create_subprocess_exec(
                "rsync",
                "-avz",
                "-e", "ssh -i /app/ssh_key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null",
                "/app/work/temp/",
                remote,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            print(f"Return code: {process.returncode}")
            print(f"=== STDOUT: {stdout.decode()} ===")
            print(f"=== STDERR: {stderr.decode()} ===")
            
            print("=== (SCP) Sending successfully complete ===")

    async def instance(self):
        pass