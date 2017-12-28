from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Server
import subprocess

# Index view (list of servers, add servers, delete servers)
def index(request):
    server_list = Server.objects.all()
    template = loader.get_template('mgr/index.html')
    context = {
        'server_list': server_list,
    }

    if request.method == 'POST':
        if request.POST['action'] == 'Add':
            server = Server(ip=request.POST['ip'], username=request.POST['username'], password=request.POST['password'])
            server.save()
            context['result'] = "Server added."

    return HttpResponse(template.render(context, request))

# Display server and boot options
def server(request, server_id):
    context = {}
    template = loader.get_template('mgr/server.html')

    try:
        server = Server.objects.get(id=server_id)
        context['server'] = server
    except:
        context['error'] = "An error has occured. Please check this server exists."

    if request.method == 'POST':
        if request.POST['action'] == 'Boot':
            command = 'chassis power on'
        elif request.POST['action'] == 'Reboot':
            command = 'chassis power cycle'
        elif request.POST['action'] == 'Reset':
            command = 'chassis power reset'
        elif request.POST['action'] == 'Shutdown':
            command = 'chassis power soft'
        elif request.POST['action'] == 'Power Off':
            command = 'chassis power off'
        else:
            command = ''
        result = subprocess.run(['ipmitool', '-I', 'lan', '-H', server.ip, '-U', server.username, '-P', server.password, command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode != 0:
            context['error'] = "An error has occured. Please check your settings and that ipmitool is installed."
            context['result'] = result.stdout.decode().strip()
        else:
            context['result'] = result.stdout.decode().strip()

    return HttpResponse(template.render(context, request))

# Delete the specified server_id
def delete(request, delete_id):
    try:
        server = Server.objects.get(id=delete_id)
    except:
        return redirect('index')

    if request.method == 'POST':
        if request.POST['action'] == 'Delete':
            server.delete()

    return redirect('index')
