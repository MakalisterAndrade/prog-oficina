from django.urls import path

from chat.views import chat_view, send_message

urlpatterns = [
    path("chat/", chat_view, name="chat_list"),
    path("chat/send-message", send_message, name="chat_send_message")
]