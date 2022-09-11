from django.shortcuts import render, redirect
import datetime
import time
import os
import shutil
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, HttpResponse
from django.views.generic import DetailView, ListView, UpdateView, DeleteView,CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Player
import cv2
import easyocr
import difflib


def table(request):
    players = Player.objects.all()

    data = {
        'title':'Главная',
        'players' : players,

        }
    return render(request, 'table/table.html', data)


def archive(request):
    data = {
        'title':'Архив',
        }
    return render(request, 'table/table.html', data)


def add_image(request):
    if request.method == 'POST':
        try:
            nicknames_dict = {}
            loaded_image = request.FILES.getlist('load_image')
            for image in loaded_image:
                shutil.rmtree('media/tmp')
                default_storage.save('tmp/image.png', ContentFile(image.read()))
                files = os.listdir(path = 'media/tmp')
                img = cv2.imread(f'media/tmp/{files[0]}')
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                text = easyocr.Reader(['en'], gpu = True)
                text = text.readtext(gray, allowlist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
                for i in text:
                    try:
                        if i[-2].isdigit():
                            pass
                        else:
                            if i[-2] in nicknames_dict.keys():
                                nicknames_dict[f'{i[-2]}'] = nicknames_dict[f'{i[-2]}']+1
                            else:
                                nicknames_dict[f'{i[-2]}'] = 1
                    except Exception as e:print(e)
            request.session['nicknames_dict'] = nicknames_dict
            return redirect(add_data)
        except Exception as e:print(e)

    data = {
        'title':'Добавление скриншотов',
        }
    return render(request, 'table/add_image.html', data)


def add_data(request):
    nicknames_dict = request.session.get('nicknames_dict', '')
    db_nicknames = Player.objects.all()
    db_nicknames_list = [x.nickname for x in db_nicknames]
    list_for_pop = []
    dict_for_add = {}
    for nick in nicknames_dict.keys():
        n = 3
        if len(nick) > 5:
            n = len(nick)-3
        diff = difflib.get_close_matches(nick, db_nicknames_list, n)
        if len(diff) > 0:
            if diff[0] == nick:
                continue
            elif diff[0] in nicknames_dict.keys():
                if diff[0] != nick:
                    nicknames_dict[diff[0]] = nicknames_dict[diff[0]] + nicknames_dict[nick]
                    list_for_pop.append(nick)
            else:
                if diff[0] != nick:
                    dict_for_add[diff[0]] = nicknames_dict[nick]
                    list_for_pop.append(nick)
    for i in list_for_pop:
        nicknames_dict.pop(i)
    nicknames_dict.update(dict_for_add)
    if nicknames_dict == {}:
        return redirect(add_image)
    else:
        if request.method == 'POST':
            try:
                request.session['nicknames_dict'] = {}
                select_activity = request.POST.get('inlineRadioOptions')
                for nick in nicknames_dict.keys():
                    new_nick = request.POST.get(nick)
                    if new_nick == '':
                        continue
                    try:
                        player_exist = Player.objects.get(nickname = new_nick)
                        if select_activity == "gangs":
                            player_exist.gangs = player_exist.gangs + nicknames_dict[nick]
                        elif select_activity == "forts":
                            player_exist.forts = player_exist.forts + nicknames_dict[nick]
                        elif select_activity == "fights":
                            player_exist.fights = player_exist.fights + nicknames_dict[nick]
                        elif select_activity == "zvz":
                            player_exist.zvz = player_exist.zvz + nicknames_dict[nick]
                        player_exist.save()
                    except Player.DoesNotExist:
                        try:
                            player = Player(nickname = new_nick)
                            if select_activity == "gangs":
                                player.gangs = nicknames_dict[nick]
                            elif select_activity == "forts":
                                player.forts = nicknames_dict[nick]
                            elif select_activity == "fights":
                                player.fights = nicknames_dict[nick]
                            elif select_activity == "zvz":
                                player.zvz = nicknames_dict[nick]
                            player.save()
                        except Exception as e:print(e)
            except Exception as e:print(e)
            return redirect(table)
        data = {
            'db_nicknames_list' : db_nicknames_list,
            'nicknames_dict' : nicknames_dict,
            'title':'Добавление данных',
            }
    return render(request, 'table/add_data.html', data)


def edit_data(request):
    data = {
        'title':'Редактирование данных',
        }
    return render(request, 'table/edit_data.html', data)
