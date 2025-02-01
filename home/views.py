import os
import time
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.files.storage import FileSystemStorage
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Document
from .forms import DocumentForm, UploadFileForm


current_dir = ""
old_dir = ""
user_page = "home"
is_authenticated = False
def main(request):
    global current_dir, old_dir, is_authenticated
    if not request.user.is_authenticated: is_authenticated = False
    else: is_authenticated = True
    print(is_authenticated)
    current_dir = ""
    return render(request, 'index.html', {'authenticated': is_authenticated})


def file_manager_view(request):
    global current_dir, old_dir, user_page
    user_page = 'file_manager'
    if not request.user.is_authenticated:
        return redirect('login')
    """View to display and manage files."""
    form =""
    fs = FileSystemStorage()
    base_dir = os.path.join(Path(__file__).resolve().parent.parent, "Media") + current_dir
    
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
            file = {'file':b , 'type': type, 'source': file_url, 'url': src}
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
        elif 'download_file' in request.POST:
            file_id = request.POST['download_file']
            # file_path = os.path.join(base_dir, file_name)
            file_object = get_object_or_404(pk=file_id) 
            try:
                with open(file_object.file.path, 'rb') as f:  # Open the file in binary mode for reading
                    response = HttpResponse(f.read(), content_type="application/force-download")
                    response['Content-Disposition'] = 'attachment; filename="%s"' % file_object.file.name
                    return response
            except FileNotFoundError:
                raise Http404("File not found.") 
            
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
                return redirect(user_page)  # Redirect to the user page
            else:
                # Invalid login credentials
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated == True:
        username = request.user.username
    else:
        username = None
    if username != None:
        logout(request)
        return redirect('home')

def registry_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(user_page)  # Redirect to the user page
            else:
                # Invalid login credentials
                form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/registry.html')


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


# def document_list(request):
#     documents = Document.objects.all()
#     return render(request, 'Documents/document_list.html', {'documents': documents,
#                                                             'authenticated': is_authenticated})

def document_list(request):
    global is_authenticated, user_page
    user_page = "document_list"
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_authenticated: is_authenticated = False
    else: is_authenticated = True
    base_dir = os.path.join(Path(__file__).resolve().parent.parent, "Media") + "/Documents"
    documents = []
    urls = []
    for f in os.listdir(base_dir):
        if os.path.isfile(os.path.join(base_dir, f)):
            documents.append({'file':f,'url': os.path.join(base_dir, f)})
    return render(request, 'Documents/document_list.html', {'documents': documents,
                                                            'authenticated': is_authenticated,})

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form)
            print("form save")
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'Documents/upload_document.html', {'form': form})

def delete_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    document.delete()
    return redirect('document_list')