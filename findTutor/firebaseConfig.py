import pyrebase
import threading


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
        try:
            path = f"{folder}/{file.name}"

            file_uploaded = self.storage.child(path).put(file)
            file_token = file_uploaded.get('downloadTokens')
            file_url = self.storage.child(path).get_url(token=file_token)
            return file_url
        except:
            return None


class UploadImage(threading.Thread):
    def __init__(self, image, folder_upload):
        self.image = image
        self.folder_upload = folder_upload
        self.storage = StoreToFirebase()
        self.url = None
        threading.Thread.__init__(self)

    def run(self):
        self.url = self.storage.get_url(self.image, self.folder_upload)