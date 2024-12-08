import flet as ft
import json

current_page_num = 0

def main(page : ft.Page):
    page.title = 'LSA_Chatbot-OnbordingTest'
    page.window.always_on_top = True
    page.window.width = 330
    page.window.height = 670    
    page.window.max_height = 670 
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.fonts = {
        "billa bong": "assets/fonts/Billabong.ttf"
    }
    
    # Functions.........
    
    current_page = ft.Container(
        expand=1,
    )

    with open("content.json") as json_file:   
        data = json.load(json_file)
        
    def set_content(value):
        global current_page_num
        current_page.content= ft.Column(
            [
                ft.Text(value=data[f'content{current_page_num+1}'][0],size=15,weight=ft.FontWeight.W_500),
                ft.Container(
                        content=ft.Image('assets/onbording1.png')
                    ),
                ft.Text(value=data[f'content{current_page_num+1}'][1],
                        text_align=ft.TextAlign.CENTER,size=25, font_family= "billa bong")
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
                nextBtn.on_click = lambda e: print("goto_final(e)")
                
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
                nextBtn.on_click = lambda e: print("goto_final(e)")
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
    
    def onboard2():
        return onboard
    
    
    page.add(
        onboard
    )

ft.app(target=main)