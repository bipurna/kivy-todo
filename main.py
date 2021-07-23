import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from datetime import datetime
from kivy.clock import Clock
from kivy.properties import ObjectProperty
import sqlitecon

class DropDownStatus(DropDown):
    pass


class TodoUI(BoxLayout):
    
    layout=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.task_list = []
        sqlitecon.create_connection(os.path.dirname(os.path.realpath(__file__))+"/todo.db")
        self.refresh_layout()

    def add_task(self):
        input_task = self.ids.input_task.text
        status = "Not Complete"
        insert_time = f"{datetime.now():%H}:{datetime.now():%M}:{datetime.now():%S}:{datetime.now():%f}"
        complete_time = ""
        self.task_list.append(input_task)
        sqlitecon.insert_data_db(os.path.dirname(os.path.realpath(__file__))+"/todo.db",input_task,status,insert_time,complete_time)
        self.refresh_layout()
    
    def dropdown_open(self):
        dropdown= DropDownStatus()
        st_btn = self.ids.status
        st_btn.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(st_btn, 'text', x))
        
        
    def clear_inputs(self): 
        for inp  in reversed(self.ids.inputs.children):
            if isinstance(inp,TextInput):
                inp.text = ''
                
    def refresh_layout(self):
        
        layout = self.ids.tasks
        layout.clear_widgets()
      
        self.conn = sqlitecon.display(os.path.dirname(os.path.realpath(__file__))+"/todo.db")
        layout.clear_widgets()
        for data in self.conn:
            self.check_btn = CheckBox(group="edit")
            self.check_btn.size_hint = (.1,None)
            self.check_btn.height = 30
            self.check_btn.id = str(data[0])
            self.check_btn.bind(active=self.check_btn_active)
            layout.add_widget(self.check_btn)
            # self.add_widget(self.check_btn)
            for item in data:
                self.t = Label()
                self.t.size_hint = (.1, None)
                self.t.height = 30
                self.t.text = str(item)
                layout.add_widget(self.t)
            self.ids.done.disabled = True
            self.ids.delete.disabled=True
            
    def check_btn_active(self,checkbox,value):
        self.id = checkbox.id
        print(self.id)
        if value:
            self.ids.done.disabled = False
            self.ids.delete.disabled=False
        else:
            self.ids.done.disabled = True
            self.ids.delete.disabled=True
    def delete_item(self):
        id = self.id
        sqlitecon.delete_entry(os.path.dirname(os.path.realpath(__file__))+"/todo.db",id)
        self.refresh_layout()
    def completed(self):
        id=self.id
        complete_time = f"{datetime.now():%H}:{datetime.now():%M}:{datetime.now():%S}:{datetime.now():%f}"
        status = "Completed"
        sqlitecon.update_data(os.path.dirname(os.path.realpath(__file__))+"/todo.db",id,status,complete_time)
        self.refresh_layout()
            
    
class TodoApp(App):
    def update(self,dt):
        date = datetime.today()
        self.title = f"TodoList - {date:%A} {date:%d} {date:%b}, {date:%Y} - {date:%H}:{date:%M}:{date:%S}"
        
    def build(self):
        todo = TodoUI()
        {Clock.schedule_interval(self.update,1.0/32.0)}
        return todo

if __name__ == "__main__":
    todo = TodoApp()
    todo.run()