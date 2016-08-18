from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import FormView, CreateView
from waggle.forms import CodeForm
from django.contrib.auth.models import User
from .models import Related, Content, Assessment, Module, Course, AssessmentProgress, ContentProgress,Student

from django.utils import timezone
from datetime import datetime
import subprocess
import re
import json
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

class LessonView(generic.DetailView):
    template_name = 'waggle/lesson.html'
    model = User

    """
    Constructor. Called in the URLconf; can contain helpful extra
    keyword arguments, and other things.
    """
    #module_id = self.kwargs.get('module')
    #assessments = Assessment.objects.filter(module_id=module_id)
    #contents = Content.objects.filter(module_id=module_id)
    #relateds = Related.objects.filter(module_id=module_id)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LessonView, self).get_context_data(**kwargs)
        module_id = self.kwargs.get('module')
        print('MODULE_ID ', module_id)
        context['module_obj'] = Module.objects.get(id=module_id)
        context['assessments'] =Assessment.objects.filter(module_id=module_id)
        context['contents'] =Content.objects.filter(module_id=module_id)
        context['relateds'] =Related.objects.filter(module_id=module_id)
        print(context.items())
        # set up progress data for student if it doesnt exist
        student_instance = context['object'].students
        for assessment_instance in context['assessments']:
            assessment_prog,created = student_instance.assessmentprogress_set.get_or_create(assessment=assessment_instance)
            print(assessment_prog,created)
            print(assessment_prog.errors_list)
        for content_instance in context['contents']:
            content_prog,created = student_instance.contentprogress_set.get_or_create(content=content_instance)
            print(content_prog,created)
        return context

    def setupEnv(self, code, envFile):
        test_filename = '/home/smccumsey/waggle-classroom/waggle/media/tmp/test.py'
        code_lines = code.splitlines()
        new_code = '\n\t#user submission'.expandtabs(4)+'\n'+'\n'.join(map(lambda s:('\t'+s).expandtabs(4),code_lines)) #lines after first must be indented
        print(new_code)
        with open(test_filename, "w") as outfile, open(envFile, 'r', encoding='utf-8') as infile:
            text = infile.read()
            text_with_code = re.sub('&&&', new_code, text,flags=re.M)
            text_with_code = re.sub('# paste user code here', '', text_with_code,flags=re.M)
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
        code_id = ([re.sub('code_id','',key) for key in postdata.keys() if 'code_id' in key])[0]
        print('POST DATA')
        print(postdata,code_id)
        if(request.POST.get('code_btn')):
            self.user_code = request.POST.get('code_id'+code_id)
            # grab file to assess user code
            envFile = Assessment.objects.get(id=int(code_id)).assess_file.path
            testFile = self.setupEnv(self.user_code, envFile)
            result_feedback = self.runCode(testFile)
            print('RESULT0',result_feedback)
            if result_feedback[0].decode('ASCII'):
                result_feedback  = json.dumps([ {k:str(v) for k,v in (eval(err)).items()} for err in result_feedback[0].decode('ASCII').splitlines()])
            elif result_feedback[1].decode('ASCII'):
                result_feedback = "bad"
            else:
                result_feedback = "good"
            print('RESULT1',result_feedback)
            assessment_progress = AssessmentProgress.objects.get(student=Student.objects.get(user=request.user), assessment=Assessment.objects.get(id=int(code_id)))
            assessment_progress.code_submission = self.user_code
            assessment_progress.errors_list = result_feedback
            assessment_progress.save()
        return self.get(request, *args, **kwargs)

class MenuView(generic.DetailView):
    template_name = 'waggle/menu.html'
    model=User

    # student_instance = user_instance.students
    # module_prog = ModuleProgress.create(student=student_instance)
    def get(self, request, *args, **kwargs):
        request.session['course_name'] = self.kwargs['course']
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MenuView, self).get_context_data(**kwargs)
        course_name = self.kwargs.get('course').replace('-', ' ')
        course_query = Course.objects.filter(name__icontains=course_name)
        context['modules'] = Module.objects.filter(course_id=course_query.get().id)
        return context

class ProfileView(generic.DetailView):
    template_name = 'waggle/profile.html'
    model = User

    # student_instance = user_instance.students
    # course_prog = CourseProgress.create(student=student_instance)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context

class GoogleView(generic.TemplateView):
    template_name = 'waggle/google8a43fbed4f8a62b6.html'

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
                return render(request, 'waggle/profile.html')#`, {'user': user})
                # Redirect to a success page.
            else:
                print('bar')
                # Return a 'disabled account' error message
        else:
            print('baz')
            # Return an 'invalid login' error message.

'''
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
'''

