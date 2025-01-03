#To install first: pip install streamlit pycountry geopy tensorflow holidays matplotlib
#To run: streamlit run user_interface.py
import pandas as pd
import streamlit as st
import os
import shutil
from fiche_pep import get_pep_co2

# Main function
def main():
    # Title with blue color
    st.markdown("<h1 style='color:#000046>Analyser une fiche PEP</h1>", unsafe_allow_html=True)
    
    # televerser un document
    st.markdown("<h3 style='color:#00768F;'>Téléverser une fiche PEP</h3>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Choisissez les documents à téléverser.",
        accept_multiple_files=True
    )

    path_list = []
    co2_eq_list = []
    # Bouton pour lancer l'opération
    if st.button("LAUNCH"):
        # Chemin du dossier de destination
        target_folder = "fiches_pep"

        # Vérifie si le dossier existe, sinon le supprimer
        if os.path.exists(target_folder):
            shutil.rmtree(target_folder)

        # Crée le dossier
        os.makedirs(target_folder)

        # Sauvegarde les fichiers téléversés dans le dossier
        if uploaded_files:
            for uploaded_file in uploaded_files:
                with open(os.path.join(target_folder, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.read())
                    file_path = os.path.join(target_folder, uploaded_file.name)
                    path_list.append(file_path)
            for path in path_list:
                co2_eq_list.append(get_pep_co2(path))
            if len(co2_eq_list) != len(path_list):
                st.warning("Les listes ne sont pas de meme taille, un fichier n'a pas été analysé !")
            data = {
                "Fichier": path_list,
                "CO2_eq": co2_eq_list
                }
            df = pd.DataFrame(data)

            # Titre dans Streamlit
            st.title("CO2 équivalent des fiches PEP")

            # Affichage du tableau dans Streamlit
            st.table(df)
            st.write(co2_eq_list)
        else:
            st.warning("Aucun fichier téléversé.")


# Run the application
if __name__ == "__main__":
    main()