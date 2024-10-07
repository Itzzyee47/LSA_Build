import flet as ft

def nextPage(e):
    key = e.control.parent.parent.key
    starter = e.control.parent.parent.parent
    #print(key)
    key = str(int(key)+1)
    #starter.controls.append(starter.controls.pop(0))
    #e.page.update()
    starter.scroll_to(300,duration=500)
    #starter.scroll_to(offset=0.4, delta=0.5,key=key,duration=500,curve=ft.AnimationCurve.EASE_IN) # type: ignore

def nextPage2(e):
    key = e.control.parent.parent.parent.key
    starter = e.control.parent.parent.parent.parent
    key = str(int(key)+1)
    starter.scroll_to(offset=0.1, delta=0.5,key=key,duration=500,curve=ft.AnimationCurve.EASE_IN) # type: ignore


def prePage2(e):
    key = e.control.parent.parent.parent.key
    starter = e.control.parent.parent.parent.parent
    key = str(int(key)-1)
    starter.scroll_to(offset=0.4, delta=0.5,key=key,duration=500,curve=ft.AnimationCurve.EASE_IN) # type: ignore

def screenContent(i):
    match i:
        case 0:
            content = ft.Container(
                content = ft.Column(
                    [
                        ft.Text('Welcome to the LSA app',size=15,weight=ft.FontWeight.W_500),
                        ft.Container(
                            content=ft.Image('assets/onbording1.png')
                        ),
                        ft.Text('Your AI-powered guide for all things Landmark and research',
                                text_align=ft.TextAlign.CENTER,
                                size=25,
                                )
                    ],alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER 
                ),padding=ft.padding.only(left=10,right=10),
            )
            return content
        
        case 1:
            content = ft.Container(
                content = ft.Column(
                    [
                        ft.Text('Meet Zylla, Your personal research buddy,',size=15,weight=ft.FontWeight.W_500),
                        ft.Container(
                            content=ft.Image('assets/onbording1.png')
                        ),
                        ft.Text('Powered by cutting-edge AI and Cloud technologies!',
                                text_align=ft.TextAlign.CENTER,
                                size=25,)
                    ],alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER 
                ),padding=ft.padding.only(left=10,right=10),
            )
            return content
        
        case 2:
            content = ft.Container(
                content = ft.Column(
                    [
                        ft.Text('Got a questions',size=15,weight=ft.FontWeight.W_500),
                        ft.Container(
                            content=ft.Image('assets/onbording1.png')
                        ),
                        ft.Text('Zylla\'s got answers! Fast, reliable, and always up-to-date',
                                text_align=ft.TextAlign.CENTER,
                                size=25,)
                    ],alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER 
                ),padding=ft.padding.only(left=10,right=10),
            )
            return content
        
        case default:
            content = ft.Container(
                content = ft.Column(
                    [
                        ft.Text('Defult page'),
                        ft.Container(
                            content=ft.Image('assets/onbording1.png')
                        ),
                        ft.Text('About data.......')
                    ],alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER 
                )
            )
            return content

def addOnboardingScreens(control,route,x=3):
        count = 0
        for i in range(0,x):
            #print(i)
            if i == 0:
                control.controls.append(
                ft.Container(
                        content=ft.Column( 
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            screenContent(i)
                                        ]
                                    ),
                                    ),
                                ft.TextButton('next page',on_click= lambda e: nextPage(e) ),
                                
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    image_src='assets/aiAppBg3.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.1,width=320,key=f'{str(count)}',padding=ft.padding.only(top=10,bottom=10),
                    )
            )
            elif i == x-1:
                control.controls.append(
                ft.Container(
                        content=ft.Column( 
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            screenContent(i)
                                        ]
                                    ),
                                    ),
                                ft.Row(
                                    [
                                        ft.TextButton('previous page',on_click= lambda e: prePage2(e)),
                                        ft.TextButton('next page',on_click= lambda e: e.page.go(route)),
                                    ],alignment=ft.MainAxisAlignment.SPACE_AROUND
                                )
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    image_src='assets/aiAppBg3.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.1,width=320,key=f'{str(count)}',padding=ft.padding.only(top=10,bottom=10),
                    )
            )
            else:
                control.controls.append(
                ft.Container(
                        content=ft.Column( 
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            screenContent(i)
                                        ]
                                    ),
                                    ),
                                ft.Row(
                                    [
                                        ft.TextButton('previous page',on_click= lambda e: prePage2(e)),
                                        ft.TextButton('next page',on_click= lambda e: nextPage2(e) ),
                                    ],alignment=ft.MainAxisAlignment.SPACE_AROUND
                                )
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    image_src='assets/aiAppBg3.jpg',image_fit=ft.ImageFit.COVER,image_opacity=0.1,width=320,key=f'{str(count)}',padding=ft.padding.only(top=10,bottom=10),
                    )
            )
            
            count += 1