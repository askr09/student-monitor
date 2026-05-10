import urllib.request
import os

GITHUB_URL = 'https://raw.githubusercontent.com/askr09/slow-learner-/refs/heads/main/combined_student_data.csv'

os.makedirs('data', exist_ok=True)
print('Downloading dataset...')
urllib.request.urlretrieve(GITHUB_URL, 'data/students.csv')
print('Downloaded!')

import pandas as pd
df = pd.read_csv('data/students.csv')
print(df.shape)
print(df.head())