import flet as ft

def main(page:ft.Page):
    page.window_width = 320
    page.theme_mode = ft.ThemeMode.LIGHT
    
    theAppbar = ft.AppBar(
        title=ft.Text('Page nav tests'),
        actions=[
            ft.IconButton(
                icon=ft.icons.SATELLITE_ALT,
                on_click= lambda _: page.go('/page2')
            )
        ]
    )
    
    # functions ...................................
    def view_pop(e: ft.ViewPopEvent):   
       
        page.views.pop()
        #print(page.views)
        top_view = page.views[-1]
        page.go(top_view.route)
        
        
     
   
    
    
    # Pages || structures and layouts...................... 
    mainMan1 = ft.Container(
        content=ft.Column( 
            [
                ft.Text('Hello page 3') ,
                ft.TextButton('go to page 2', on_click= lambda _: page.go('/page2'))
            ]
        )
    )
    
    mainMan = ft.Container(
        content=ft.Column(
            [
                ft.Text('Hello page 1'),
                ft.TextButton('go to page 2', on_click= lambda _: page.go('/page2'))
            ]
        )
    )
    
    secondPage = ft.Container( 
        content=ft.Column(
            [
                ft.Text('Hello page 2'),
                ft.ElevatedButton('go back',on_click= lambda _: page.go('/')),
                ft.ElevatedButton('go to page 3',on_click= lambda _: page.go('/page3'))
            ] 
        )
    )
    
    
    # Pages || routes and nav controls...................
    pages = {
        #'/': ft.View( "/", [onboardingPage,],padding=0,), 
        '/': ft.View( "/", [mainMan,],padding=0,appbar=theAppbar ),
        '/page2': ft.View( "/page2", [secondPage,],padding=0,appbar=theAppbar), 
        '/page3': ft.View( "/page3", [mainMan1,],padding=0,appbar=theAppbar), 
        
    } 
    
    
    
    def route_change(e: ft.RouteChangeEvent):
        #page.views.insert(2, pages[page.route])
        page.views.clear()
        
        page.views.append(pages["/"])
        if page.route == "/page2":
            page.views.append(pages["/page2"])
        elif page.route == "/page3":
            page.views.append(pages["/page2"])
            page.views.append(pages["/page3"])
        print(page.views)
        
        #print(page.views)
        page.update()     
        

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    
    
     
ft.app(target=main)