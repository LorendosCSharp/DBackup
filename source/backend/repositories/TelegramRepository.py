import os
from typing import Final
import telegram
from source.backend.interfaces import IRepository
from dotenv import load_dotenv

class TelegramRepository(IRepository):
    
    def __init__(self):
        load_dotenv()
        self.token:Final=os.getenv("TELEGRAM_BOT_TOKEN")
        pass
    
    async def main(self):
        bot = telegram.Bot(self.token)
        async with bot:
            print(await bot.getMe())
    
    async def upload(self,path):
        print("=== Uploading To Telegram ===")
        
        pass
    