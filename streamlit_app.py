import requests
from bs4 import BeautifulSoup
import streamlit as st


def get_song_title(url):
    """
    Récupère le titre de la chanson depuis la balise <title> dans la page HTML.

    :param url: URL de la page contenant la chanson
    :return: Titre de la chanson ou "suno_song" si non trouvé
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.text.strip()
                # Nettoyer le titre pour extraire uniquement le nom de la chanson
                title = title.split(" by ")[0]  # Supprimer " by @username | Suno"
                return title
        return "suno_song"
    except Exception as e:
        st.error(f"Erreur lors de la récupération du titre : {e}")
        return "suno_song"


def download_audio_file(audio_url, output_path):
    """
    Télécharge un fichier audio depuis une URL.

    :param audio_url: Lien direct vers le fichier audio
    :param output_path: Chemin et nom du fichier de sortie
    :return: Le chemin du fichier téléchargé
    """
    try:
        response = requests.get(audio_url, stream=True)
        if response.status_code == 200:
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            return output_path
        else:
            st.error(f"Échec du téléchargement, code d'état : {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erreur lors du téléchargement : {e}")
        return None


# Application Streamlit
st.set_page_config(page_title="Téléchargeur Suno", layout="centered")

# Titre principal
st.title("Téléchargeur Suno")
st.write("Une application simple pour télécharger des sons publics depuis Suno. "
         "Cela vous permet d'obtenir les sons que vous aimez avec un titre personnalisé !")

# Inputs utilisateur
url = st.text_input("Entrez l'URL du son Suno :",
                    placeholder="https://suno.com/song/fc991b95-e4e9-4c8f-87e8-e5e4560755e7")
custom_title = st.text_input("Entrez un titre personnalisé (facultatif) :", placeholder="Titre personnalisé")

# Bouton pour lancer le téléchargement du son en mémoire
if st.button("Récupérer le son"):
    if url:
        # Obtenir le titre de la chanson depuis l'URL
        song_title = get_song_title(url)

        # Utiliser un titre personnalisé si fourni
        if custom_title.strip():
            song_title = custom_title.strip()

        # Nettoyer le titre pour le nom de fichier
        song_title = song_title.replace(" ", "_").replace("/", "_")
        audio_url = f"https://cdn1.suno.ai/{url.split('/')[-1]}.mp3"

        # Télécharger le fichier
        with st.spinner("Récupération en cours..."):
            downloaded_file = download_audio_file(audio_url, f"{song_title}.mp3")

        # Vérifier si le fichier a été récupéré avec succès
        if downloaded_file:
            st.success(f"Son récupéré avec succès : {downloaded_file}")
            # Permettre à l'utilisateur de télécharger le fichier
            with open(downloaded_file, "rb") as file:
                st.download_button(
                    label="Télécharger le son",
                    data=file,
                    file_name=f"{song_title}.mp3",
                    mime="audio/mpeg"
                )
    else:
        st.error("Veuillez entrer une URL valide.")

# Charger l'image
image_path = "images/tuto_lien.png"  # Remplacez par le chemin de votre image

# Page principale
st.markdown("""
# **Comment récupérer l'URL du son depuis Suno**

Pour télécharger un son public depuis **Suno** en utilisant cette application, voici comment récupérer l'URL du son :

### 1. **Accédez au lecteur audio**
- Rendez-vous sur la page du son que vous souhaitez télécharger sur **Suno**.
- Vous verrez un lecteur audio similaire à celui affiché ci-dessous :
""")

# Afficher l'image
st.image(image_path, caption="Exemple de lecteur Suno avec l'icône de partage entourée.", use_column_width=True)

st.markdown("""
### 2. **Cliquez sur l'icône de partage**
- Dans le lecteur, repérez l'icône **partage** entourée en rouge dans l'image ci-dessus.
- Cliquez dessus pour copier le lien du son.

### 3. **Utilisez l'URL dans l'application**
- Collez cette URL dans le champ prévu dans cette application, elle ressemblera à quelque chose comme :  
  `https://suno.com/song/[code_unique_du_son]`.
- Vous pourrez ensuite télécharger le fichier audio.

---

### **Remarque importante :**
Le lien généré par l'icône de partage garantit que l'application obtient le bon fichier audio. Assurez-vous de copier une URL valide pour éviter les erreurs.
""")
