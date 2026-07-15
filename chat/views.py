from django.shortcuts import render


def chat_room(request):
    """Chat sahifasini ko'rsatadi."""
    return render(request, 'chat/chat.html')
