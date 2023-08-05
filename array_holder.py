import pandas as pd
class Columns:
    def __init__(self,data_frame):
        df = pd.read_csv(data_frame, encoding='latin-1',dtype={'nconst': object, 'primaryName': object, 'birthYear': object, 'deathYear': object,'primaryProfession': object, 'knownForTitles': object})  # convert to github link later
        self.names = df['primaryName'].to_numpy()[0:20000]
        self.movies_1 = df['knownForTitles'].to_numpy()[0:20000]
        self.movies_2 = df['Unnamed: 6'].to_numpy()[0:20000]
        self.movies_3 = df['Unnamed: 7'].to_numpy()[0:20000]
        self.movies_4 = df['Unnamed: 8'].to_numpy()[0:20000]
