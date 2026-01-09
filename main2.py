import pandas as pd

# Nom du fichier (tel qu'il apparaît dans VS Code)
file_path = "dataset_anonymized_flight_Sheet1 (1).xlsx"

# Charger le fichier Excel
df = pd.read_excel(file_path)

# Afficher les premières lignes
print(df.head())

print('Hello Dataiku')