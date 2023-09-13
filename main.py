from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
import pymongo

KV = '''
BoxLayout:
    orientation: 'vertical'
    
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: "48dp"
        
        MDTextField:
            id: message_input
            hint_text: "Type your message..."
            
        MDRaisedButton:
            text: "Send"
            on_release: app.send_message()

    ScrollView:
        MDList:
            id: chat_history
'''

class ChatApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        # Initialize MongoDB connection
        self.client = pymongo.MongoClient("mongodb+srv://satwikit21051:Satwik2021@cluster0.zmqqwlf.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["chat_app"]
        self.collection = self.db["messages"]

    def send_message(self):
        message_input = self.root.ids.message_input
        message_text = message_input.text.strip()

        if message_text:
            # Insert the message into MongoDB
            message = {"text": message_text}
            self.collection.insert_one(message)

            # Add the message to the chat history
            chat_history = self.root.ids.chat_history
            chat_history.add_widget(MDTextField(text=message_text, readonly=True))

            # Clear the input field
            message_input.text = ""

if __name__ == '__main__':
    ChatApp().run()
