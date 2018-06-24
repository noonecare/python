=============
Django Form
=============

:作者: 王蒙
:标签: Django, Web Frameworks, Python

:简介:

    本节介绍 Django 如何处理 form（表单）。

.. contents::

目标读者
========

Python 开发，网站开发

预备知识
=============

Django Model, Python

问题
=======

- 什么是表单
- Django 如何处理表单


解决办法
========

什么是表单
~~~~~~~~~~~~~~~~


    表单用于接收用户输入参数。

    表单是 html5 中的 form 元素。

    html5 form 元素中 method 属性表示向服务器发送的 HTTP 方法，一般都是 POST ，也可能是 GET。

    表单会向服务器传送用字典表示的数据，Django 可以方便得解析 form 获得用户输入。

Django 如何处理表单
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

定义 form， 和定义 Model 类似，给出表单的字段，就定义了表单。与 Model 中的字段不同， form 字段的 widget 会设置该字段在前端的展现形式。

在模板中 render form。 form.as_p, form.as_table 等等方法可以把 form 转成 html 语句（进而显示在前端），一般会把 form.as_p, form.as_table 等等语句直接写到模板中。


Form 解析用户输入数据：

    #. 首先调用构造器，生成 form， 比如 EmailForm(request.POST)
    #. 然后调用 is_valid 验证输入是否合法，调用 .clean_data（dict 类型数据） 得到用户输入。
    #. 如果是 ModelForm，可能会调用 save 保存结果。



.. code-block:: python

    from django import forms
    # define a form is forms.py.
    class EmailPostForm(forms.Form):
        name = forms.CharField(max_length=25)
        email = forms.EmailField()
        to = forms.EmailField()
        comments = forms.CharField(required=False,
                                    widget=forms.Textarea)

    # handle form in views.

    def post_share(request, post_id):
        # Retrieve post by id
        post = get_object_or_404(Post, id=post_id, status='published')
        sent = False

        if request.method == 'POST':
            # Form was submitted
            form = EmailPostForm(request.POST)
            if form.is_valid():
                # Form fields passed validation
                cd = form.cleaned_data
                post_url = request.build_absolute_uri(post.get_absolute_url())
                subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
                message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
                send_mail(subject, message, 'admin@myblog.com', [cd['to']])
                sent = True
        else:
            form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post': post,
                                                        'form': form,
                                                        'sent': sent})


ModelForm
~~~~~~~~~~~~~~~~~

ModelFrom 直接使用关联的 model 中定义的字段作为 form 的输入字段。

.. code-block:: python

    from .models import Comment
    # define modelform.
    class CommentForm(forms.ModelForm):
        class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


 Formset
~~~~~~~~~~~~~~~

多个 form 组成 formset。详细参见 `Formsets`_ 。





参考文献
=========

- Django by Example（本节的代码摘自 Django By Example）
- working with form: https://docs.djangoproject.com/en/dev/topics/forms/
- Form and field validation: https://docs.djangoproject.com/en/dev/ref/forms/validation/
- Creating forms from models: https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/
- Formset: https://docs.djangoproject.com/en/1.11/topics/forms/formsets/

.. _Formsets: https://docs.djangoproject.com/en/1.11/topics/forms/formsets/