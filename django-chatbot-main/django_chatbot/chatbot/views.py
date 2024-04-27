from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from openai import OpenAI;
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.http import HttpResponse
from django.utils import timezone



client = OpenAI(
    api_key="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"
)

chat_completion_0 = client.chat.completions.create(
    messages = [
        {
            "role": "system", 
            "content" : "Ты мой Гейм Мастер в настольной ролевой игре под названием DnD. Ты должен предлагать мне варианты возможных действий в разных игровых ситуациях. При этом веди повествование как старый рассказчик из книг.",
        },
        {
            "role": "user",
            "content": f'Меня зовут Арригал, я Маг-Эльф. Вот моя предистория: Я родом из деревени Кишки-на-ружу-ниндзя, мой отец Никита Малютин тяжело был поражен проклятьем СИШАРПА могучего демона. Мое единственное желание стать сильнее и отыскать эту нечисть, чтобы снять проклятье с моего отца!'
        }
    ],
    model="gpt-3.5-turbo",

)

print(chat_completion_0)

chat_response_0 = chat_completion_0.choices[0].message.content


def ask_openai(message):
    answer = ""
    response = client.chat.completions.create(
    messages = [
        {
            "role": "system", 
            "content" : "Ты мой Гейм Мастер в настольной ролевой игре под названием DnD. Используй систему DnD для проверок характеристик и навыков игрока где он будет бросать кубик 1к20, если выпало число меньше 10 происходит что-то плохое, если больше 10 то что-то хорошее. При этом каждое значение броска кубика ты должен прописывать. При этом веди повествование как старый рассказчик из книг. Мои соперники также бросают кубики пытаясь мне навредить и возможно даже убить",
        }, 
         {
            "role": "assistant", 
            "content" : chat_response_0,
        },
        {
            "role": "assistant", 
            "content" : answer,
        },
        {
            "role": "user",
            "content": message,
        }
    ],
    model="gpt-3.5-turbo",

)
    answer = response.choices[0].message.content
    message.append({
        "role": "assistant",
        "content": char_response
    })
    print(answer)
    return answer


def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')