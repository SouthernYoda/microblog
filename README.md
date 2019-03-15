Features of this microblog based on assignment:<pre>

  1.    Administration
    a.    The application has three tiers of users, Administrators, Users and Visitors (unauthenticated 
    visitors to the site).
    b.    All user tiers can list, search and view public Posts.
    c.    Administrators can list, search, create, edit, update, delete Users.
    d.    The administrator interface and functions should not be visible by Users or Visitors
    e.    Administrators can list, search, enable and disable Posts but cannot create, edit or 
    otherwise modify a Post.
    f.     Can login from a special administrator portal (not the default login portal that Users use).
    g.    Can logout
  2.    Users
    a.    Users can list, search, create, edit, update and delete their own Posts.
    b.    Users can also list, search and view private Posts which they have been invited to.
    c.    Can logout
    d.    Can edit, update and delete their account and profile
    <strike>e.    Users can configure “watch” words and receive notifications in their account when a post is 
    made by any user that matches their “watch” words.</strike>
  3.    Visitors
    a.    Can create a new User account
    b.    Can login
    c.    Can perform a password reset
  4.    Posts
    a.    Can be marked as Public or Private
    b.    Private Posts can have a list of “invited” users who are allowed to see the posts. Invites 
    can be sent to other Users by providing a list of usernames.
    c.    Posts work similarly to pastebin (a raw and rendered window) with the option to download the 
    raw post as a text file.
    d.    Posts have “short” URLs similar to the ones on the real Pastebin site. (Ex. 
    yourassignment.com/a8BjLp)
    <strike>e.    User should be able to configure a post expiration date.</strike>
    f.     Posts can have titles.
    g.    The main/home page should display the 10 most recent posts.
    h.    Users should be able to upload text files as posts.
    i.     Users should be able to type posts into a text field on the post creation page.
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
  
