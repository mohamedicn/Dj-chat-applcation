from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from accounts.models import Profile,Friend
# Create your views here.
from django.shortcuts import get_object_or_404
from.models import ChatMessage
from django.db.models import Q
from itertools import chain
from django.urls import reverse
import json

def home(request):
    if request.user.is_authenticated:
        return redirect('/chat')
    return render(request,'chat/index.html',)

def main(request):
    profile = get_object_or_404(Profile, user=request.user)
    friends = profile.friend.all()
    return render(request,'chat/chat.html',{'profile': profile, 'friends': friends})

def chat_details(request,slug):
    profile=get_object_or_404(Profile,slug=slug)
    user_profile = get_object_or_404(Profile, user=request.user)
    msg_sender = ChatMessage.objects.filter(
        (Q(msg_sender=profile) & Q(msg_receiver=user_profile))
    ).order_by('send_in')
    msg_receiver = ChatMessage.objects.filter(
        (Q(msg_sender=user_profile) & Q(msg_receiver=profile))
    ).order_by('send_in')
    all_messages = sorted(chain(msg_sender, msg_receiver), key=lambda x: x.send_in)
    if request.method == 'POST' and 'send' in request.POST:
        chat_body = request.POST['chat_body']
        chat_text=ChatMessage.objects.create(
                                        msg_sender=user_profile,
                                        body=chat_body,
                                        msg_receiver=profile,
                                            )
        chat_text.save()
        return redirect(reverse('chat:chat_details', kwargs={'slug': profile.slug}))



    return render(request,'chat/chat_details.html',{'profile': profile,'user_profile': user_profile,'all_messages': all_messages})

def send_message(request,slug):
    profile=get_object_or_404(Profile,slug=slug)
    user_profile = get_object_or_404(Profile, user=request.user)
    data=json.loads(request.body)
    chat_body = data["msg"]
    chat_text=ChatMessage.objects.create(
                                        msg_sender=user_profile,
                                        body=chat_body,
                                        msg_receiver=profile,
                                            )
    chat_text.save()
    response_data = {
        'msg': chat_body,
        'send_in': chat_text.send_in,  # Assuming you have a 'timestamp' field in ChatMessage
        'avatar_url': user_profile.image.url if user_profile.image else '',  # Update accordingly
    }

    return JsonResponse(response_data, safe=False)
from django.core.serializers import serialize
def receive_message(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    user_profile = get_object_or_404(Profile, user=request.user)
    
    # arr =[]
    # Filter messages where the sender is the other user and the receiver is the current user
    msg_receiver = ChatMessage.objects.filter(
        Q(msg_sender=profile) & Q(msg_receiver=user_profile)
    ).order_by('send_in')
    serialized_messages = serialize('json', msg_receiver, fields=('send_in', 'body', 'msg_sender__image'))

    # Deserialize the data to manipulate the structure
    data = json.loads(serialized_messages)
    arr = []

    for entry in data:
        fields = entry['fields']
        send_in = fields.get('send_in', '')  # Get the timestamp or an empty string if not present

        # Build a dictionary with the desired structure
        message_data = {
            'body': fields.get('body', ''),
            'send_in': send_in,
            'avatar_url': profile.image.url if profile.image else '', 
        }

        arr.append(message_data)

    return JsonResponse(arr, safe=False)


def friend_request(request,slug):
    profile = get_object_or_404(Profile, user=request.user)
    friend_requests = profile.friend_request.all()
    return render(request,'chat/friend_request_list.html',{'friend_requests': friend_requests})


def add_friend(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    friend=user_profile.friend.all()
    add_friends = Friend.objects.all().exclude(profile=request.user.profile)
    return render(request,'chat/add_friend.html',{'add_friends': add_friends})

def send_request(request,slug):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)
        profile=get_object_or_404(Profile,slug=slug)
        profile.friend_request.add(user_profile.friend_profile)
        profile.save()
    return redirect('/add_friend/')


def accecpt_friend_request(request,slug):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(Profile, user=request.user)
        profile=get_object_or_404(Profile,slug=slug)
        profile.friend.add(user_profile.friend_profile)
        user_profile.friend.add(profile.friend_profile)
        user_profile.friend_request.remove(profile.friend_profile)
        user_profile.save()
        profile.save()
    return redirect('/')