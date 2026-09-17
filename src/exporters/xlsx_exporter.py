from openpyxl import Workbook

class XlsxExporter:
    def export(self,rows,output_file):
        wb=Workbook()
        ws=wb.active
        if rows:
            ws.append(list(rows[0].keys()))
            for row in rows:
                ws.append(list(row.values()))
        wb.save(output_file)
        return output_file
