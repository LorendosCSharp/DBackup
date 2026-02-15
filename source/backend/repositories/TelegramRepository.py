import os
from typing import Final
import telegram
from telegram import Bot, InputFile, InputMediaDocument
from backend.interfaces import IRepository
from dotenv import load_dotenv

class TelegramRepository(IRepository.IRepository):
    
    def __init__(self):
        load_dotenv()
        self.token:Final=os.getenv("TELEGRAM_BOT_TOKEN")
        self.bot=telegram.Bot(self.token)
        self.users=os.getenv("TELEGRAM_USER_IDS","").split(",")  
    
    async def upload(self,paths:list[str]):
        print("=== Telegram Repo ===")

        # media:InputMediaDocument=[]
        # for i,path in enumerate(paths):
        #     print(f"=== Adding file to Upload Job {path} ===")
        #     file= open(path,"rb")
        #     media.append(InputMediaDocument(file))
            
        batches=self.makeBatch(paths)

        print("=== Uploading ===")
        for user in self.users:
            print(f"=== Sending for User {user} ===")
            for i,batch in enumerate(batches):
                await self.bot.send_media_group(chat_id=user,media=batch,caption="For: "+paths[0].split("[=]")[1]+f" Batch: {i+1}")
            print("=== Sending successfully complete ===")
    
    def makeBatch(self,paths:list[str]):
        
        batches=[]
        media=[]
           
        for path in paths:
            print(f"=== Adding file to Upload Job {path} ===")
            file = open(path,"rb")
            media.append(InputMediaDocument(file))
            file.close()
                
        for i in range(0,len(paths),10):
            batches.append(media[i:i+10])
                    
        return batches
    
    async def instance(self):

        pass
        
        
    