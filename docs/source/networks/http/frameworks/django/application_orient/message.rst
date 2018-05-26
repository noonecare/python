===========
message
===========

:Author: 王蒙
:Tags: Django, Web Frameworks, Python, message, notification

:abstract:

    Django 中 `django.contrib.messages` 提供了消息通知机制。

.. contents::

Audience
========

Python 开发，网络开发

Prerequisites
=============

Python， Django View


Problem
=======

使用消息通知用户操作成功了，操作失败了等等。


Solution
========

`django.contrib.messages` 提供了

    - success(): 表示操作成功了
    - info(): 普通消息
    - warning(): 报警
    - error(): 表示操作失败了
    - debug(): 调试信息


.. code-block::

    from django.contrib import messages
    @login_required
    def edit(request):
        if request.method == 'POST':
            # ...
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile updated '\
                'successfully')
            else:
                messages.error(request, 'Error updating your profile')
        else:
            user_form = UserEditForm(instance=request.user)


Reference
=========

- Django By Example
