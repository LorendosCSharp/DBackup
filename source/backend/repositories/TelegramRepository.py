import os
from typing import Final
import telegram
from telegram import Bot
from backend.interfaces import IRepository
from dotenv import load_dotenv

class TelegramRepository(IRepository.IRepository):
    
    def __init__(self):
        load_dotenv()
        self.token:Final=os.getenv("TELEGRAM_BOT_TOKEN")
        self.bot=telegram.Bot(self.token)
    
    async def upload(self,path):
        print("=== Uploading To Telegram ===")

        async with self.bot:
            print(await self.bot.get_me())
    
    async def instance(self):

        pass
        
        
    