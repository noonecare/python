===========
追踪用户
===========

:Author: 王蒙
:Tags: Django, Web Frameworks, Python, session, cookies

:abstract:

    用户在一个网站连续执行的操作称为是一个 session。在一个 session 中，我们希望服务器记录我们在该 session 的行为。比如我们登录了网站之后，去浏览网站时，我们希望网站知道我们已经登录，不希望网站不断重复地要求我们输入账号密码。

    http 协议中，session/cookies 保存用户一次会话的历史。本节总结 Django 是如何处理 session/cookies 的。

.. contents::

Audience
========

Python 开发，网站开发

Prerequisites
=============

Python, cookies, session


Problem
=======


Django 如何处理 session/cookies ？


Solution
========

客户端会把用户本次会话的信息保存到 http request 的 cookies 中发送给服务器处理。服务器端缓存接收到用户本次会话信息（在 http request 的 cookies 中）到 session 中，然后把服务器端的 session 保存到 http response 的 set-cookies 中发送回客户端。每次客户端接到服务器端的 http response，也会根据 http response 中的 cookies 更新客户端的 cookies。这样不管是客户端和服务器端都缓存了用户本次会话的信息。

django 提供了 `django.contrib.sessions.middleware.SessionMiddleware` 来处理上面这套逻辑。该中间件，使得开发人员在写 view 的时候可以通过 request.session（是个字典） 访问 http request 请求的 cookies。


可以使用不同的引擎来保存session, 为此使用 session 时，需要在 settings.py 配置


    - SESSION_ENGINE: 使用数据库，缓存(Memcached)，文件还是什么来保存session。Django 默认使用数据库保存 session，推荐使用缓存保存 session ，因为使用缓存效率更高。
    - SESSION_COOKIES_AGE: 过期时间。在写 views.py 时，可以通过调用 `set_expiry()` 方法操作过期行为。
    - SESSION_COOKIES_DOMAIN
    - SESSION_COOKIES_SECURE: 不接受 http 的cookies，只有 https 的 cookies 是有效的。
    - SESSION_EXPIRE_AT_BROWSER_CLOSE: 客户端关闭浏览器会使 cookies 过期。
    - SESSION_SAVE_EVERY_REQUEST: 每次请求都会更新服务器端的 session。



.. code-block::

    class Cart(object):

        def __init__(self, request):
            """
            Initialize the cart.
            """
            self.session = request.session
            cart = self.session.get(settings.CART_SESSION_ID)
            if not cart:
                # save an empty cart in the session
                cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

        def __len__(self):
            """
            Count all items in the cart.
            """
            return sum(item['quantity'] for item in self.cart.values())

        def __iter__(self):
            """
            Iterate over the items in the cart and get the products from the database.
            """
            product_ids = self.cart.keys()
            # get the product objects and add them to the cart
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                self.cart[str(product.id)]['product'] = product

            for item in self.cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

        def add(self, product, quantity=1, update_quantity=False):
            """
            Add a product to the cart or update its quantity.
            """
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0,
                                          'price': str(product.price)}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save()

        def save(self):
            # update the session cart
            self.session[settings.CART_SESSION_ID] = self.cart
            # mark the session as "modified" to make sure it is saved
            self.session.modified = True



Reference
=========

- Django Cookies Session Settings: https://docs.djangoproject.com/en/1.8/ref/settings/#sessions
- Django By Example

