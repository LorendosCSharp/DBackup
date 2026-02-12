from source.backend.interfaces import IRepository


class TelegramRepository(IRepository):
    def upload(self,path):
        print("=== Uploading To Telegram ===")
        
        pass