import pyrebase
import threading
import urllib.parse
from PIL import Image
import os
from django.conf import settings


class StoreToFirebase:
    def __init__(self):
        config = {
        "apiKey": "AIzaSyAsuMuLjeRjrF21Vlsugm2SfPoEP7CvU1g",
        "authDomain": "tim-gia-su-618bf.firebaseapp.com",
        "projectId": "tim-gia-su-618bf",
        "storageBucket": "tim-gia-su-618bf.appspot.com",
        "messagingSenderId": "441000868282",
        "appId": "1:441000868282:web:a435d26997028eb48ac583",
        "measurementId": "G-4TRFC2FPX0",
        "databaseURL": "",
        }
        firebase = pyrebase.initialize_app(config)
        self.storage = firebase.storage()

    def get_url(self, file, folder):
        path = f"{folder}/{file.name}"

        # convert to .webp
        file_name_webp = file.name + ".webp"
        path_tempo_file = "tempo_image/" + file_name_webp

        img = Image.open(file).convert("RGB")
        img.save(path_tempo_file, "webp")

        # end convert

        # file_uploaded = self.storage.child(path).put(file)
        path = path + ".webp"
        file_uploaded = self.storage.child(path).put(path_tempo_file)
        os.remove(path_tempo_file)

        file_token = file_uploaded.get('downloadTokens')
        
        # file_url = self.storage.child(path).get_url(token=file_token)

        bucket = file_uploaded.get("bucket")
        path_encode = urllib.parse.quote(path, safe='')
        file_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket}/o/{path_encode}?alt=media&token={file_token}"
        return file_url
        


class UploadImage(threading.Thread):
    def __init__(self, image, folder_upload):
        self.image = image
        self.folder_upload = folder_upload
        self.storage = StoreToFirebase()
        self.url = None
        threading.Thread.__init__(self)

    def run(self):
        self.url = self.storage.get_url(self.image, self.folder_upload)