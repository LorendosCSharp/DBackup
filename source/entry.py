from backend.BackupsGenerator import BackupGenerator

class Entry():
    
    def __init__(self):
        self.backupGenerator = BackupGenerator()
    
    def main(self):
        path=self.backupGenerator.generate()
            
if __name__=="__main__":
    entry = Entry()
    entry.main()
    
    
    

