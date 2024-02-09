import time
import flet as ft

class ToDO(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.main_container = None
        self.tasks_view = None
        self.text_field = None
        self.tabs = None
        self.delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete this item?"),
            actions=[
                ft.TextButton("Yes", on_click=self.delete_confirmed),
                ft.TextButton("No", on_click=self.close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self._actual_deleted_item = None

    def close_dialog(self, e):
        self.delete_dialog.open = False
        e.page.update()

    def delete_confirmed(self, e):
        
        self.delete_item_callback(self._actual_deleted_item)
        self.delete_dialog.open = False
        e.page.update()
        e.page.show_snack_bar(
            ft.SnackBar(
                ft.Text("Deleted Item successfully!"),
                action="OK!",
                open=True
            )
        )

    def open_delete_dialog(self, item):
        item.page.dialog = self.delete_dialog
        item.page.dialog.open = True
        self._actual_deleted_item = item
        item.page.update()

    def update(self):
        
        index = self.tabs.current.selected_index

        
        for todo_item_control in self.tasks_view.current.controls:
            if index == 1:
                todo_item_control.visible = not todo_item_control.item_checkbox.current.value
            elif index == 2:
                todo_item_control.visible = todo_item_control.item_checkbox.current.value
            else:
                todo_item_control.visible = True
        super().update()

    def delete_item_callback(self, item):
        
        self.tasks_view.current.controls.remove(item)
        self.update()

    def submit_item(self, e: ft.ControlEvent):
        
        if self.text_field.current.value:
            item = TodoItem(self.text_field.current.value, self.update, self.open_delete_dialog)
            self.tasks_view.current.controls.append(item)
            self.text_field.current.value = ""
            self.text_field.current.counter_text = '0 chars'
            self.page.show_snack_bar(
                ft.SnackBar(
                    ft.Text("Added New To-Do Item"),
                    action="OK!",
                    open=True
                )
            )
            self.update()

    def tabs_change(self, e):
       
        self.update()

    def counter_text_change(self, e: ft.ControlEvent):
        
        self.text_field.current.counter_text = f'{len(e.data)} chars'
        self.text_field.current.update()

    def build(self):
        
        self.text_field = ft.Ref[ft.TextField]()
        self.tasks_view = ft.Ref[ft.Column]()
        self.main_container = ft.Ref[ft.Column]()
        self.tabs = ft.Ref[ft.Tabs]()

        return ft.Column(ref=self.main_container,
                         controls=[
                             ft.Row(
                                 controls=[
                                     ft.TextField(
                                         ref=self.text_field,
                                         helper_text="What do you plan to do?",
                                         hint_text="Try Something new..",
                                         counter_text='0 chars',
                                         keyboard_type=ft.KeyboardType.TEXT,
                                         label="New Item",
                                         expand=True,
                                         text_size=20,
                                         tooltip="Field for new items",
                                         prefix_icon=ft.icons.LIST_ALT_ROUNDED,
                                         autofocus=True,
                                         on_change=self.counter_text_change,
                                         on_submit=self.submit_item
                                     ),
                                     ft.FloatingActionButton(
                                         icon=ft.icons.ADD,
                                         tooltip="add item",
                                         on_click=self.submit_item
                                     )
                                 ]
                             ),
                             ft.Tabs(
                                 ref=self.tabs,
                                 tabs=[
                                     ft.Tab(text='all', icon=ft.icons.CHECKLIST_OUTLINED),
                                     ft.Tab(text='not yet done', icon=ft.icons.CHECK),
                                     ft.Tab(text='done', icon=ft.icons.DONE_ALL)
                                 ],
                                 selected_index=0,
                                 on_change=self.tabs_change
                             ),
                             ft.Column(
                                 ref=self.tasks_view,
                                 scroll=ft.ScrollMode.ALWAYS
                             )
                         ],
                         spacing=24,
                         width=630
                         )


class TodoItem(ft.UserControl):
    def __init__(self, item_text, checkbox_change, delete_dialog_callback):
       
        super().__init__()
        self.item_text = item_text
        self.open_delete_dialog = delete_dialog_callback
        self.checkbox_change = checkbox_change
        self.normal_view = ft.Ref[ft.Row]()
        self.edit_view = ft.Ref[ft.Row]()
        self.item_checkbox = ft.Ref[ft.Checkbox]()
        self.text_field = ft.Ref[ft.TextField]()

    def save_edit(self, e):
       
        self.normal_view.current.visible = True
        self.edit_view.current.visible = False
        self.text_field.current.autofocus = False
        self.item_checkbox.current.label = self.text_field.current.value
        # It updates the UI.
        self.update()
        e.page.show_snack_bar(
            ft.SnackBar(
                ft.Text("Updated Item successfully!"),
                action="OK!",
                open=True
            )
        )

    def copy_item(self, e):
        
        e.page.set_clipboard(self.item_checkbox.current.label)
        e.page.show_snack_bar(
            ft.SnackBar(
                ft.Text("Content copied to Clipboard!"),
                action="OK!",
                open=True
            )
        )

    def edit_item(self, e):
        
        self.normal_view.current.visible = False
        self.edit_view.current.visible = True
        self.text_field.current.autofocus = True
        self.update()

    def delete_item(self, e):
        
        self.open_delete_dialog(self)

    def item_checkbox_value_change(self, e):
       
        self.checkbox_change()

    def build(self):
       
        return ft.Column(
            controls=[
                ft.Row(
                    ref=self.normal_view,
                    controls=[
                        ft.Checkbox(
                            ref=self.item_checkbox,
                            label=self.item_text,
                            value=False,
                            on_change=self.item_checkbox_value_change),
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.COPY,
                                    icon_color=ft.colors.BLUE,
                                    tooltip="copy",
                                    on_click=self.copy_item,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_color=ft.colors.LIGHT_GREEN_ACCENT_700,
                                    on_click=self.edit_item,
                                    tooltip="update item",
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE_FOREVER,
                                    icon_color=ft.colors.RED_900,
                                    tooltip="delete item",
                                    on_click=self.delete_item,
                                ),
                            ]
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    ref=self.edit_view,
                    visible=False,
                    controls=[
                        ft.TextField(
                            ref=self.text_field,
                            value=self.item_text,
                            tooltip="field to edit the item",
                            autofocus=False,
                            label="Edit Item",
                            expand=True,
                            on_submit=self.save_edit,
                            suffix=ft.ElevatedButton(text="Update", on_click=self.save_edit))
                    ],
                )
            ],
        )


def main(page: ft.Page):
   

    page.title = "myToDo App"
    page.window_width = 562
    page.window_height = 720
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"
    page.fonts = {"SF-simple": "/fonts/San-Francisco/SFUIDisplay-Light.ttf",
                  "SF-bold": "/fonts/San-Francisco/SFUIDisplay-Bold.ttf"}
    page.theme_mode = "light"
    page.theme = ft.Theme(
        font_family="SF-simple",
        use_material3=True,
        visual_density=ft.ThemeVisualDensity.COMPACT,
    )

    def change_bg_theme(e):
       
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon_button.selected = not theme_icon_button.selected
        page.update()

    todo = ToDO()

    theme_icon_button = ft.IconButton(
        ft.icons.DARK_MODE,
        selected_icon=ft.icons.LIGHT_MODE,
        selected=False,
        on_click=change_bg_theme, icon_size=40
    )

    page.add(
        ft.Row(
            controls=[
                ft.Text(
                    value="myToDo App",
                    text_align=ft.TextAlign.CENTER,
                    selectable=False,
                    font_family="SF-bold",
                    weight=ft.FontWeight.BOLD,
                    size=40
                ),
                theme_icon_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        ft.Divider(),
        todo,
        ft.Text(
            "Made by Akash Yadav",
            
            italic=True, color="blue",
            text_align=ft.TextAlign.END,
            expand=True,
        )
    )



ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="assets")
