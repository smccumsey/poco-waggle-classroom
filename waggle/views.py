from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import FormView, CreateView
from waggle.forms import CodeForm
from django.contrib.auth.models import User
from .models import Assessment, Module, Course

from django.utils import timezone
import subprocess
import re
import imp
import ntpath
from importlib.machinery import SourceFileLoader
import os
import sys
import subprocess
from shutil import copyfile
from django.template import RequestContext
from oauth2client import client, crypt
from django.conf import settings
from django.contrib.auth.decorators import login_required

import os
import logging
import httplib2
from django.contrib.auth import login, authenticate



class GoogleView(generic.TemplateView):
    template_name = 'waggle/google8a43fbed4f8a62b6.html'

class ProfileView(generic.DetailView):
    template_name = 'waggle/profile.html'
    model = User
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        c = super(ProfileView, self).get_context_data(**kwargs)
        user = self.request.user
        print('session: ',self.request.session.items())
        if User.objects.get(pk=int(self.request.session['_auth_user_id'])) != user:
            print('ERROR WRONG USER')
        return c

class LoginView(generic.TemplateView):
    template_name = 'waggle/login.html'

    def post(self, request, *args, **kwargs):
        usr_token = request.POST.get('idtoken')
        user = authenticate(token=usr_token)
        print("USERID!",user)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('foo')
                return render(request, 'waggle/profile.html', {'user': user})
                # Redirect to a success page.
            else:
                print('bar')
                # Return a 'disabled account' error message
        else:
            print('baz')
            # Return an 'invalid login' error message.

class AssessmentView(generic.ListView):
    # ListView
    model = Assessment
    context_object_name = 'challenge_list'
    template_name = 'waggle/assessment.html'
    # vars that are added to context
    code_id=''
    name = {}
    short_desc = {}
    long_desc = {}
    user_code = ''

    def handleResult(self, pipeVals):
        stdout, stderr = pipeVals
        if not stderr:
            if ('CORRECT' in stdout.decode('ASCII')):
                self.name = 'CORRECT'
                self.short_desc = 'answer == solution -> True' 
                self.long_desc = stdout.decode('ASCII') 
                return 
            self.name = 'INCORRECT'
            self.short_desc = 'answer == solution -> False' 
            self.long_desc = stdout.decode('ASCII') 
            return 
        self.name = 'ERROR'
        self.short_desc = ([word[:-1] for word in str(stderr.decode('ASCII')).split() if 'Error' in word])
        self.long_desc = "STDERR "+str(stderr.decode('ASCII'))
        return 

    def setupEnv(self, code, envFile):
        test_filename = os.path.dirname(os.path.abspath(envFile))+'/test.py'
        print(test_filename)
        # remove text editor crap from code
        with open(test_filename, "w") as outfile, open(envFile, 'r', encoding='utf-8') as infile:
            text = infile.read()
            text_with_code = re.sub('&&&', code, text)
            outfile.write(text_with_code)
        return test_filename

    def runCode(self, fname):
        try:
            p = subprocess.Popen('python '+fname, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            return p.communicate()  # this gets you pipe values
        except Exception as e:
            return 'error'+e
        else:
            return "else"

    def post(self, request, *args, **kwargs):
        postdata = request.POST.dict()
        self.code_id = ([re.sub('code_id','',key) for key in postdata.keys() if 'code_id' in key])[0]
        if(request.POST.get('code_btn')):
            self.user_code = request.POST.get('code_id'+self.code_id)
            # lookup challenge environment
            envFile = Assessment.objects.get(id=int(self.code_id)).soln.name
            testFile = self.setupEnv(self.user_code, envFile)
            result = self.runCode(testFile)
            self.handleResult(result)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AssessmentView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['name'] = self.name
        context['short_desc'] = self.short_desc
        context['long_desc'] = self.long_desc
        context['codefill'] = self.user_code
        return context




