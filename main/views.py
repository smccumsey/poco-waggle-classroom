from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse,HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.models import User
from .models import Related, Content, Assessment, Module, Course, Video, Student, AssessmentSubmission
from .models import ContentProgress, AssessmentProgress, VideoProgress, CourseProgress, ModuleProgress

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
from django.template.defaultfilters import slugify
from django.forms.models import model_to_dict

class LessonView(generic.DetailView):
    from django.template.defaultfilters import slugify
    template_name = 'main/lesson.html'
    model = User

    """
    Constructor. Called in the URLconf; can contain helpful extra
    keyword arguments, and other things.
    """
    #module_id = self.kwargs.get('module')
    #assessments = Assessment.objects.filter(module_id=module_id)
    #contents = Content.objects.filter(module_id=module_id)
    #relateds = Related.objects.filter(module_id=module_id)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        print("REQUEST SESSION", request.session.items())
        print("GET context", context.items())
        #if not request.session.get('approved'):
            #return HttpResponseNotFound("<br/><br/><h1 style='text-align:center;vertical_align:middle;'>Please sign-in to <a href='http://smccumsey.pythonanywhere.com/main/login/'>Poco<a> to access this page</h1>")
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LessonView, self).get_context_data(**kwargs)
        module_id = int(self.kwargs.get('module'))
        print('MODULE_ID ', module_id)
        context['module_obj'] = Module.objects.get(id=module_id)
        context['assessments'] =Assessment.objects.filter(module_id=module_id).order_by('order')
        context['contents'] =Content.objects.filter(module_id=module_id)
        context['videos'] =Video.objects.filter(module_id=module_id)
        context['relateds'] =Related.objects.filter(module_id=module_id)
        print(context.items())
        print("VERSION", sys.version)
        # set up progress data for student if it doesnt exist
        student_instance = context['object'].students
        for content_instance in context['contents']:
            content_prog,created = student_instance.contentprogress_set.get_or_create(content=content_instance)
            print(content_prog,created)
        for assessment_instance in context['assessments']:
            assessment_prog,created = student_instance.assessmentprogress_set.get_or_create(assessment=assessment_instance)
            print(assessment_prog,created)
        for video_instance in context['videos']:
            video_prog,created = student_instance.videoprogress_set.get_or_create(video=video_instance)
            print(video_prog,created)
        return context

    def setupEnv(self, code, envFile, username):
        #directory = '/home/smccumsey/waggle-classroom/main/media/user_{}_tmp_dir'
        #test_filename = '/home/smccumsey/waggle-classroom/main/media/user_{}_tmp_dir/test.py'.format(username)
        test_filename = '/home/smccumsey/waggle-classroom/main/media/user_{}.py'.format(username)
        code_lines = code.splitlines()
        first_line = (code_lines[0]).expandtabs(0) 
        if len(code_lines)>1:
            other_lines = code_lines[1:]
            new_code = first_line+ "\n"+'\n'.join(map(lambda s:('\t'+s).expandtabs(8),other_lines)) #lines after first must be indented
        else: 
            new_code = first_line
        print("USER CODE AFTER SETUP: {}".format(new_code))
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
        print('POST DATA: {}'.format(postdata))
        if(request.POST.get('video_click')):
            videoID = request.POST.get('videoID')
            my_student = Student.objects.get(user=request.user) 
            my_video = Video.objects.get(id=int(videoID))
            video_progress = VideoProgress.objects.get(student=my_student, video=my_video)
            video_progress.clicks_on_video_open_counter = video_progress.clicks_on_video_open_counter + 1
            video_progress.save()
            return HttpResponse('django says the video click was recorded')
        elif(request.POST.get('content_click')):
            contentID = request.POST.get('contentID')
            my_student = Student.objects.get(user=request.user) 
            my_content = Content.objects.get(id=int(contentID))
            content_progress = ContentProgress.objects.get(student=my_student, content=my_content)
            content_progress.clicks_on_content_tab_counter = content_progress.clicks_on_content_tab_counter + 1
            content_progress.save()
            return HttpResponse('django says the content click was recorded')
        elif(request.POST.get('html_notes')):
            updated_note_table = request.POST.get('html_notes')
            videoID = request.POST.get('videoID')
            video_timepoint = request.POST.get('time')
            print("VIDEOID=%s,\t HTML_NOTES: %s" % (videoID, updated_note_table))
            my_student = Student.objects.get(user=request.user) 
            my_video = Video.objects.get(id=int(videoID))
            video_progress = VideoProgress.objects.get(student=my_student, video=my_video)
            video_progress.video_notes = updated_note_table
            video_progress.video_timepoint= video_timepoint
            video_progress.save()
            return HttpResponse('django says the note was saved')
        elif(request.POST.get('submittedcode')):
            usr_code = request.POST.get('submittedcode')
            #if re.search(r'print\(.+\)', usr_code) or re.search(r'plt.show\(.+\)', usr_code):
            if re.search(r'print\(.+\)', usr_code) or re.search(r'plt.show\(.+\)', usr_code):
                parsed_result_feedback = "Print and show are disabled in assessment submissions. Please practice using these in your notebooks."
                return HttpResponse(parsed_result_feedback)
            assessmentID = request.POST.get('assessmentID')
            print('USER CODE: {}'.format(usr_code))
            print('ASSESSMENT ID: {}'.format(usr_code, assessmentID))
            envFile = Assessment.objects.get(id=int(assessmentID)).assess_file.path
            testFile = self.setupEnv(usr_code, envFile, request.user)
            result_feedback = list(map(lambda x: x.decode('ASCII'), self.runCode(testFile)))
            print('RAW RESULT: {}'.format(result_feedback))
            if result_feedback[0]: #stdout
                print("STDOUT")
                out_string = result_feedback[0]
                def parseLong(err):
                    span = re.search('Long.+}', err).span()
                    old = err[(span[0]+7):(span[1]-1)]
                    #print("LONG ERR0",old)
                    if "Error(" in old:
                        new = repr(old)[1:-1].replace("\'","*").replace("\"","`")
                        #print("LONG ERR1",new)
                        return(err.replace(old, "'"+new+"'"))
                    return err
                    
                out_string = [parseLong(err) for err in out_string.splitlines()]
                #print(out_string)
                parsed_result_feedback  = json.dumps([ {k:v for k,v in (eval(err)).items()} for err in out_string])
            elif result_feedback[1]: #stderr
                print("STERR")
                error_string = result_feedback[1]
                name = "Error"
                shortd = [x for x in error_string.split() if 'Error' in x].pop()[:-1]
                longd =  error_string[(error_string.find(shortd)):-1] #+ error_string[(error_string.find('\n')):(error_string.find(shortd))] 
                if 'Indentation' in shortd:
                    name = 'Indentation error'
                    shortd = 'Make sure you are using tabs for indentation, and not spaces.'
                
                feedback = {"Name":name, "Short":shortd, "Long":longd}
                parsed_result_feedback = json.dumps([feedback])
            else:
                parsed_result_feedback = "good"
            print('PARSED RESULT: {}'.format(parsed_result_feedback))
            assessment_progress = AssessmentProgress.objects.get(student=Student.objects.get(user=request.user), assessment=Assessment.objects.get(id=int(assessmentID)))
            assessment_progress.code_submission = usr_code
            assessment_progress.errors_list = parsed_result_feedback
            assessment_progress.attempted = True
            assessment_progress.number_of_attempts = assessment_progress.number_of_attempts+1
            if parsed_result_feedback == 'good':
                assessment_progress.solved = True
            assessment_progress.save()
            ap_record = str(model_to_dict(assessment_progress))
            AssessmentSubmission.objects.create(submission_record = ap_record)
            return HttpResponse(parsed_result_feedback)
        return self.get(request, *args, **kwargs)

class MenuView(generic.DetailView):
    template_name = 'main/menu.html'
    model=User

    # student_instance = user_instance.students
    # module_prog = ModuleProgress.create(student=student_instance)
    def get(self, request, *args, **kwargs):
        request.session['course_title'] = self.kwargs['course']
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        studentId = context['user'].students.id
        courseId = context['course_obj'].id
        print("REQUEST SESSION", request.session.items())
        print(studentId, courseId)
        print(CourseProgress.objects.all().values())
        print("GET context", context.items())
        if not (CourseProgress.objects.filter(student_id=studentId, course_id=courseId,approved=True)):
            request.session['approved'] = False
            return HttpResponseNotFound("<br/><br/><h1 style='text-align:center;vertical_align:middle;'>Please register for the course to access this page</h1>")

        request.session['approved'] = True
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MenuView, self).get_context_data(**kwargs)
        courses = [(slugify(c.title),c) for c in Course.objects.all()]
        course_title= self.kwargs.get('course')
        course_lookup = [c[1] for c in courses if c[0]==course_title].pop() #sloppy

        context['course_obj'] = course_lookup
        context['modules'] = Module.objects.filter(course_id=course_lookup.id)
        # setup module progress for student
        student_instance = context['object'].students
        for module_instance in context['modules']:
            module_prog,created = student_instance.moduleprogress_set.get_or_create(module=module_instance)

        return context

    def post(self, request, *args, **kwargs):
        print("UPDATE MODULE PROGRESS", request.POST.dict())
        if request.POST.get('changeButton'):
            moduleID = request.POST.get('moduleID')
            # update module progress
            module_progress = ModuleProgress.objects.get(student=Student.objects.get(user=request.user), module=Module.objects.get(id=int(moduleID)))
            module_progress.started = True
            module_progress.save()
            return HttpResponse("module progress has been saved with started=True")
        return HttpResponse("post received, no action taken by django")

class ProfileView(generic.DetailView):
    template_name = 'main/profile.html'
    model = User

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        request.session['approved'] = False
        print("REQUEST SESSION", request.session.items())
        print("GET context", context.items())
        return self.render_to_response(context)
    # student_instance = user_instance.students
    # course_prog = CourseProgress.create(student=student_instance)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        # setup course progress for student
        student_instance = context['object'].students
        for course_instance in context['courses']:
            course_prog,created = student_instance.courseprogress_set.get_or_create(course=course_instance)
        return context


class GoogleView(generic.TemplateView):
    template_name = 'main/google8a43fbed4f8a62b6.html'

class LoginView(generic.TemplateView):
    template_name = 'main/login.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        request.session['approved'] = False
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        usr_token = request.POST.get('idtoken')
        user = authenticate(token=usr_token)
        print("USERID!",user,user.pk)
        if user is not None:
            if user.is_active:
                login(request, user)
                print('foo')
                return HttpResponse(json.dumps({'pk':user.pk}))

                # Redirect to a success page.
            else:
                print('bar')
                # Return a 'disabled account' error message
        else:
            print('baz')
            # Return an 'invalid login' error message.

