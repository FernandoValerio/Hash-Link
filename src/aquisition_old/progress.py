class DownloadProgress:
    def __init__(self,total:int=0):
        self.total=total
        self.received=0

    def update(self,size:int)->None:
        self.received+=size
