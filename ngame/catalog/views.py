from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def home(request):
    games = Game.objects.all()
    return render(request, 'catalog/home.html', {'games': games})

def index(request):
    user = request.user 
    game = Game.objects.all()
    data_game = []
    for games in game:
        data_game.append(    
            {
            'games': games,
            'liked': games.user_liked(user) if user.is_authenticated else False,
            'comments': Comment.objects.filter(game=games)
            }
        )
    return render(request, 'catalog/index.html', {'games': data_game})

@login_required
def like_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    like, created = Like.objects.get_or_create(user=request.user, game=game)
    if not created:
        like.delete()
    return redirect('index')

@login_required
def comment_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(user=request.user, game=game, content=content)
    return redirect('index')

# @login_required
# def detail_game(request, game_id):
#     game = get_object_or_404(Game, id=game_id)
#     comments = Comment.objects.filter(game=game)
#     liked = False
#     if request.user.is_authenticated:
#         liked = Like.objects.filter(user=request.user, game=game).exists()
#     return render(request, 'catalog/detail_clothing.html', {'game': game, 'comments': comments, 'liked': liked})

@login_required
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogo cadastrado com sucesso!')
            return redirect('home')
    else:
        form = GameForm()
    return render(request, 'catalog/add_game.html', {'form': form})

@login_required
def edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jogo editado com sucesso!')
            return redirect('home')
    else:
        form = GameForm(instance=game)
    return render(request, 'catalog/edit_game.html', {'form': form})

@login_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    if request.method == 'POST':
        game.delete()
        messages.success(request, 'jogo deletado com sucesso!')
        return redirect('home')
    return render(request, 'catalog/delete_game.html', {'game': game})