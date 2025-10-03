from google.cloud import storage

def upload_image_to_gcs(file, filename):
    # Authentification avec la clé JSON
    client = storage.Client.from_service_account_json('credentials/gestion-image.json')
    
    # Remplace par le nom exact du bucket de ton prof
    bucket = client.get_bucket('***************')
    
    blob = bucket.blob(filename)
    blob.upload_from_file(file)  # file = open('image.png', 'rb') ou fichier d'un formulaire
    
    # Retourne l'URL publique
    return blob.public_url
