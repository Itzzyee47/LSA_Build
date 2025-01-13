from datetime import datetime
from math import floor
import flet as ft
import os
import requests



def isOnline():
    # Check if device is online (simulating navigator.onLine in Python)
    response = requests.get("https://www.google.com", timeout=5)
    if response.status_code != 200:
        #page.snack_bar = ft.SnackBar(ft.Text("No internet connection!"), open=True)
        return False
    else:
        return True

# function to get conversation of a given user....
def get_conversations(page,current_user):
    
    try:
        data = {"currentUser": current_user}  # User ID to be sent along with the file
        url = "https://landmarkai.onrender.com/getConvo"
        response = requests.post(url, json=data)

        if response.ok:
            data = response.json()  # Get the JSON response
            #print(data)
            conversations = data['respons']
            
            return conversations
        
    except Exception as error:
        print(f"Error getting conversations: {error}")
        page.snack_bar = ft.SnackBar(ft.Text("Failed to get your conversations"), open=True)
        page.update()
    
    
def load_messages(conversation_id):
    try:
        # Check if conversation ID is valid
        data = {"convoID": conversation_id}  # User ID to be sent along with the file
        url = "https://landmarkai.onrender.com/getMessage"
        response = requests.post(url, json=data)

        if response.ok:
            data = response.json()  # Get the JSON response
            #print(data)
            messages = data["snapshot"]
                
            return messages  
                    # Extract message fields
                    # sender = message_data.get("sender")
                    # message = message_data.get("content")
                    # time = message_data.get("time")

        elif not data:  # If no messages found
            return []  
        
        # Assuming the chat history is an internal state and not a DOM element.
    
    except Exception as e:
        print(f"Error loading messages: {e}")
        
def create_new_conversation(current_user):
    
    print("Creating new convo...")
    data = {
        "currentUser": current_user
    }  # User ID to be sent along with the file
    url = "https://landmarkai.onrender.com/createConvo"
    response = requests.post(url, json=data)

    if response.ok:
        data = response.json()  # Get the JSON response
        conversation_id = data["snapshot"]
        
        print('New convo created sucessfully!! ', conversation_id)
        return conversation_id
    else:
        return NotImplementedError
    
def delet_conversation(convo_id):
    try:
        data = { "id": convo_id  }  # User ID to be sent along with the file
        url = "https://landmarkai.onrender.com/deleteConvo"
        response = requests.post(url, json=data)

        if response.ok:
            print(f"Deleted conversation with ID: {convo_id}")
            return True
    except Exception as error:
        print(f'The was an error deleting the conversation: {error}')
        return False
    
    
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


def uploadProfileImg(page, filePath, id):
    try:
        files = {"profilePic": open(filePath, 'rb')}  # File as 'rb' for binary mode
        data = {"id": id}  # User ID to be sent along with the file
        url = "https://landmarkai.onrender.com/updateUPictureM"
        
        
        response = requests.post(url, files=files, json=data)

        if response.ok:
            data = response.json()  # Get the JSON response
            print("File uploaded successfully!")
            #print(f"Server response: {data}")
            print(data)
            # Here you would update the user's image on the page (e.g. with a new Image component)
            download_url = data["downloadURL"]
            
            return download_url
        
    except Exception as error:
        print(f"Error uploading profile picture: {error}")
        page.snack_bar = ft.SnackBar(ft.Text("Failed to upload profile picture."), open=True)
        page.update()
    
# Function to get the current timestamp
def time_stamp():
    return int(datetime.now().timestamp())

# function to save a chat message
def save_chat_message(message, u, convo_id):
    try:
        # Prepare the data to save
        data = {
            "u": "bot" if u == "bot" else u,
            "message": message,
            "convoID": convo_id  # Assuming convo_id is passed to this function
        }
        url = "https://landmarkai.onrender.com/saveMessage"
        response = requests.post(url, json=data)

        if response.ok:
            print("Message saved....")

    except Exception as e:
        print(f"Error saving document: {e}")
        
def save_review(message,u):
    try:
        # Prepare the data to save
        data = {
            "feedback": message,
            "currentUser": u
        }

        # Add the feedbacks to the 'feedbacks' collection
        url = "https://landmarkai.onrender.com/sendFeedback"
        response = requests.post(url, data=data)

        if response.ok:
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
convoID = "SjwIJVNBY2z52G61VuEp" 
message = "What is the weather like"
#page = ft.Page
{
    "id": "SjwIJVNBY2z52G61VuEp",
    "date": "2024-12-28T10:07:32.698Z"
}
#print('Attempting to save chat')
#save_chat_message(message,current_user,convoID)
#bot_reply= send_user_message(message)
save_chat_message(message,'bot',convoID)
#create_new_conversation(current_user)
#send_user_message("hi there, how do you do")
#delet_conversation("RAKOmdW9xtGh86kdcKGw")
#delet_conversation('vO3b09QH9i9GAVkm7qMt')
#convos = get_conversations(page,current_user)
#print(f'{convos}')
#print(f'conversation of id {convoID} has messages {load_messages("eL3KCvUyjNUwrK9CgbEa")}')
# count = 0
# for convo in convos:
#     print(f'{count} {convo}')
#     count += 1
#load_messages(convoID)


def convert_timestamp(timestamp):
    # Convert time from isoformat to date in string format
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z","+00:00"))
        formatted_date = dt.strftime('%A %d, %b, %Y')
        #print(formatted_date)
        #print(f'{dt.year}-{dt.month}-{dt.day}')
        
        return formatted_date
    except Exception as er:
        print(f'The was an error: {er}')

def convert_timestamp2(timestamp):
    # Convert time from isoformat to date in string format
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z","+00:00"))
        formatted_date = dt.strftime('%A %d, %b, %Y, %H:%M')
        #print(formatted_date)
        #print(f'{dt.year}-{dt.month}-{dt.day}')
        
        return formatted_date
    except Exception as er:
        print(f'The was an error: {er}')

def convert_time(timestamp):
    #print(f'Converting from {timestamp} to time')
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z","+00:00"))
        formatted_date = dt.strftime('%H:%M')
        #print(formatted_date)
        #print(f'{dt.year}-{dt.month}-{dt.day}')
        return formatted_date
    except Exception as er:
        print(f'The was an error: {er}')
        

def currentTime():
    timeStamp = datetime.now().isoformat()
    
    # Create a datetime object from the timestamp
    dt_object = datetime.fromisoformat(timeStamp.replace("Z","+00:00"))
    
    # Format the datetime object into the desired format
    formatted_date = dt_object.strftime('%d-%m-%Y, %H:%M')
    
    return dt_object

def titleTime(timestamp):
    dt = datetime.fromisoformat(timestamp.replace("Z","+00:00"))
    formatted_date = dt.strftime('%d/%m/%Y')
    #print(formatted_date)
    #print(f'{dt.year}-{dt.month}-{dt.day}')
    
    return formatted_date

def titleTime2(timestamp):
    dt = datetime.fromisoformat(timestamp.replace("Z","+00:00"))
    formatted_date = dt.strftime('%d/%m/%Y')
    #print(formatted_date)
    #print(f'{dt.year}-{dt.month}-{dt.day}')
    
    return formatted_date
    
   #print(f'{timestamp} in readable time is: {formatted_date}')

# Example usage
#timestamp = 1673689775078
#formatted_date = 
#convert_timestamp2("2024-12-28T10:07:32.698Z")
#print(f'The time now is: {currentTime()}')
# print(f'Converting timestamp to date: {convert_timestamp(datetime.now().timestamp())}')
# print(f'Here is the title time of the current time {titleTime(datetime.now().timestamp())}')
# print(convert_time(datetime.now().timestamp()))




    