class WorkflowController:
    def __init__(self, workflow_service):
        self.workflow_service=workflow_service

    def analyse_url(self,url):
        return self.workflow_service.run(url)
