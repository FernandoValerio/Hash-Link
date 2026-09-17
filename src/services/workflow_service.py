class WorkflowService:
    def __init__(self,acquisition_service,hashing,manifest,exports):
        self.acquisition_service=acquisition_service
        self.hashing=hashing
        self.manifest=manifest
        self.exports=exports

    def run(self,url:str):
        return self.acquisition_service.analyse(url)
