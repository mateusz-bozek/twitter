from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.views import View

from workshop.models import Tweet, Message, Comment
from .forms import AddTweetForm, LoginForm, AddCommentForm


@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html', {
        'tweets': Tweet.objects.filter(disabled=False).order_by('-creation_date')
    })


@login_required(login_url='/login')
def user(request):
    return render(request, 'home.html', {
        'tweets': Tweet.objects.filter(disabled=False, user=request.user).order_by('-creation_date')
    })


@login_required(login_url='/login')
def messages(request):

    sent_by_me = Message.objects.filter(disabled=False, sender=request.user)
    received_by_me = Message.objects.filter(disabled=False, receiver=request.user).exclude(sender=request.user)

    result = render(request, 'messages.html', {
        'sent_by_me': sent_by_me.order_by('-creation_date'),
        'received_by_me': received_by_me.order_by('-creation_date'),
    })

    for message in received_by_me:
        message.seen = True
        message.save()

    return result


class AddTweet(LoginRequiredMixin, View):

    # TODO display only for logged in users
    def get(self, request):
        form = AddTweetForm()
        return render(request, 'add_tweet.html', {'form': form})

    # TODO display only for logged in users
    def post(self, request):
        tweet = Tweet(user=request.user)
        form = AddTweetForm(request.POST, instance=tweet)
        if form.is_valid():
            tweet = form.instance
            tweet.save()
            return redirect('/')
        else:
            ...  # TODO handle errors


class LoginView(View):

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('/')

        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return redirect('/')
        else:
            return render(request, 'login.html', {'form': form})


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/login')


class CommentsView(LoginRequiredMixin, View):

    def get(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, pk=tweet_id)
        comments = Comment.objects.filter(disabled=False, tweet=tweet).order_by('creation_date')
        return render(request, 'comments.html', {
            'tweet': tweet,
            'comments': comments,
            'form': AddCommentForm()
        })

    def post(self, request):
        ...
