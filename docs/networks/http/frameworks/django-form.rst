=============
Django Form
=============

:Author: 王蒙
:Tags: Django, Web Frameworks, Python

:abstract:

    本节介绍 Django 如何处理 form（表单）。

.. contents::

Audience
========

Python 开发，网站开发

Prerequisites
=============

Django Model, Python

Problem
=======

- 什么是表单
- Django 如何处理表单


Solution
========

- 什么是表单

    表单就是 html5 中的 form 元素。比如：

    .. code-block::

        <form action="demo_form.asp" method="get" id="user_form">
        First name:<input type="text" name="fname" />
        <input type="submit" />
        </form>

    表单中 method 属性表示向服务器发送的 HTTP 方法，一般都是 POST ，也可能是 GET。

    通常表单就是向服务器发送了个 dict。

- Django 如何处理表单

    - Form

        .. code-block::

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

    - ModelForm

        ModelFrom 直接使用关联的 model 中定义的字段作为 form 的输入字段。

        .. code-block::

            from .models import Comment
            # define modelform.
            class CommentForm(forms.ModelForm):
                class Meta:
                model = Comment
                fields = ('name', 'email', 'body')


            # 使用 ModelForms 与普通的 form 最重要的一点区别是： ModelForms 可以直接调用 save 方法，保存数据到数据库中。
            def post_detail(request, year, month, day, post):
                post = get_object_or_404(Post, slug=post,
                                               status='published',
                                               publish__year=year,
                                               publish__month=month,
                                               publish__day=day)

                # List of active comments for this post
                comments = post.comments.filter(active=True)
                if request.method == 'POST':
                    # A comment was posted
                    comment_form = CommentForm(data=request.POST)

                    if comment_form.is_valid():
                        # Create Comment object but don't save to database yet
                        new_comment = comment_form.save(commit=False)
                        # Assign the current post to the comment
                        new_comment.post = post
                        # Save the comment to the database
                        new_comment.save()
                else:
                    comment_form = CommentForm()
                    new_comment = False

                # List of similar posts
                post_tags_ids = post.tags.values_list('id', flat=True)
                similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
                similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags',
                                                                                         '-publish')[:4]
                return render(request, 'blog/post/detail.html', {'post': post,
                                                                 'comments': comments,
                                                                 'comment_form': comment_form,
                                                                 'similar_posts': similar_posts,
                                                                 'new_comment': new_comment})







Reference
=========

- Django by Example（本节的代码摘自 Django By Example）
