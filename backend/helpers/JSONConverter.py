import json

class JSONConverter:
    def __init__(self):
        pass
    
    def row_to_dict(self, columns, rows):
        return {col: value for col, value in zip(columns, rows)}

    def conversion(self, columns, rows):
        results = [self.row_to_dict(columns, rows) for row in rows]
        return json.dumps(results, ensure_ascii=False)