# coding=utf8

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from timepaw.profiles.models import Profile
from timepaw.activekeys.views import use as use_key
import hashlib

def index(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        is_logged_in = True
    else:
        is_logged_in = False
    return render_to_response('profiles/index.html', {'is_logged_in' : is_logged_in }, context_instance=RequestContext(request))

def signup(request):
    error = {}
    if request.method == 'POST':
        if len(request.POST['nickname']) < 2:
            error['nickname'] = u"昵称由2-20个字符组成."
        if len(request.POST['nickname']) > 20:
            error['nickname'] = u"昵称由2-20个字符组成."
        if (Profile.objects.filter(email=request.POST['email']).count() != 0):
            error['email'] = u"该email地址已经被注册！"
        if len(request.POST['password']) < 6:
            error['password'] = u"密码由6-20个字符组成."
        if len(request.POST['password']) > 20:
            error['password'] = u"密码由6-20个字符组成."
        if request.POST['passwordagain'] != request.POST['password']:
            error['passwordagain'] = u"您输入的两次密码不匹配."
        if not use_key(request.POST['invitecode']):
            error['invitecode'] = u"无效的邀请码."
        
        if error == {}:
            m = hashlib.md5()
            m.update(request.POST['password'])
            p = Profile.objects.create(nickname=request.POST['nickname'], email=request.POST['email'], password=m.hexdigest())
            request.session['uid'] = p.id
            return redirect('/datasources')
        else:
            return render_to_response('profiles/signup.html', {'error' : error}, context_instance=RequestContext(request))
    else:
        return render_to_response('profiles/signup.html', context_instance=RequestContext(request))

def login(request):
    uid = request.session.get('uid', default = None)
    if uid is not None:
        return redirect('/home#latest')
    if request.method == 'POST':
        error = {}
        if (Profile.objects.filter(email = request.POST['email']).count() != 0):
            p = Profile.objects.get(email = request.POST['email'])
            m = hashlib.md5()
            m.update(request.POST['password'])
            if m.hexdigest() == p.password:
                request.session['uid'] = p.id
                return redirect('/home#latest')
            else:
                error['password'] = u"请输入正确的密码"
        else:
            error['email'] = u"请输入有效的email地址"
        return render_to_response('profiles/login.html',  {'error' : error}, context_instance=RequestContext(request))
    else:
        return render_to_response('profiles/login.html', context_instance=RequestContext(request))

def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return redirect('/')