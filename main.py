from math import exp
from token import LESS
from turtle import left
from typing import Container
import flet as ft
from funtions import *

def main(page: ft.Page):
    page.title = 'LSA_Chatbot'
    page.window.always_on_top = True
    page.window.width = 330
    page.window.height = 670    
    page.window.max_height = 670 
    page.theme_mode = ft.ThemeMode.DARK 
    
    
    def view_pop(view):   
        page.views.pop()
        page.go(page.route)
        page.update()
     
    #PAGE COMPONENTS..............
    def alert(e,value):
        dlg = ft.AlertDialog(
            title=ft.Text(value=value,size=13,text_align=ft.TextAlign.CENTER)
            )
        e.page.dialog = dlg # type: ignore
        dlg.open = True
        e.page.update() # type: ignore

    # .lfakeljrn f;kjae;raemf
    def close_dlg(e,dlgName):
            dlgName.open = False
            e.page.update()
            
    def resetPassword(e):
        emailValue = signIn.content.controls[0].value
        
        if emailValue == "":
            alert(e,'Please enter the email to send the reset password link!')
        else:
            alert(e,f'Check your email {emailValue} for the reset password link')
            
    
    appbar1 = ft.AppBar(
       title=ft.Text('Conversations',weight=ft.FontWeight.W_600),
       bgcolor='purple',
        actions=[
            ft.Container(
                height=30,  
                width=30,
                bgcolor=ft.colors.WHITE,
                image_src=f'assets/avatar.png',
                border_radius=ft.border_radius.all(40),
                margin=ft.margin.all(10),
            on_click= lambda _: page.go('/profile')
            ),
        ]         
    )
    
    conversationDate = ft.Text('18/09/2024',size=10,color='grey')
    
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
            on_click= lambda _: page.go('/home')
            ),
        actions=[
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Restart",on_click=lambda _:page.go('/')),
                    ft.PopupMenuItem(text="About Zylla"),
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
                    ft.PopupMenuItem(text="Restart",on_click=lambda _:page.go('/')),
                    ft.PopupMenuItem(text="Settings"),
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
                        ft.Text('Hello oawibdaoiwbodaiw doawidbnoaiwbndoaibw doaiwndoiabwodba owdainbwoidbaow doaiwnbdoiwdoa owdinaowdbi aowidb',size=10,width=250,weight=ft.FontWeight.W_600,no_wrap=False),
                        ft.Row(
                            [
                                ft.Text('6:44 pm',size=8,color='white'),
                               
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ]
                ),bgcolor=ft.colors.BLACK12
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
                        ft.Text('Hey...',size=10,weight=ft.FontWeight.W_600),
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
            selected_files.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
            )
            card.controls[1].imagesrc=f'{selected_files.value}',
            selected_files.update()
            page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    selected_files = ft.Text()

    page.overlay.append(pick_files_dialog)

    
    
    card = ft.Stack(
        [
            ft.Container(
                height=60,bgcolor='purple', 
                border_radius=ft.border_radius.only(bottom_left=70,bottom_right=70),
            ),
            ft.Container(
                height=100, 
                width=100,
                bgcolor=ft.colors.WHITE,
                image_src=f'assets/avatar.png',
                border_radius=ft.border_radius.all(90),
                margin=ft.margin.all(10),
                bottom=30,left=100
            ),
            ft.IconButton(
                icon=ft.icons.ADD_A_PHOTO_OUTLINED,bottom=20,left=140,bgcolor='purple',
                icon_color='white', on_click= lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ),
            ),
            selected_files,
            
        ],height=150,alignment=ft.alignment.center
    )
    
    # PAGES..............
    
    starter = ft.Row(   
        [ ],
        scroll="hidden",expand=True,spacing=2,
        on_scroll_interval=1
    ) 
    
    signUp = ft.Column(
            [
                ft.Text('Sign-up',size=30,weight=ft.FontWeight.W_500),
                ft.Container(content=ft.Column(
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
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(spans=[
                                        ft.TextSpan('Already have an account ? '),
                                        ft.TextSpan('Sign-in',
                                                    style=ft.TextStyle(color='blue'),
                                                    on_click= lambda _: page.go('/auth2')
                                                ),
                                    ],size=10 
                                ),
                            
                        ],alignment=ft.MainAxisAlignment.CENTER
                    )
                    ),
                ft.Container(
                    content=ft.ElevatedButton('Submit',on_click=lambda _: page.go('/home')),
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
                            ft.TextField(label='Enter your email',border=ft.InputBorder.UNDERLINE, keyboard_type=ft.KeyboardType.EMAIL),
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
                ft.Text('Sign-in',size=30,weight=ft.FontWeight.W_500),
                signIn,
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(spans=[
                                        ft.TextSpan('Need have an account ? '),
                                        ft.TextSpan('Sign-up',
                                                    style=ft.TextStyle(color='blue'),
                                                    on_click= lambda _: page.go('/auth')
                                                ),
                                    ],size=10
                                ), 
                            ft.Text(spans=[
                                        ft.TextSpan('Forgot password',
                                                    style=ft.TextStyle(color='red'),
                                                    on_click= lambda e: resetPassword(e)
                                                ),
                                    ],size=10
                                )
                            
                        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),margin=ft.margin.only(left=10,right=10)
                ),
                ft.Container(
                    content=ft.ElevatedButton('Submit',on_click=lambda _: page.go('/home')),
                   
                )
            ],expand=1,alignment=ft.MainAxisAlignment.SPACE_AROUND,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),expand=True,image_src=f'./assets/wallpaper1.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.3
    )
    
    newConvo = ft.IconButton(
        icon=ft.icons.ADD,icon_size=40,
        bgcolor=ft.colors.with_opacity(0.4,'purple'),
        bottom=30,right=10,
        on_click= lambda _: page.go('/chatPage'),
        tooltip=ft.Tooltip('Start a new conversation')
    )
    
    allConvos =ft.ListView(expand=1)
    count = 1

    for i in range(0, 12):
        allConvos.controls.append(
            ft.ListTile(
                    title=ft.Text(f'list item {count}'),
                    on_click= lambda _: page.go('/chatPage')
                )
        )
        count += 1
    
    home = ft.Container(
        content=ft.Column(
            [
                ft.Text('welcome, username \nwhat would you like me to assist you with today',size=12),
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
        image_src='assets/aiAppBg2.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.4,
    )
    
    chatPage = ft.Container(
        content=ft.Column(
            [
                 ft.Container(
                    content=ft.Column(
                        [
                            messageBubble2, messageBubble, messageBubble2,
                            messageBubble, messageBubble2, messageBubble,
                            messageBubble2, messageBubble, messageBubble,
                            messageBubble2, messageBubble, messageBubble,messageBubble2,
                        ],scroll=ft.ScrollMode.HIDDEN,auto_scroll=True
                    ),expand=9,padding=ft.padding.only(left=10,right=10),
                    image_src='assets/aiAppBg.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.5,
                ),
              ft.Container(
                  content= ft.TextField(
                                    multiline=True,
                                    hint_text='Message..',border=ft.InputBorder.OUTLINE,adaptive=True,
                                    suffix=ft.IconButton(icon=ft.icons.SEND,icon_color='green',),
                                    fill_color=ft.colors.with_opacity(0.1,ft.colors.GREY_300),
                                    border_radius=ft.border_radius.all(30)
                                ),
                  height=70,padding=ft.padding.only(left=9,right=9)
              )
                           
            ]
        ),expand=True
    )
    
    profile = ft.Container(
        content=ft.Column(
            [
                card,
                ft.Container(
                    content=ft.Column(
                        [
                        ft.TextField('user name',read_only=True,border=ft.InputBorder.NONE,),  
                        ft.TextField('user@email.com',read_only=True,border=ft.InputBorder.NONE),
                        ft.TextField('user name',read_only=True,password=True,border=ft.InputBorder.NONE),
                        ft.ElevatedButton('Edit') 
                        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  
                    ),padding=ft.padding.only(left=20,right=20),
                ), 
                ft.ElevatedButton('log-out',icon=ft.icons.LOGOUT_OUTLINED,)
            ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START
        ),expand=True,image_src='assets/aiAppBg2.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.5,
    )
    
    #print(result)      
    addOnboardingScreens(starter,'/auth',3,) 
    onboardingPage = ft.SafeArea(content=starter,expand=True)
    
    pages = {
        
        '/': ft.View( "/", [auth,],padding=0,),
        '/auth2': ft.View( "/auth2", [auth2,],padding=0,), 
        '/home': ft.View( "/home", [home,],padding=0,appbar=appbar1), 
        '/chatPage': ft.View( "/chatPage", [chatPage,],padding=0,appbar=appbar2), 
        '/profile': ft.View( "/profile", [profile,],padding=ft.padding.only(bottom=20),appbar=profileAppbar), 
    } 
    def route_change(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
            
        )
        page.update() 
        
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    
    

ft.app(target=main,assets_dir="assets") 