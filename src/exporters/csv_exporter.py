import csv

class CsvExporter:
    def export(self,rows,output_file):
        with open(output_file,"w",newline="",encoding="utf-8") as f:
            if rows:
                writer=csv.DictWriter(f,fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        return output_file
