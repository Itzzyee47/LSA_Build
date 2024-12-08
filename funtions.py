from datetime import datetime
from math import floor
import flet as ft

import pyrebase

import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from google.cloud import storage as gcs_storage
import os
import requests


# Firebase configuration details (replace with your own Firebase config)
firebase_config = {
    "apiKey": "AIzaSyC6LbV4AJAxbpBlMXtSBz77NgdgInpcl6c",
    "authDomain": "lsachatbot.firebaseapp.com",
    "databaseURL": "https://lsachatbot-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "lsachatbot",
    "storageBucket": "lsachatbot.appspot.com",
    "messagingSenderId": "817674467330",
    "appId": "1:817674467330:web:a97a4b92bc7a8258308f1b"
}

config = {
  "apiKey": "AIzaSyC6LbV4AJAxbpBlMXtSBz77NgdgInpcl6c",
  "authDomain": "lsachatbot.firebaseapp.com",
  "databaseURL": "https://lsachatbot-default-rtdb.europe-west1.firebasedatabase.app/",
  "storageBucket": "lsachatbot.appspot.com"
}


cred = credentials.Certificate("./lsaKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'lsachatbot.appspot.com'
})

bucket = storage.bucket()

# Firestore client
db = firestore.client()

def isOnline():
    # Check if device is online (simulating navigator.onLine in Python)
    response = requests.get("https://www.google.com", timeout=5)
    if response.status_code != 200:
        #page.snack_bar = ft.SnackBar(ft.Text("No internet connection!"), open=True)
        return False
    else:
        return True

# function to get conversation of a given user....
def get_conversations(current_user):
    
    try:
        # Reference to the 'conversations' collection
        conversations_ref = db.collection('conversations')
        
        # Query for documents where 'user' field is equal to 'current_user'
        query = conversations_ref.where('user', '==', current_user)
        
        # Fetching the documents
        docs = query.stream()

        conversations = []
        for doc in docs:
            conversations.append([doc.id,doc.to_dict()])  # Convert each document to a dictionary

        # Example of using a loader in Python CLI
        print("Loading conversations...")

        # Return or print the conversations
        return conversations
    
    except Exception as e:
        print(f"Error fetching conversations:  {str(e)}")
        return []
    
    
def load_messages(conversation_id):
    try:
        # Check if conversation ID is valid
        if not conversation_id:
            print(f"Invalid conversation ID: {conversation_id}")
            return ReferenceError

        # Query Firestore for messages with the given conversation ID and order by time
        messages_ref = db.collection('messages')
        query = messages_ref.where('convoId', '==', conversation_id).order_by('time', "ASCENDING")
        
        # Execute the query
        docs = query.get()
        messages = []

        if docs:
            # Process the query results
            for doc in docs:
                #print(doc)
                message_data = doc.to_dict()
                #print([message_data])  # Log or process each message
                messages.append(message_data)
            
            return messages  
                # Extract message fields
                # sender = message_data.get("sender")
                # message = message_data.get("content")
                # time = message_data.get("time")

        elif not docs:  # If no messages found
            return []  
        
        # Assuming the chat history is an internal state and not a DOM element.
    
    except Exception as e:
        print(f"Error loading messages: {str(e)}")
        
def create_new_conversation(current_user,time):
    
    print("Creating new convo...")

    # Add a new document to the "conversations" collection
    db.collection("conversations").add({
        "user": current_user,
        "time": time
    })

    # Query the "conversations" collection for the newly created document
    query_snapshot = db.collection("conversations").where("time", "==", time).get()
    doc = query_snapshot[0] if query_snapshot else None

    if doc:
        conversation_id = doc.id
        print('New convo created sucessfully!! ', conversation_id)
        return conversation_id
    else:
        return NotImplementedError
    
def delet_conversation(convo_id):
    try:
        convo_ref = db.collection("conversations").document(convo_id).delete()
        print(f'Convo of id {convo_id} was deleted sucesfully!!')
        messages_ref = db.collection("messages")
        messages_query = messages_ref.where("convoId", "==", convo_id)
        messages = messages_query.get()

        # Delete each message
        for message in messages:
            message.reference.delete()
            #print(f"Deleted message with ID: {message.id}")
    except Exception as error:
        print(f'The was an error deleting the conversation: {error}')
    
    
def send_user_message(user_message):
    try:
        print('Sending message.... \n',user_message)
        
        server_response = requests.post(
            "https://genzylla.onrender.com/getResponds",  # Endpoint for chatbot
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"message": user_message}
        )
        if server_response.status_code == 200:
            data = server_response.json()
            model_response = data.get("answer")
            print( "bot: ", model_response)
            # Add the model's response to the chat 
            return model_response
        else:
            return False
    except Exception as error:
        print(error)
        return False


def upload_profile_image(page, file_path, Useremail):
    try:
        # Get the current user (assuming you have a way to identify the current user)
        user = auth.get_user_by_email(Useremail)  # Replace with method to get current user
        user_id = user.uid
        print(f'The users id: {user_id}')

        # Define the storage path for the profile picture in Firebase
        file_name = os.path.basename(file_path)
        blob = bucket.blob(f"profilePictures/{user_id}/propic")

        # Upload the file to Firebase Storage
        blob.upload_from_filename(file_path)
        print(f"Profile picture uploaded successfully: {file_path}")

        blob.make_public()
        # Get the download URL of the uploaded profile picture
        download_url = blob.public_url
        
        print(f"Profile updated with new photo URL: {download_url}")

        # Notify the user of success
        page.snack_bar = ft.SnackBar(ft.Text("Profile picture updated successfully!"), open=True)
        page.update()
        
        return download_url

        # Optionally update the user's profile with the new photoURL
        #auth.update_user(user_id, photo_url=download_url)
        

    except Exception as e:
        print(f"Error uploading profile picture: {e}")
        page.snack_bar = ft.SnackBar(ft.Text("Failed to upload profile picture."), open=True)
        page.update()

def uploadProfileImg(page, filePath, id):
    try:
        files = {'profilePic': open(filePath, 'rb')}  # File as 'rb' for binary mode
        data = {'userId': id}  # User ID to be sent along with the file
        url = "https://genzylla.onrender.com/updateUPictureM"
        
        
        response = requests.post(url, files=files, data=data)

        if response.ok:
            data = response.json()  # Get the JSON response
            print("File uploaded successfully!")
            #print(f"Server response: {data}")
            print(data)
            # Here you would update the user's image on the page (e.g. with a new Image component)
            download_url = data['downloadURL']
            
            return download_url
        
    except Exception as error:
        print(f"Error uploading profile picture: {error}")
        page.snack_bar = ft.SnackBar(ft.Text("Failed to upload profile picture."), open=True)
        page.update()
    
# Function to get the current timestamp
def time_stamp():
    return int(datetime.now().timestamp())

# function to save a chat message
def save_chat_message(message, u, convo_id,time):
    try:
        # Prepare the data to save
        data = {
            "sender": 'bot' if u == 'bot' else u,
            "content": message,
            "convoId": convo_id,  # Assuming convo_id is passed to this function
            "time": time
        }

        # Add the message to the 'messages' collection
        db.collection("messages").add(data)

        # Simulate chat scrolling to bottom (just for demonstration)
        print("Message saved....")

    except Exception as e:
        print(f"Error saving document: {e}")
        
def save_review(message,u):
    try:
        # Prepare the data to save
        data = {
            "feedback": message,
            "time": str(floor(datetime.now().timestamp())),
            "user": u
        }

        # Add the feedbacks to the 'feedbacks' collection
        db.collection("feedbacks").add(data)

        print("Review saved....")

    except Exception as e:
        print(f"Error saving document: {e}")



# Collection name = feedbacks
# feedback
# "good app, very functional."
# (string)


# time
# "1723643947274"
# (string)


# user
# "test6@gmail.com"
'bnpniyBLwmQsNZ5FMxR8' 'vO3b09QH9i9GAVkm7qMt'

current_user = "test6@gmail.com"
convoID = "vO3b09QH9i9GAVkm7qMt"
message = "What is the weather like"
#save_chat_message(message,current_user,convoID)
#bot_reply= send_user_message(message)
#save_chat_message(bot_reply,'bot',convoID)
#create_new_conversation(current_user)
#delet_conversation('bnpniyBLwmQsNZ5FMxR8')
#delet_conversation('vO3b09QH9i9GAVkm7qMt')
#convos = get_conversations(current_user)
#print(f'{convos}')
#print(f'conversation of id {convoID} has messages {load_messages("eL3KCvUyjNUwrK9CgbEa")}')
# count = 0
# for convo in convos:
#     print(f'{count} {convo}')
#     count += 1
#load_messages(convoID)


def convert_timestamp(timestamp):
    # Convert milliseconds to seconds
    timestamp_seconds = timestamp / 1000
    
    # Create a datetime object from the timestamp
    dt_object = datetime.fromtimestamp(timestamp_seconds,)
    
    # Format the datetime object into the desired format
    formatted_date = dt_object.strftime('%A %d, %b, %Y, %H:%M')
    
    return formatted_date

def convert_timestamp2(timestamp):
    # Convert milliseconds to seconds
    if len(timestamp) <= 10:
        # Create a datetime object from the timestamp
        dt_object = datetime.fromtimestamp(int(timestamp),)
        
        # Format the datetime object into the desired format
        formatted_date = dt_object.strftime('%A %d, %b, %Y, %H:%M')
        
        return formatted_date
    elif len(timestamp) > 10:
        timestamp = int(timestamp)
        timestamp_seconds = timestamp / 1000
    
        # Create a datetime object from the timestamp
        dt_object = datetime.fromtimestamp(timestamp_seconds,)
        
        # Format the datetime object into the desired format
        formatted_date = dt_object.strftime('%A %d, %b, %Y, %H:%M')
        
        return formatted_date

def convert_time(timestamp):
    #print(f'Converting from {timestamp} to time')
    try:
        if len(timestamp) <= 10:
            # Create a datetime object from the timestamp
            dt_object = datetime.fromtimestamp(int(timestamp),)
            
            # Format the datetime object into the desired format
            formatted_date = dt_object.strftime('%H:%M')
            
            return formatted_date
        elif len(timestamp) > 10:
            
            timestamp = int(timestamp)
            timestamp_seconds = timestamp / 1000
        
            # Create a datetime object from the timestamp
            dt_object = datetime.fromtimestamp(int(timestamp_seconds),)
            
            # Format the datetime object into the desired format
            formatted_date = dt_object.strftime('%H:%M')
            
            return formatted_date
    except Exception as er:
        print(f'The was an error: {er}')
        

def currentTime():
    timeStamp = datetime.now().timestamp()
    
    # Create a datetime object from the timestamp
    dt_object = datetime.fromtimestamp(timeStamp,)
    
    # Format the datetime object into the desired format
    formatted_date = dt_object.strftime('%A %d, %b, %Y, %H:%M')
    
    return formatted_date

def titleTime(timestamp):
    if len(timestamp) <= 10:
        # Create a datetime object from the timestamp
        dt_object = datetime.fromtimestamp(int(timestamp),)
        
        # Format the datetime object into the desired format
        formatted_date = dt_object.strftime('%d/%m/%Y')
        
        return formatted_date
    elif len(timestamp) > 10:
        timestamp = int(timestamp)
        timestamp_seconds = timestamp / 1000

        # Create a datetime object from the timestamp
        dt_object = datetime.fromtimestamp(timestamp_seconds,)
        
        # Format the datetime object into the desired format
        formatted_date = dt_object.strftime('%d/%m/%Y')

        return formatted_date

def titleTime2(timestamp):
    # Convert milliseconds to seconds
    
    # Create a datetime object from the timestamp
    dt_object = datetime.fromtimestamp(timestamp,)
    
    # Format the datetime object into the desired format
    formatted_date = dt_object.strftime('%d/%m/%Y')
    
    return formatted_date
    
   #print(f'{timestamp} in readable time is: {formatted_date}')

# Example usage
#timestamp = 1673689775078
#formatted_date = convert_timestamp(timestamp)
# print(f'The time now is: {currentTime()}')
# print(f'Converting timestamp to date: {convert_timestamp(datetime.now().timestamp())}')
# print(f'Here is the title time of the current time {titleTime(datetime.now().timestamp())}')
# print(convert_time(datetime.now().timestamp()))

def pyre():
    pass
    # Initialize Firebase
    # firebase = pyrebase.initialize_app(config)
    # auth = firebase.auth()


                
    # def signUpUser(username,email,password):
    #     username = username
    #     email = email
    #     password = password
    #     try:
    #         # Sign in with Firebase
    #         user = auth.create_user_with_email_and_password(email, password)
            
    #         # Show success message or navigate to another page
    #         return user
    #     except Exception as error:
    #         return f'No user {error}'

    # def current():
    #     return auth.current_user


    # def signOut():
    #     pass

    # def currentUserData(user):
    #         data = auth.get_account_info(user['idToken'])
    #         return data
    # def updateUserName(id,name):
    #     try:
    #         auth.update_profile(id_token=id,display_name=name)
    #     except Exception as error:
    #         print(error)

    # def signInUser(email,password):
    #     email = email
    #     password = password
    #     try:
    #         # Sign in with Firebase
    #         user = auth.sign_in_with_email_and_password(email, password)
            
    #         # Show success message or navigate to another page
    #         return auth.current_user
    #     except Exception as error:
    #         print(error)
    #         return None
   
            


    