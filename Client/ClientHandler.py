from Client import MenuKeyboard
from Client import ChatsKeyboard
from Client import DelayedMessageKeyboard
from Client import UserKeyboard

def register_handler_client():
    MenuKeyboard.register_handler_menu()
    ChatsKeyboard.register_handler_chats()
    DelayedMessageKeyboard.register_handler_delayed_message()
    UserKeyboard.register_handler_users()
