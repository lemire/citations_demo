import pandas as pd
import sqlite3
import os

def extract_columns_from_excel(file_path, sheet_name='Data'):
    try:
        # Lire le fichier Excel
        xls = pd.ExcelFile(file_path)

        # Afficher les feuilles disponibles
        print("Feuilles disponibles dans le fichier Excel :")
        print(xls.sheet_names)

        # Charger la feuille spécifiée
        df = xls.parse(sheet_name)

        # Afficher les colonnes disponibles
        print("Colonnes disponibles dans la feuille :")
        print(df.columns)

        # Liste des colonnes à extraire
        columns_to_extract = ['authfull', 'inst_name', 'cntry', 'firstyr', 'lastyr', 'rank (ns)']

        # Vérifier si toutes les colonnes demandées existent
        missing_columns = [col for col in columns_to_extract if col not in df.columns]
        if missing_columns:
            print(f"Colonnes manquantes dans le fichier Excel : {missing_columns}")
            return None

        # Extraire les colonnes spécifiées
        extracted_df = df[columns_to_extract]

        # Sauvegarder le résultat dans un nouveau fichier Excel
        output_file = 'extracted_columns.csv'
        extracted_df.to_csv(output_file, index=False)
        print(f"Colonnes extraites et sauvegardées dans {output_file}")

        return extracted_df

    except FileNotFoundError:
        print(f"Le fichier {file_path} n'a pas été trouvé.")
        return None
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return None

# Exemple d'utilisation
file_path = 'Table_1_Authors_career_2023_pubs_since_1788_wopp_extracted_202408.xlsx'  # Remplacer par le chemin de votre fichier Excel
extracted_data = extract_columns_from_excel(file_path)

# Afficher un aperçu des données extraites (si elles existent)
if extracted_data is not None:
    print("\nAperçu des données extraites :")
    print(extracted_data.head())

# Chemins
csv_path = os.path.join(os.path.dirname(__file__), '../data/stanford_ranking_2025.csv')
db_path = os.path.join(os.path.dirname(__file__), '../data/stanford_ranking_2025.db')

def main():
    # Lire le CSV
    df = pd.read_csv(csv_path)
    # Enregistrer dans SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql('stanford_ranking_2025', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Base de données créée : {db_path}")

if __name__ == "__main__":
    main()
