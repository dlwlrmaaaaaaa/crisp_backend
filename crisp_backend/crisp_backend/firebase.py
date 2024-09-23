import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase
cred = credentials.Certificate('C:/Users/ADMIN/Documents/crisp-5d09f-firebase-adminsdk-vl4cg-30e5cb1ca3.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'crisp-5d09f.appspot.com'  # Replace with your actual bucket name
})