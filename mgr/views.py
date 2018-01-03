from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Server
from shlex import quote
import subprocess
import socket

# Index view (list of servers, add servers, delete servers)
def index(request):
    server_list = Server.objects.all()
    template = loader.get_template('mgr/index.html')
    context = {
        'server_list': server_list,
    }

    # See if we're adding a server
    if request.method == 'POST':
        if request.POST['action'] == 'Add':
            # Ip validation
            try:
                socket.inet_aton(request.POST['ip'])
            except:
                context['error'] = 'Invalid ip.'
                return HttpResponse(template.render(context, request))

            # Username/password validation
            if request.POST['username'].isalnum() and request.POST['password'].isalnum():
                # Save if we're good
                server = Server(ip=request.POST['ip'], username=request.POST['username'], password=request.POST['password'])
                server.save()
                context['result'] = "Server added."
            else:
                # Invalid username or password
                context['error'] = 'Invalid username or password.'

    return HttpResponse(template.render(context, request))

# Display server and boot options
def server(request, server_id):
    context = {}
    template = loader.get_template('mgr/server.html')

    # Check if this server exists
    try:
        server = Server.objects.get(id=server_id)
        context['server'] = server
    except:
        context['error'] = "An error has occured. Please check this server exists."

    # Check if we're doing anything to this server
    if request.method == 'POST':
        if request.POST['action'] == 'Status':
            command = 'chassis power status'
        elif request.POST['action'] == 'Boot':
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

        # Quote out our arguments to avoid injecting anything nasty
        ip = quote(server.ip);
        username = quote(server.username);
        password = quote(server.password);

        # subprocess.run() will throw an exception if ipmitool isn't found
        try:
            result = subprocess.run(['ipmitool', '-I', 'lan', '-H', ip, '-U', username, '-P', password, command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except:
            context['error'] = "An error has occured. Please check that ipmitool is installed."
            return HttpResponse(template.render(context, request))

        # Otherwise return output on success or failure
        if result.returncode != 0:
            context['error'] = "An error has occured. Please check your settings."
            context['result'] = result.stdout.decode().strip()
        else:
            context['result'] = result.stdout.decode().strip()

    return HttpResponse(template.render(context, request))

# Delete the specified server_id
def delete(request, delete_id):
    # If it doesn't exist just return to
    try:
        server = Server.objects.get(id=delete_id)
    except:
        return redirect('index')

    # Otherwise delete and go back to the list/main page
    if request.method == 'POST':
        if request.POST['action'] == 'Delete':
            server.delete()

    return redirect('index')
