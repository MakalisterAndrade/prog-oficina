from django.shortcuts import render
from django.http import JsonResponse

from .models import Message


def chat_view(request):
    messages = Message.objects.all().order_by('-created_at')
    return render(request, 'chat.html', {'messages': messages})


def send_message(request):
    sender = request.user.username
    recipient = request.POST.get('recipient')
    message = request.POST.get('message')

    # Cria uma nova mensagem
    message_obj = Message(sender=sender, recipient=recipient, message=message)
    message_obj.save()

    # Envia a lista de mensagens atualizadas ao navegador
    messages = list(Message.objects.values().order_by('-created_at'))
    return JsonResponse({'messages': messages})