#To install first: pip install streamlit pycountry geopy tensorflow holidays matplotlib
#To run: streamlit run user_interface.py

import streamlit as st
from datetime import datetime
import os
import shutil

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
            st.success("OK")
            st.write("Liste des fichiers téléversés :")
            st.write(path_list)
        else:
            st.warning("Aucun fichier téléversé.")


# Run the application
if __name__ == "__main__":
    main()