from datetime import datetime
from math import floor
import os, json
from time import sleep
from types import NoneType
import pyrebase
import flet as ft
from threading import Thread
from start_controls import start_controls,set_auto_signin

from funtions import convert_time, convert_timestamp, convert_timestamp2, create_new_conversation, currentTime, delet_conversation, get_conversations, load_messages, save_chat_message, save_review, send_user_message, titleTime, time_stamp, titleTime2, upload_profile_image, uploadProfileImg

current_page_num = 0



# Firebase configuration details (replace with your own Firebase config)
firebase_config = {
    "apiKey": "AIzaSyC6LbV4AJAxbpBlMXtSBz77NgdgInpcl6c",
    "authDomain": "lsachatbot.firebaseapp.com",
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

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()




def signUpUser(username,email,password):
    username = username
    email = email
    password = password
    try:
        # Sign in with Firebase
        user = auth.create_user_with_email_and_password(email, password)
        auth.update_profile(user['id_token'],display_name=username)
        # Show success message or navigate to another page
        return user
    except Exception as error:
        return f'No user {error}'

def current():
    u = auth.current_user
    return u


def signOut(page):
    print('Signing the current user out!!!')
    auth.current_user = None
    page.client_storage.remove("users_credentials")
    page.go('/auth')

def currentUserData(user):
        data = auth.get_account_info(user['idToken'])
        return data
    

def signInUser(email,password):
    email = email
    password = password
    try:
        # Sign in with Firebase
        user = auth.sign_in_with_email_and_password(email, password)
        
        # Show success message or navigate to another page
        #print(user)
        return auth.current_user
    except Exception as error:
        print(error)
        return error
    
def getCurrentUserImg():
    theUser = current()
    if theUser:
        if 'profilePicture' not in theUser:
            img = 'assets/avatar.png'
            return img
            
        else:
            img = f'{theUser['profilePicture']}'
            return img
    else:
        img = 'assets/avatar.png'
        return img

def main(page: ft.Page):
    page.title = 'LSA_Chatbot'
    page.window.always_on_top = True
    page.window.width = 330
    page.window.height = 670    
    page.window.max_height = 670 
    page.theme_mode = ft.ThemeMode.DARK 
    
    
    page.fonts = {
        "billa bong": "assets/fonts/Billabong.ttf"
    }
    
    current_page = ft.Container(
        expand=1,
    )

    with open("content.json") as json_file:   
        data = json.load(json_file)
        
    def set_content(value):
        global current_page_num
        current_page.content= ft.Column(
            [
                ft.Text(value=data[f'content{current_page_num+1}'][0],size=15,weight=ft.FontWeight.W_300),
                ft.Container(
                        content=ft.Image('assets/onbording1.png')
                    ),
                ft.Text(value=data[f'content{current_page_num+1}'][1],
                        text_align=ft.TextAlign.CENTER,size=28,
                        font_family= "billa bong",
                        weight=ft.FontWeight.W_800)
            ],alignment = ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,expand=1
        )
        
        page.update()
        
    set_content(current_page_num)
    
    def skip():
        global current_page_num
        current_page_num = 3 
        
        if current_page_num > 0:
            backBtn.visible = True
            if current_page_num > 2:
                nextBtn.text = 'Get started'
                nextBtn.on_click = lambda e: page.go('/auth')
                
        set_content(current_page_num)
        #print(current_page_num)
        page.update()
    
    def back(e):
        global current_page_num
        if current_page_num != 0:
            current_page_num -= 1 
            if current_page_num == 2:
                nextBtn.text = 'Next'
                nextBtn.on_click = lambda e: next(e)
            elif current_page_num == 0:
                backBtn.visible = False
            
                
        set_content(current_page_num)
        #print(current_page_num)
        page.update()
    
    def next(e):
        global current_page_num
        current_page_num += 1 
        
        if current_page_num > 0:
            backBtn.visible = True
            if current_page_num > 2:
                nextBtn.text = 'Get started'
                nextBtn.on_click = lambda e: page.go('/auth')
        else:
            backBtn.visible = False
            
            
        set_content(current_page_num)
        #print(current_page_num)
        page.update()
    
    #print(data["content1"][0])
    #print(data)
    # Components....
    skipBtn = ft.TextButton(
            'Skip',on_click= lambda _: skip(),
        )
    
    backBtn = ft.ElevatedButton("Back!", on_click= lambda e: back(e))
    nextBtn = ft.ElevatedButton("Next!", on_click=lambda e: next(e))
    backBtn.visible = False
    
    bottom_nav = ft.Container(
        content=ft.Row(
            [
                backBtn,nextBtn,
            ],alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),expand=1
    )
    
    
    onboard = ft.SafeArea(
        content=ft.Container(
            content= ft.Column(
                [
                    ft.Container(
                        content=ft.Stack(
                            [
                                current_page,skipBtn
                            ]    
                        ),
                        expand=9,
                    ),
                    bottom_nav
                ]
            ),
            image_src='assets/aiAppBg3.jpg', bgcolor=ft.colors.with_opacity(0.1,'purple'),
            image_fit=ft.ImageFit.COVER,image_opacity=0.1,
        ),expand=True
    )
    
    
    # Global data about the current user....
    User = None 
    theUser = current()
    # User data is stored in session as userData, userName, userEmail
    u = theUser['displayName'] if theUser != None else 'Username'
    e =  theUser['email'] if theUser != None else 'email'
    img = getCurrentUserImg()
    
    
    try:
        Username = page.client_storage.get("userName")
        Useremail = page.client_storage.get("email")
        UserImage = page.client_storage.get("img")
    except Exception as er:
        pass
    
    print('This is the current user')
    print(u, e)
    def view_pop(view):    
        if page.route != '/home':
            page.go('/home')
            #pass
        top_view = page.views[-1]
        page.go(top_view.route)
        page.update()
     
    #PAGE COMPONENTS..............
    def alert(e,value):
        dlg = ft.AlertDialog(
            title=ft.Text(value=value,size=15,color='red',text_align=ft.TextAlign.CENTER)
            )
        e.page.dialog = dlg # type: ignore
        dlg.open = True
        e.page.update() # type: ignore
        
    loader = ft.AlertDialog(
        modal=True,
        title=ft.Text(value='One moment please...',size=15,color='blue',text_align=ft.TextAlign.CENTER,weight=ft.FontWeight.W_700),
        content=ft.Container(
            height=50,
            content=ft.Column(
                [ft.ProgressRing(color='white')],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ), 
        bgcolor= ft.colors.with_opacity(0.3,'black')
    )   
    
    def loading(e):
        page.dialog = loader # type: ignore
        loader.open = True
        page.update() # type: ignore
        
    def end_loading(e):
        page.close(loader)
        page.update()

    # .lfakeljrn f;kjae;raemf
    def close_dlg(dlgName):
        page.close(dlgName)
        page.update()
        
    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()
            
    def refreshPage():
        global auth
        global  img
        theUser = current() 
       
        
        if theUser == None:
            editUnameDlg.content.content.controls[0].value = 'displayName' 
            uNameInput.value = 'displayName'
            uEmailInput.value = 'email' 
            appBarImg.image_src , profileCardImg.image_src = 'assets/avatar.png' ,'assets/avatar.png' 
            welcomeMessage.value = f'welcome, Username \nwhat would you like me to assist you with today'
        else:
            user = auth.get_account_info(theUser['idToken'])
            #print(user)
            #print(user['users'][0]['displayName'])
            editUnameDlg.content.content.controls[0].value = theUser['displayName'] 
            uNameInput.value = user['users'][0]['displayName']
            uEmailInput.value = theUser['email'] 
            appBarImg.image_src , profileCardImg.image_src = img ,img 
            welcomeMessage.value = f'welcome, {theUser['displayName']} \nwhat would you like me to assist you with today'
            getChats()
       
        page.update()
        #print(f'The current user: {current()}')
    
    
    def resetPassword(e):
        global auth
        emailValue = signIn.content.controls[0].value
        
        if emailValue == "":
            alert(e,'Please enter the email to send the reset password link!')
        else:
            loading(e)
            auth.send_password_reset_email(emailValue)
            end_loading(e)
            alert(e,f'Check your email {emailValue} for the reset password link')
            
    def setUserData():
        #User = page.client_storage.get("userData")
        #Udata = currentUserData(User)
        #page.client_storage.set("userName", name)
        global theUser,Username, Useremail, UserImage

        # User data is stored in session as userData, serName, userEmail
        global u , e, img
        theUser = current() 
        #print(theUser)
        # User data is stored in session as userData, serName, userEmail
        u = theUser['displayName'] if theUser != None else 'Username'
        e =  theUser['email'] if theUser != None else 'email'
        if theUser:
            if 'profilePicture' not in theUser:
                img = 'assets/avatar.png'
                
            else:
                img = theUser['profilePicture']
        page.client_storage.set("userName", u)
        page.client_storage.set("email", e)
        page.client_storage.set("img", img)
        
        Username = u
        Useremail = page.client_storage.get("email")
        UserImage = page.client_storage.get("img")
        
        
        print('The current user: ')
        print(theUser['email']) 
        #print(name, email, Udata)
        page.update()
        
    def clearFormValues(form):
        count = 0
        for i in form.content.controls:
            form.content.controls[count].value = ''
            count += 1
        
    
    def validateSignUp(e):
        global User
        
        name = signUpForm.content.controls[0].value
        email = signUpForm.content.controls[1].value
        password1 = signUpForm.content.controls[2].value
        password2 = signUpForm.content.controls[3].value
        terms = Accept_terms.value
        
        def passwordMatch(): 
            if len(password1) != 0:
                if password1 == password2:
                    return True
            else:
                return False
        
        if name and email: 
            if not passwordMatch():
                alert(e,'Passwords do not match!')
            else:
                if terms != True:
                    alert(e,'You must accept the terms and conditions')
                    
                else:
                    try:
                        alert(e,'Attempting to signUp...')
                        User = signUpUser(name,email,password1)
                        page.client_storage.set("userData", User)
                        page.dialog = None
                        #print(User)
                        set_auto_signin(page,email,password1)
                        sleep(2)
                        setUserData()
                        refreshPage()
                        
                        #getChats()
                        clearFormValues(signUpForm)
                        # Redirect to login
                        page.go('/auth2')
                    except Exception as error:
                        #pass
                        alert(e,f'There was an error siging Up please check your intenet connection!{error}')
                        print(error, User['error'])
                    
        else:
            alert(e,'Please fill all the required fields!!')
            
    def auto_signin():
        try:
            user = page.client_storage.contains_key("users_credentials")
        
            if user:
                credentials = page.client_storage.get("users_credentials")
                email = credentials[0]
                password = credentials[1]
            
                try:
                    User = signInUser(email,password)
                    page.client_storage.set("userData", User)
                    # Set auto sign in variables
                    setUserData() 
                    refreshPage()
                    #page.update()
                    sleep(1)
                    getChats()
                    #
                    page.go('/home')
                except Exception as error:
                    pass
            else:
                pass
        except Exception as er:
            pass
    
    def signin(e):
        global User
        
        email = signIn.content.controls[0].value
        password = signIn.content.controls[1].value
        if password == "" or email == "":
            alert(e,'Please fill all the required fields!')
            
        else:
            try:
                alert(e,'Attempting to signIn...')
                User = signInUser(email,password)
                page.client_storage.set("userData", User)
                page.client_storage.set("pass", password)
                # Set auto sign in variables
                set_auto_signin(page,email,password)
                setUserData() 
                refreshPage()
                #page.update()
                clearFormValues(signIn)
                sleep(2)
                getChats()
                #
                page.go('/home')
            except Exception as error:
                alert(e,f'There was an error siging In Please check your internet connection!{error}')
                print(error)

    editUnameDlg = ft.AlertDialog(
        
            modal=True, title=ft.Text('Edit user name',color='purple',weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                [
                    ft.TextField(value=Username,label='User name',border=ft.InputBorder.UNDERLINE),  
                ]),
                height=80
            )
            ,actions=[
                        ft.ElevatedButton('Save', on_click= lambda e: updateUserName()),
                        ft.ElevatedButton('Cancel',on_click= lambda e: close_dlg(editUnameDlg))
                    ]
            )

    def editUserName():
        
        page.open(editUnameDlg)# type: ignore
        
    def updateUserName():
        global auth, u
        try:
            user = current()
            id = user['idToken']
            name = editUnameDlg.content.content.controls[0].value
            close_dlg(editUnameDlg)
            loading(e)
            #print(name, id)
            try:
                auth.update_profile(id,display_name=name)
                sleep(2)
                end_loading(e)
                setUserData()
                refreshPage()
                
            except Exception as error:
                end_loading(e)
                alert(e,'The was an error updating your user name, check your network anad try again!')
                print(error)
        except Exception as error:
           
            print(error)
            return error
    
            
    appBarImg = ft.Container(
        height=40,width=35,
        bgcolor=ft.colors.WHITE,
        image_src=f'{UserImage}',
        image_fit= ft.ImageFit.COVER,
        border_radius=ft.border_radius.all(50),
        margin=ft.margin.all(10),
        on_click= lambda _: page.go('/profile')
    )
    
    appbar1 = ft.AppBar(
       title=ft.Text('Conversations',weight=ft.FontWeight.W_800),
       bgcolor='purple',
        actions=[
            appBarImg
        ]         
    )
    
    review_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text('Leave a review'),
        content=ft.Container(height=60,content=ft.TextField(multiline=True),padding=1),
        actions=[
            ft.TextButton("Submit", on_click= lambda _: submitReview()),
            ft.TextButton("Cancel", on_click= lambda e: close_dlg(review_dlg)),
        ]
    )
    
    conversationDate = ft.Text('18/09/2024',size=10,color='grey')
    
    currentConversation = ''
    
    appbar2 = ft.AppBar(
        title=ft.Container(
            content=ft.Column(
                    [
                        ft.Text('Zylla',weight=ft.FontWeight.W_600,size=25),
                        conversationDate
                    ],alignment=ft.MainAxisAlignment.CENTER,spacing=2
                ),on_click= lambda _: print('clicked')
            ),
        bgcolor='purple',
        leading=ft.IconButton( 
            icon=ft.icons.ARROW_BACK,
            on_click= lambda e: goHome(e)
            ),
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="About Zylla"),
                    ft.PopupMenuItem(text='Leave a review', on_click= lambda _: review())
                ],
                menu_position= ft.PopupMenuPosition.UNDER
            ),
        ]      
    )
    
    profileAppbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click= lambda _: page.go('/home')  
            ),
        title=ft.Text('Profile'),
        bgcolor='purple',
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Restart",on_click=lambda _:print("page.go('/')")),
                    ft.PopupMenuItem(text="Refresh",on_click=lambda _: refreshPage()),
                ],
                menu_position= ft.PopupMenuPosition.UNDER
            ),
        ]
    )
    
    messageBubble = ft.Row(
        [
            ft.Container(
                content=ft.Column( 
                    [
                        ft.Text('Hello oawibdaoiwbodaiw doawidbnoaiwbndoaibw doaiwndoiabwodba owdainbwoidbaow doaiwnbdoiwdoa owdinaowdbi aowidb',width=250,size=11,weight=ft.FontWeight.W_600,no_wrap=False),
                        ft.Row(
                            [
                                ft.Text('6:44 pm',size=8,color='white'),
                               
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ]
                ),bgcolor=ft.colors.with_opacity(0.7,'black')
                ,blur=8
                ,padding=9,border_radius=ft.BorderRadius(0,10,10,10),
                ),
        ],alignment=ft.MainAxisAlignment.START
    )
    messageBubble2 = ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text('Hey...',size=11,weight=ft.FontWeight.W_600),
                        ft.Row(
                            [
                                ft.Text('6:44 pm',size=8,color='white'),
                                
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ]
                ),bgcolor=ft.colors.with_opacity(0.5,ft.colors.BLUE_400), blur=8
                ,padding=9,border_radius=ft.BorderRadius(10,0,10,10),
                ),
        ],alignment=ft.MainAxisAlignment.END
    )
    
    def pick_files_result(e: ft.FilePickerResultEvent):
        global auth
        if e.files:
            # Call the upload function with the selected file path
            loading(e)
            try: 
                theUser = current() 
                id =  theUser['idToken']
                print(f'The current users id : {id}')
                uploadImgLink = uploadProfileImg(page, e.files[0].path, id)
                auth.update_profile(id,photo_url=uploadImgLink)
                refreshPage()
                end_loading(e)
                
            except Exception as error:
                end_loading(e)
                print(f'The was an error uploading {error}')
                page.snack_bar = ft.SnackBar(ft.Text(f'Failed to udate profile picture. {error}'), open=True)
                page.update()
                
            end_loading(e)

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)
    
    def goHome(e):
        refreshPage()
        page.go('/home')
    
    def review():
        page.dialog = review_dlg
        review_dlg.open = True
        
        page.update()
        
    def submitReview():
        review_data = review_dlg.content.content.value
        if len(review_data) > 3:
            #print(review_data)
            review_dlg.content.content.value = ""
            save_review(review_data,Useremail)
            review_dlg.open = False
            
            page.update()
        else:
            return

    print(f'the now user: {current()}')
    
    profileCardImg = ft.Container(
                height=100, 
                width=100,
                bgcolor=ft.colors.WHITE,
                image_src=f'{img}',
                image_fit= ft.ImageFit.COVER,
                border_radius=ft.border_radius.all(90),
                margin=ft.margin.all(10),
                
            )
    
    card = ft.Stack(
        [
            ft.Container(
                height=60,bgcolor='purple', 
                border_radius=ft.border_radius.only(bottom_left=70,bottom_right=70),
            ),
            ft.Container(
                content= ft.Column(
                    [
                        ft.Stack(
                            [
                                profileCardImg,
                                ft.IconButton(
                                    icon=ft.icons.ADD_A_PHOTO_OUTLINED,bgcolor='purple',
                                    icon_color='white', on_click= lambda e: pick_files_dialog.pick_files(
                                            allow_multiple=False
                                        ),right=0,bottom=0,
                                ),
                            ]
                        )
                    ],alignment=ft.MainAxisAlignment.START,spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),width=360,
            ),
            selected_files,
            
        ],height=150,
    )
    
   
    
    # PAGES..............
    
    starter = ft.Row(   
        [ ],
        scroll="hidden",expand=True,spacing=2,
        on_scroll_interval=1
    ) 
    
    signUpForm = ft.Container(
                content=ft.Column(
                    [
                        ft.TextField(label='Enter you name',border=ft.InputBorder.UNDERLINE),
                        ft.TextField(label='Enter your email',border=ft.InputBorder.UNDERLINE),
                        ft.TextField(label='Set your password',border=ft.InputBorder.UNDERLINE,password=True,
                        can_reveal_password=True),
                        ft.TextField(label='Confirm password',border=ft.InputBorder.UNDERLINE,password=True,
                        can_reveal_password=True),
                    ]
                ),padding=ft.padding.only(left=20,right=20),
                            margin=ft.margin.only(bottom=15) 
            )
    Accept_terms = ft.Checkbox(label="Accept terms and conditions", value=False)
    signUp = ft.Column(
            [
                ft.Text('Sign-up',size=40,weight=ft.FontWeight.W_600),
                signUpForm,
                ft.Container(
                    content=ft.Column(
                        [
                             ft.Row(
                                [
                                    Accept_terms,
                                    
                                ],alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Row(
                                [
                                    ft.Text(spans=[
                                                ft.TextSpan('Already have an account ? '),
                                                ft.TextSpan('Sign-in',
                                                            style=ft.TextStyle(color='blue'),
                                                            on_click= lambda _: page.go('/auth2')
                                                        ),
                                            ],size=15 
                                        ),
                                    
                                ],alignment=ft.MainAxisAlignment.CENTER
                            )
                           
                        ]
                    )
                    ),
                ft.Container(
                    #content=ft.ElevatedButton('Submit',on_click=lambda _: page.go('/home')),
                    content=ft.ElevatedButton('Submit',on_click=lambda e: validateSignUp(e)),
                    margin=ft.margin.only(top=20)
                )
            ],expand=1,alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    auth = ft.Container(
        content=signUp        
        ,expand=True,image_src=f'./assets/wallpaper1.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.3
    )
    
    signIn = ft.Container(content=ft.Column(
                        [
                            ft.TextField(label='Enter your email',border=ft.InputBorder.UNDERLINE, keyboard_type=ft.KeyboardType.EMAIL, enable_suggestions=True),
                            ft.TextField(label='Enter your password',border=ft.InputBorder.UNDERLINE,password=True,
                                         can_reveal_password=True
                                         ),
                        ]
                    ),padding=ft.padding.only(left=20,right=20),
                             margin=ft.margin.only(bottom=15)
                )
     
    auth2 = ft.Container(
        content=ft.Column(
            [
                ft.Text('Sign-in',size=40,weight=ft.FontWeight.W_600),
                signIn,
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(spans=[ 
                                        ft.TextSpan('Need an account? '),
                                        ft.TextSpan('Sign-up',
                                                    style=ft.TextStyle(color='blue'),
                                                    on_click= lambda _: page.go('/auth')
                                                ),
                                    ],size=15
                                ), 
                            ft.Text(spans=[
                                        ft.TextSpan('Forgot password',
                                                    style=ft.TextStyle(color='red'),
                                                    on_click= lambda e: resetPassword(e)
                                                ),
                                    ],size=15
                                )
                            
                        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),margin=ft.margin.only(left=10,right=10)
                ),
                ft.Container(
                    content=ft.ElevatedButton('Submit',on_click=lambda e: signin(e)),
                   
                )
            ],expand=1,alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),expand=True,image_src=f'./assets/wallpaper1.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.3
    )
    
    newConvo = ft.IconButton(
        icon=ft.icons.ADD,icon_size=40,
        bgcolor=ft.colors.with_opacity(0.4,'purple'),
        bottom=30,right=10,
        on_click= lambda e: start_new_chat(),
        tooltip=ft.Tooltip('Start a new conversation')
    )
    
    allConvos =ft.ListView(expand=1,)
    
    def loadChats():
        count = 1
        allChats = page.client_storage.get('uConversations')
        allConvos.controls.clear()
        #chatid = None
        #print(allChats[0][1]['time'])
        #[['SHD45km3Dq19jB9v9YsO', {'user': 'test5@gmail.com', 'time': '1726748273781'}]]

        try:
            for i in range(len(allChats)): 
                chatid = allChats[i][0]
                #print(int(allChats[i][1]['time']))
                allConvos.controls.append(
                    ft.ListTile(
                            title=ft.Text(f' {convert_timestamp2(allChats[i][1]['time'])}',
                                        width=150, overflow= ft.TextOverflow.FADE, no_wrap=True
                                        ),
                            subtitle=ft.Text(f'{convert_time(allChats[i][1]['time'])}'),
                            key=f'{allChats[i][1]['time']}',
                            trailing=ft.PopupMenuButton(  
                                items=[
                                    ft.PopupMenuItem(icon=ft.icons.DELETE_OUTLINE,text="Delete",on_click= lambda e: deleteChat(e)),
                                ],
                                menu_position= ft.PopupMenuPosition.UNDER
                            ),data= f'{chatid}',
                            on_click= lambda e: openChatFor(e,chatid)
                        )
                ) 
                count += 1
        except Exception as error:
            print(f'There was an error setting up conversations: {error}')
        page.update()
    
    
    def getChats():
        
        u = current()
        #print(u['email'])
        allChats = get_conversations(u['email'])
        page.client_storage.set('uConversations', allChats) 
        
        loadChats()
        
    def deleteChat(e):
        #loading(e)
        id = e.control.parent.parent.data
        #print(id)
        try:
            delet_conversation(id)
            refreshPage()
            #end_loading(e)
        except Exception as error:
            end_loading(e)
            alert(e, 'The was an error deleting conversation')
            print(error)
            
        end_loading(e)
            
    
    welcomeMessage =  ft.Text(f'welcome, {Username} \nwhat would you like me to assist you with today',
                              size=16
                              )
    
    home = ft.Container(
        content=ft.Column(
            [
               welcomeMessage,
                ft.Row(
                    controls=[ 
                            ft.Container(content=ft.Text('Past conversations',)
                                    ,bgcolor=ft.colors.with_opacity(0.4,'purple'),
                                    border_radius=ft.border_radius.all(10),
                                    padding=ft.padding.all(10)
                                )
                              
                            ],alignment=ft.MainAxisAlignment.CENTER
                    ),
                ft.Stack(
                    [
                        allConvos,
                        newConvo
                    ],expand=True 
                )
            ],alignment=ft.MainAxisAlignment.CENTER,
            
            
        ),expand=True,padding=ft.padding.only(left=10,right=10),
        image_src='assets/aiAppBg2.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.3,
    )
    
    def messageRow(sender,content,time):
        if sender == 'bot':
            r = ft.Row(
                        [
                            ft.Container(
                                content=ft.Column( 
                                    [
                                        ft.Markdown(f'{ content}',
                                                    code_theme=ft.MarkdownCodeTheme.A11Y_DARK,
                                                    code_style=ft.TextStyle(size=11)
                                                    ),
                                        #ft.Text(f'{ message['content']}',width=250,size=11,weight=ft.FontWeight.W_600,no_wrap=False),
                                        ft.Row(
                                            [
                                                ft.Text(f'{convert_time(str(time))}',size=8,color='white'),
                                            
                                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        )
                                    ]
                                ),bgcolor=ft.colors.with_opacity(0.4,'black')
                                ,blur=8,expand=True
                                ,padding=6,border_radius=ft.BorderRadius(0,10,10,10),
                                ),
                        ],alignment=ft.MainAxisAlignment.START
                    )
            return r
        else:
            r = ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(f'{ content}',size=13,weight=ft.FontWeight.W_400,no_wrap=False,width=250),
                                        ft.Row(
                                            [
                                                ft.Text(f'{convert_time(str(time))}',size=8,color='white'),
                                                
                                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        )
                                    ],horizontal_alignment=ft.CrossAxisAlignment.END
                                ),bgcolor=ft.colors.with_opacity(0.5,ft.colors.BLUE_400), blur=8
                                ,padding=6,border_radius=ft.BorderRadius(10,0,10,10)
                                ),
                        ],alignment=ft.MainAxisAlignment.END
                    )
            return r
    
    
    new_chatpage_messagebox = ft.Column(
        [
            ft.Container(
                content=ft.Text('Hi there,\n What can i assist you with',
                                size=25,text_align=ft.TextAlign.CENTER
                                ,weight=ft.FontWeight.BOLD
                                ),height=200
            )
        ],scroll=ft.ScrollMode.HIDDEN,auto_scroll=True,alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    def start_new_chat():
        global Useremail
         # Get the current timestamp
        time = int(datetime.now().timestamp())
        # Set new conversation date
        conversationDate.value = titleTime2(time)
        current_user = Useremail
        
        loading(e)
        try:
            # Set id for new chat gotten from create conversation function
            new_chatpage_messagebox.data = create_new_conversation(current_user,str(time))
            sleep(1)
            end_loading(e)
            page.go('/newChatPage')
        except Exception as error: 
            end_loading(e)
            ft.SnackBar(content=ft.Text('The was an error starting a new chat...'),open=True)
            print(error)
            
    def sendMessage(e,messagebox):
        convo_id = messagebox.data
        message = e.control.parent.controls[0].value
        #print(message)
        if len(message) >= 2:
            if messagebox == new_chatpage_messagebox:
                messagebox.controls[0].visible = False
            time = str(floor(datetime.now().timestamp()))
            #print(e.control.parent.value)
            #print(messagebox.controls)
            e.control.parent.controls[0].value = ''
            messagebox.controls.append(
            messageRow(Useremail,message,time)
            )
            save_chat_message(message,Useremail,convo_id, time)
            page.update() 
            sleep(1)
            bot_reply= send_user_message(message)
            time = str(floor(datetime.now().timestamp()))
            save_chat_message(bot_reply,'bot',convo_id, time)
            messagebox.controls.append( messageRow('bot',bot_reply,time) )
            
            page.update()
        else:
            alert(e,'Sorry a valid message is required!')
            page.update
    
    
    newChatPage = ft.Container(
        content=ft.Column(
            [
                 ft.Container(
                    content= new_chatpage_messagebox
                    ,expand=11,padding=ft.padding.only(left=10,right=10),
                    
                ),
              ft.Container(
                  content= ft.TextField(
                                    multiline=True,
                                    hint_text='Message..',border=ft.InputBorder.NONE,adaptive=True,
                                    suffix=ft.IconButton(icon=ft.icons.SEND,icon_color='green',on_click= lambda e: sendMessage(e,new_chatpage_messagebox)),
                                    fill_color=ft.colors.with_opacity(0.1,ft.colors.GREY_300),
                                    border_radius=ft.border_radius.all(30)
                                ),
                  height=50,padding=ft.padding.only(left=9,right=9)
              )
                           
            ]
        ),expand=True,image_src='assets/aiAppBg2.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.3,
    )
    
    messageBox = ft.Column(
                        [
                            messageBubble2, messageBubble, messageBubble2,
                            messageBubble, messageBubble2, messageBubble,
                            messageBubble2, messageBubble, messageBubble,
                            messageBubble2, messageBubble, messageBubble,messageBubble2,
                        ],scroll=ft.ScrollMode.HIDDEN,auto_scroll=True
                    )
    
   
    def openChatFor(e,chatid):
        loading(e)
        #page.update()
        time = e.control.key
        id = e.control.data
        messageBox.data = id
        #print('\n',id)
        #print(time)
        messages = load_messages(id)
        #print(f'{messages}')
        conversationDate.value = titleTime(time)
        messageBox.controls.clear()
        #print(f'Convo of id: {id} with messages {messages}')
         
        for message in messages:
            if message['sender'] == 'bot':
                messageBox.controls.append(
                    messageRow('bot',message['content'],message['time'])
                )
            elif message['sender'] != 'bot':
                messageBox.controls.append(
                    messageRow(message['sender'],message['content'],message['time'])
                )
            else:
                pass
            
        page.update()
        end_loading(e)
        page.go('/chatPage')
        
    messageBoxS = ft.TextField(
                                hint_text='Ask Zylla...',
                                expand=10,multiline=True,border=ft.InputBorder.NONE,
                                content_padding=ft.padding.only(left=8,right=3,bottom=1,top=1)
                            )
    chatPage = ft.Container(
        content=ft.Column(
            [
                 ft.Container(
                    content=messageBox
                   ,expand=9,padding=ft.padding.only(left=10,right=10)
                ),
                 #Input field for texting messages....... 
                ft.Container(
                  content= ft.Row(
                      [
                          messageBoxS,
                          ft.IconButton(
                              icon=ft.icons.SEND,icon_color='purple',expand=2,
                              on_click= lambda e: sendMessage(e,messageBox)
                          )
                      ],expand=True,alignment=ft.MainAxisAlignment.CENTER,vertical_alignment=ft.CrossAxisAlignment.CENTER
                      ),
                  padding=ft.padding.only(left=9,right=9,top=0,bottom=0),expand=1 ,
              )
                           
            ],spacing=0
        ),expand=True, image_src='assets/aiAppBg2.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.3,
    )
    
    #setUserData(User)
    uNameInput = ft.TextField(f'{Username}', suffix=ft.IconButton(icon=ft.icons.EDIT,on_click= lambda _: editUserName()),
                                     read_only=True,border=ft.InputBorder.NONE,
                                     )
    uEmailInput = ft.TextField(f'{Useremail}',read_only=True,border=ft.InputBorder.NONE)
    
    profile = ft.Container(
        content=ft.Column(
            [
                card,
                ft.Container(
                    content=ft.Column(
                        [
                            uNameInput,
                            uEmailInput,
                            ft.TextField('user name',read_only=True,password=True,suffix=ft.IconButton(icon=ft.icons.LOCK_RESET),border=ft.InputBorder.NONE),
                        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN ,spacing=12
                    ),padding=ft.padding.only(left=20,right=20)
                ), 
                ft.ListTile(title=ft.Text('Change theme'),trailing=ft.Switch(active_color='white', on_change=theme_changed)),
                ft.ListTile(title=ft.Text('Log_out'), trailing=ft.Icon(name=ft.icons.LOGOUT_OUTLINED), on_click= lambda _: signOut(page))
            ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,spacing=0
        ),expand=True,image_src='assets/aiAppBg2.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.3,
    )
    
    #print(f'the current user is : {current()}')  
    #loadChats()
    #print(result)      
    #addOnboardingScreens(starter,'/auth',3,)   
    #onboard = OnboardingPages("/auth",pageHolder,page)  
    #onboardingPage = onboard.create()
    #safeArea = ft.SafeArea(content=onboardingPage,expand=True)
    
    pages = {
        '/': ft.View( "/", [onboard,],padding=0,),
        #'/': ft.View( "/", [auth,],padding=0,),
        '/auth': ft.View( "/auth", [auth,],padding=0,),
        '/auth2': ft.View( "/auth2", [auth2,],padding=0,), 
        '/home': ft.View( "/home", [home,],padding=0,appbar=appbar1), 
        '/newChatPage': ft.View( "/newChatPage", [newChatPage,],padding=0,appbar=appbar2), 
        '/chatPage': ft.View( "/chatPage", [chatPage,],padding=0,appbar=appbar2), 
        '/profile': ft.View( "/profile", [profile,],padding=0,appbar=profileAppbar), 
    } 
    def route_change(route):   
        page.views.clear()
        
        page.views.append( 
            pages[page.route]
            
        ) 
        
        page.update() 
         
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    #page.go('/')
    # Starts the app by showing the onboarding page for new users or signin if the app has been opened before....
    start_controls(page,'/','/auth')
    
    def automate_signIn():
        if page.route == '/auth' or page.route == '/auth2':
            loading(e)
            auto_signin()
            end_loading(e)
        else:
            pass
    
    
    Thread(target=automate_signIn, daemon=True).start() 
    
    
ft.app(target=main,assets_dir="assets") 