Features of this microblog:<pre>
Administration
  <br>a. The application has three tiers of users, Administrators, Users and Visitors (unauthenticated visitors
  to the site).
  b. All user tiers can list, search and view public Posts.
  c. Administrators can list, search, create, edit, update, delete Users.
  d. The administrator interface and functions should not be visible by Users or Visitors
  e. Administrators can list, search, enable and disable Posts but cannot create, edit or otherwise modify a
  Post.
  f. Can login from a special administrator portal (not the default login portal that Users use).
  g. Can logout
  
</pre>


Layout for the Fluffy Container Ship:
<pre><code>
app/
  api/
    __init__.py
    auth.py
    errors.py
    tokens.py
    users.py
  auth/
    __init__.py
    email.py
    forms.py
    routes.py
  errors/
    __init__.py
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
  translate.py
  </code></pre>
  
