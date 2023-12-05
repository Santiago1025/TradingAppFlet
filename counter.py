import flet as ft

def main(page: ft.Page):
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    txt_number = ft.TextField(value=f"0",text_align=ft.TextAlign.CENTER,width=100)
    
    def minus(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()
        
    def plus(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()
    
    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE,on_click=minus),
                txt_number,
                ft.IconButton(ft.icons.ADD,on_click=plus),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
ft.app(main)