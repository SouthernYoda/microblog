<pre><code>app/
    auth/                               &lt;-- blueprint package
        __init__.py                     &lt;-- blueprint creation
        email.py                        &lt;-- authentication emails
        forms.py                        &lt;-- authentication forms
        routes.py                       &lt;-- authentication routes
    templates/
        auth/                           &lt;-- blueprint templates
            login.html
            register.html
            reset_password_request.html
            reset_password.html
    __init__.py                         &lt;-- blueprint registration
</code></pre>





Layout for the Fluffy Container Ship:
<p>app/
<p>  api/</p>
<p>    __init__.py</p>
<p>    auth.py</p>
<p>    errors.py</p>
<p>    tokens.py</p>
<p>    users.py</p>
<p>  auth/</p>
<p>    __init__.py</p>
<p>    email.py</p>
<p>    forms.py</p>
<p>    routes.py</p>
<p>  errors/</p>
<p>    __init__.py</p>
    handlers.py
  main/
    __init__.py
    form.py
    routes.py
  static/
    loading.gif
  templates/
    auth/
      login.html
      register.html
      reset_password.html
      reset_password_request.html
    email/
      export_posts.html
      export_posts.txt
      reset_password.html
      reset_password.txt
    errors/
      404.html
      500.html
    _post.html
    base.html
    edit_profile.html
    index.html
    messages.html
    search.html
    send_message.html
    users.html
    user_popup.html
  translations/
  __init__.py
  cli.py
  email.py
  models.py
  search.py
  tasks.py
  translate.py</p>
  
