from django.shortcuts import render, redirect,get_object_or_404
from .models import Post, Comment, UserProfile, FriendRequest,Message,ChatRoom,MembershipRequest,ChatMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from .forms import CustomUserCreationForm, EditProfileForm, PostForm, MessageForm
from my_messages.models import Message

User = get_user_model()

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'signin.html', {'error_message': 'Invalid credentials'})

    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            UserProfile.objects.create(user=user)
            # Set the backend attribute on the user object
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def follow(request, username):
    target_user = get_object_or_404(User, username=username)
    target_user_profile = target_user.userprofile
    current_user = request.user
    current_user_profile = current_user.userprofile

    if target_user not in current_user_profile.followers.all():
        current_user_profile.followers.add(target_user)
        action = 'followed'
    else:
        current_user_profile.followers.remove(target_user)
        action = 'unfollowed'

    return JsonResponse({'action': action, 'username': username})

@login_required
def is_following(request, username):
    target_user = get_object_or_404(User, username=username)
    current_user = request.user
    current_user_profile = current_user.userprofile

    is_following = target_user in current_user_profile.followers.all()

    return JsonResponse({'is_following': is_following})


def send_friend_request(request, username):
    if request.method == 'POST':
        sender = request.user
        receiver = get_object_or_404(User, username=username)
        friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
        return JsonResponse({'sent': created})

def accept_friend_request(request, request_id):
    if request.method == 'POST':
        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
        # Implement logic to add users as friends
        sender_profile = UserProfile.objects.get(user=friend_request.sender)
        receiver_profile = UserProfile.objects.get(user=friend_request.receiver)

        sender_profile.friends.add(friend_request.receiver)
        receiver_profile.friends.add(friend_request.sender)
        friend_request.delete()
        return JsonResponse({'status': 'accepted'})

def decline_friend_request(request, request_id):
    if request.method == 'POST':
        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
        friend_request.delete()
        return JsonResponse({'status': 'declined'})








@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user.userprofile)
    return render(request, 'edit_profile.html', {'form': form})



def add_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        text = request.POST['text']
        comment = Comment(post=post, user=request.user, text=text)
        comment.save()
        return redirect('index')

def home(request):
    
    posts = Post.objects.select_related("user__userprofile").all()
    return render(request, "index.html", {"posts": posts})
def photo(request):
    return render(request,"photo.html")
def base(request):
    return render(request,"base.html")

def profile(request, username):

    
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(user=user).order_by('-created_at')
    context = {
        'user_posts': user_posts,
        'profile_user': user,
    }
    return render(request, 'profile.html', context)

def chat(request):
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user)
    friends = user_profile.friends.all()

    context = {
        'friends': friends,
    }

    return render(request, 'chat.html', context)

def create(request):
    return render(request,"create.html")


def rooms(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request,"rooms.html",{'chat_rooms': chat_rooms})


def notifications(request):
    return render(request,"notifications.html")



def dm(request, friend_username):
    friend = get_object_or_404(User, username=friend_username)
    room_name = f"{request.user.id}_{friend.id}"
    print("Room name:", room_name)

    messages = Message.objects.filter(sender=request.user, recipient=friend) | Message.objects.filter(sender=friend, recipient=request.user)
    messages = messages.order_by('timestamp')
    print("Messages:", messages)

    return render(request, 'dm.html', {'room_name': room_name, 'friend': friend, 'messages': messages})


def create_chat_room(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES['image']
        is_private = 'is_private' in request.POST

        chat_room = ChatRoom(
            name=name,
            description=description,
            image=image,
            is_private=is_private,
            owner=request.user
        )
        chat_room.save()
        return redirect('rooms')

    return render(request, 'create_room.html')


def chat_room(request, chat_room_id):
    chat_room = get_object_or_404(ChatRoom, pk=chat_room_id)
    messages = ChatMessage.objects.filter(chat_room=chat_room).order_by('timestamp')
    form = MessageForm()

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_room = chat_room
            message.user = request.user
            message.save()
            return redirect('chat-room', chat_room_id=chat_room_id)

    return render(request, 'chat_room.html', {'chat_room': chat_room, 'messages': messages, 'form': form})

def logout_view(request):
    logout(request)
    return redirect('signin')