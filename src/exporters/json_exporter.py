import json

class JsonExporter:
    def export(self,data,output_file):
        with open(output_file,"w",encoding="utf-8") as f:
            json.dump(data,f,indent=2,ensure_ascii=False)
        return output_file
