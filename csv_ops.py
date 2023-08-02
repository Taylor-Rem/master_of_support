import pandas as pd


class CsvOperations:
    def __init__(self):
        pass

    def get_url_columns(self, file_path):
        df = pd.read_csv(file_path)
        return df.filter(like="URL").values.flatten().tolist()
