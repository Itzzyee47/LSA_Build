import flet as ft

def start_controls(page,onbord,signin):
    first_timer = page.client_storage.contains_key("first_timer")
    
    if first_timer:
        page.client_storage.set("first_timer", False)
        page.go(signin)
    else:
        page.client_storage.set("first_timer", True)
        page.go(onbord)
        
def set_auto_signin(page,email,password):
    old_user = page.client_storage.contains_key("users_credentials")
    
    try:
        if old_user:
            # Remove the old users credentials
            page.client_storage.remove("users_credentials")
            # Store the new users credentials
            page.client_storage.set("users_credentials", [ email, password ])
            
            return True
        else:
            # Store the new users credentials
            page.client_storage.set("users_credentials", [ email, password ])
            
            return True
    except Exception as er:
        pass 
    
#if page.route != '/' or page.route != '/auth' or page.route != '/auth2':
    #if page.route == '/home':
        #pass
    #else:
        #page.views.append('/home') 

"""
ft.Container(
                  content= ft.TextField(
                                    multiline=False,expand=True,height=150,
                                    hint_text='Message..',border=ft.InputBorder.UNDERLINE,adaptive=True,
                                    suffix=ft.IconButton(icon=ft.icons.SEND,icon_color='green',on_click= lambda e: sendMessage(e,messageBox)),
                                    fill_color=ft.colors.with_opacity(0.1,ft.colors.GREY_300),
                                   content_padding=ft.padding.only(left=8,right=8,top=0,bottom=6),
                                ),
                  padding=ft.padding.only(left=9,right=9,top=0,bottom=0),expand=1,
              )
"""
            
    