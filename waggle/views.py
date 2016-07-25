from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import FormView, CreateView
from waggle.forms import CodeForm

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


class AssessmentView(generic.ListView):
    # ListView
    model = Assessment
    context_object_name = 'challenge_list'
    template_name = 'waggle/assessment.html'
    # vars that are added to context
    code_id=''
    submit_result = {}
    user_code = "# Type your python code here"

    def handleResult(self, pipeVals):
        stdout, stderr = pipeVals
        if not stderr:
            submission = str(stdout.decode('ASCII').rstrip())
            solution = str(Assessment.objects.get(id=int(self.code_id)).tests)
            if (submission == solution):
                return True
            return "STDOUT "+str(stdout.decode('ASCII'))
        return "STDERR "+str(stderr).decode('ASCII')

    def setupEnv(self, code, envFile):
        test_filename = os.path.dirname(os.path.abspath(envFile))+'/test.py'
        print(test_filename)
        # remove text editor crap from code
        with open(test_filename, "w") as outfile, open(envFile, 'r', encoding='utf-8') as infile:
                text = infile.read()
                text_with_code = re.sub('USERCODE', code, text)
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
            result = self.handleResult(result)
            self.submit_result = result
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(AssessmentView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['result'] = self.submit_result
        context['codefill'] = self.user_code
        return context




