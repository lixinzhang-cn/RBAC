# coding: utf-8
#!/usr/bin/env python
"""
    created by: Gao YaXing
    created on: 17/4/4
"""

from __future__ import unicode_literals

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from staff.models import User, UserRole, Access, RoleAccess


def login(request):
    """登录"""
    uid = request.GET.get('uid')
    if not uid:
        return HttpResponseRedirect(u'/', {"index_info", '登录必须有UID'})

    try:
        user = User.objects.get(id=uid)
    except Exception as e:
        user = None

    if user:
        res = HttpResponse
        res.set_cookie('uid', uid)
        if user.is_admin:
            res.set_cookie('iss', 1)
        return res
    return HttpResponseRedirect('/')


def logout(request):
    """登出"""
    response = HttpResponseRedirect("/login")
    if 'uid' in request.COOKIES:
        response.delete_cookie('uid')
    if 'iss' in request.COOKIES:
        response.delete_cookie('iss')
    return response


def user_add(request):
    """用户添加 操作"""
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()

    user = User.objects.create(name=name, email=email)

    try:
        user.save()
    except Exception as e:
        print('保存出错了, %s', e)
    return HttpResponseRedirect(reverse('staff_list'))


def user_edit(request):
    """用户编辑 操作"""
    uid = request.POST.get('uid', '').strip()
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()

    try:
        user = User.objects.get(id=uid)
    except Exception as e:
        user = None

    if user:
        user.name = name
        user.email = email
        user.save()

    return HttpResponseRedirect(reverse('staff_list'))

