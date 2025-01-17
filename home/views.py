import os
import time
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UploadFileForm
import tkinter
from tkinter import filedialog
current_dir = ""
old_dir = ""

def main(request):
    global current_dir, old_dir
    current_dir = ""
    return render(request, 'index.html')


def file_manager_view(request):
    global current_dir, old_dir
    """View to display and manage files."""
    form =""
    fs = FileSystemStorage()
    base_dir = '/home/ndk/Documents/ndkWeb/Media' + current_dir  # Replace with the actual directory
    old_dir = base_dir

    files=[]
    
    for f in os.listdir(base_dir):
        if os.path.isfile(os.path.join(base_dir, f)):
            a = f.split(".")
            tx = ""
            for x in a[:-1]:
                tx += x
            if len(tx) > 15: 
                b = tx[:13] + "vv" + "."+a[len(a)-1]
                sfile = base_dir + "/" + f
                des = base_dir + "/" + b
                if not os.path.exists(des): os.rename(sfile, des)
            else:
                b = f
            if a[len(a)-1] in ['png', 'jpg', 'jpeg', 'webp', 'gif', 'pdf']:
                type = 'image'
            elif a[len(a)-1] in ['exe', 'msi', 'bat']: 
                type = 'program'
            elif a[len(a)-1] in ['xlsx', 'csv']: 
                type = 'excel'
            elif a[len(a)-1] in ['zip', 'rar', '7z']: 
                type = 'zip'
            else: type = "nk"
            src = base_dir + "/" + b
            file_url = fs.url(src)
            file = {'file':b , 'type': type, 'source': file_url}
            files.append(file)
    # files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"], base_dir, files)
            return redirect('file_manager')
        else:
            form = UploadFileForm()
        if 'enter_folder' in request.POST: 
            if not os.path.isdir(base_dir + "/" +request.POST['enter_folder']): pass
            # else: current_dir += "/" + request.POST['enter_folder']
            else: current_dir += "/" + request.POST['enter_folder']
            return redirect('file_manager')
        elif 'return_home' in request.POST: 
            current_dir =""
            return redirect('file_manager')
        elif 'delete_file' in request.POST:
            file_name = request.POST['delete_file']
            file_path = os.path.join(base_dir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect('file_manager')
            
    # files = [f for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
    
    return render(request, 'file_manager/index.html', {'files': files,
                                                       'folders': folders,
                                                       'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_page')  # Redirect to the user page
            else:
                # Invalid login credentials
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def handle_uploaded_file(f, dir, files):
    filename = (f.name).split(".")
    index = 0
    fname = f.name
    for file in files:
        if f.name == file:
            fname = filename[0]
            index+=1
            for t in range(1,(len(filename)-1)):
                fname = fname + "." + filename[t]
            fname = fname + str(int(time.time())) + "." + filename[len(filename)-1]
            f.name = fname
        
    file_path = os.path.join(dir, fname)    
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
