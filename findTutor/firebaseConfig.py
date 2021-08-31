import pyrebase

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
storage = firebase.storage()

def get_url(file, folder):
    try:
        path = f"{folder}/{file.name}"

        file_uploaded = storage.child(path).put(file)
        file_token = file_uploaded.get('downloadTokens')
        file_url = storage.child(path).get_url(token=file_token)
        return file_url
    except:
        return None