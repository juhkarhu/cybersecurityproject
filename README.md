# Cyber Security Base 2022 - Course Project I

My project for [Cyber Security Base 2022](https://cybersecuritybase.mooc.fi/) courses Course Project I assignment. The goal for the project is to construct software with at least five security flaws from the [OWASP Top 10 Web Application Security Risks](https://owasp.org/www-project-top-ten/) list. In the list below, I have pointed out each flaw, how to use it, and how to fix it in code. 

The repository can be found here: LINK HERE

To use the project on your own machine, download and extract the files, open terminal in the project directory and type: 

```
python manage.py runserver
```

If for some reason there are problems with the database (sqlite3), run the following commands before trying to run the application.

```
python manage.py makemigrations
python manage.py migrate
```

Once the application is running, it's address should be displayed on the terminal (probably something along the lines of http://127.0.0.1:8000/). 

You can easily remove users, posts and other information from the database by going to the Django's admin interface in the following address: http://127.0.0.1:8000/admin/

There should be premade admin credentials for you to use with the following username and password.
**Username**: admin
**Password**: password


---


## Flaw 1: [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

One of the most, if not the, prevelant vulnerability in software is broken access control, which only seems to rise in popularity each year. Access control enforces such policiess that users cannot act outside their intented permissions. In the context of web applications, such as this, access control is dependent on authentication and session management. 

In the contect of this application, the vulnerability caused by broken access control is known as *key identifier change*, which allows unwanted access to users to perform actions that would be otherwise unauthorized. In this application, users have profile with some personal information fields. Everyone's profile should currently be visible only to the user in question, but sadly developers forgot to implement this. This exploit can be used in this application by simply going 'http://localhost:8000/profile/' and adding the user's username to the end of the address. Even users that aren't logged in can go and view the information (even the occasional bypasser can enter that page and alter the info even though it reports error when updating information - so the vulnerability does not even need users to be logged in). 

### **How to fix**

To fix this, you will need two things. Firstly there should be the following decorator above the profile_view function requiring the user entering that view to be logged in. This can be achieved like this:

```python
@login_required(login_url='/login') # <-- This is the decorator in question
def profile_view(request, username):
```

Then secondly, there should be a check that checks if the user that is trying to enter his/her own profile, and if not redirect said user elsewhere. This is fixed be adding the following two lines of code just at the start of the function. 

```python
def profile_view(request, username):
    if request.user.username != username:   # <-- This 
        return redirect('project:index')    # <-- And this line 
```


## Flaw 2: [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)  

Previously found on OWASP's Top 10 list as *Broken Authentication*, Identification and Authentication failures can occur when the function's that are related to the user's identity and authentication are overlooked in design/development phase or not being protected by the application adequately enough. According to OWASP there may be authentication weakness if the application:
> Permits default, weak, or well-known passwords, such as "Password1" or "admin/admin"

Currently the application does not require anything from the passwords and they can be pretty much anything ('123', 'abc', etc.). This obviously isn't good so let's change that. 

Since the application uses [Django's authentication system](https://docs.djangoproject.com/en/4.0/topics/auth/default/), we can quire easily add some [password validators](https://docs.djangoproject.com/en/4.0/topics/auth/passwords/#module-django.contrib.auth.password_validation) for Django to use in the registration form. There actually are some prefedined validators ready in settings.py although they are currently commented. Validators can be found under the 'AUTH_PASSWORD_VALIDATORS' variable (to be precise, the validators are on lines 123-134). 


## Flaw 3: [Insecure Design](https://owasp.org/Top10/A04_2021-Insecure_Design/) 

New category in OWASP's Top 10 list, Insecure Design focuses on risks related to design and architectural flaws, with a emphasis among other things in secure design patterns. Although a broad category, it is distinct between insecure design and implementation (e.g., insecure implementation of password validators). 

One of the ways of improving the design if writing [tests](https://docs.djangoproject.com/en/4.0/topics/testing/overview/). Secure design ensures that code is robustly designed and tested to prevent known attack methods. In our case, we could write tests that test that ensures that password validators work as intented with different combinations. 

```python
class BaseTest(TestCase):
    def setUp(self):
      self.registration_url = reverse('project:register')
      self.user = {
        'username': 'testuser',
        'password1': 'abc',
        'password2': 'abc'
      }
      return super().setUp()

class RegisterTest(BaseTest):
    def test_can_not_use_abc_as_password(self):
        response = self.client.post(self.registration_url, self.user)
        self.assertEqual(response.status_code, 302)
```

It is noteworthy that, since I'm redirecting user after succesfull registration, the expected status code is 302. A status code 200 is expected if the registration is unsuccesfull and it just loads the same registration page. 


## Flaw 4: [Security Logging and Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)  

Wouldn't it be nice to have a log of everything that has happened in your application. Having logs is nice, reading them can be boring but the thought of making them seems to be the most boring since it has it's own place on OWASP Top 10 list. Logging is quite often an afterthought, if not complemetely overlooked, even if most would agree it helps the both the development and maintaining the app. 

Fortunately adding logging in Django is quite easy using [Django's logging system](https://docs.djangoproject.com/en/4.0/topics/logging/). By adding this bit of code to the settings.py

Lack of proper security logging and monitoring is often overlooked, as many developers feel like it is only necessary for development purposes. Currently the website has no logging whatsoever and we need to add records to some auditable events, such as logins and form submits to monitor any suspicious activity.

In order to add logging functionality to the application, we can use Django's built-in logging system. First we must set-up the logging in the settings.py file by adding the following to the bottom of the file. 

```python
LOGGING = {
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO', # This can also be DEBUG, which gives you a lot more information. For explaining this, INFO works just fine
            'class': 'logging.FileHandler',
            'filename': './admin.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

After the above to settings.py, we can use the logger ourselves. Let's add this line to the top of views.py to import out logger.

```python
import logging
logger = logging.getLogger(__name__)
```

Then we can log events as we please like so for example when registration is succesfull:

```python
logger.info('User registration succesfull with the following username: {}'.format(user.username))

```


## Flaw 5: [Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)  

Last but not least on my list of vulnerabilities on my application is outdated components. Even small projects (especially on some languages/frameworks) can require quite a bit of outside libraries to import functionality and services. OWASP makes it quite clear when you are vulnerable regarding this:
> If you do not know the versions of all components you use (both client-side and server-side).

To prevent this, all components, documentation, files, dependencies and features that aren't used should be removed. One should always aim to keep all the components and apps updated. This can be easily done with package manager such as [pip](https://pypi.org/project/pip/). In this project there is [django-staticfiles](https://github.com/jezdez/django-staticfiles) named app on the INSTALLED_APPS list in settings.py (note that it is commented out for safety and should not be installed). 


## Flaw 6: [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

Same category as in Flaw 1, but slightly different mechanism in play. The weakness in question is [Cross-Site Request Forgery](https://cwe.mitre.org/data/definitions/352.html). Due to a overlook by the developers, they left a '@csrf_exempt' decorator in the views.py above the 'register_view' method. To add insult to injury, they also forgot to add {% csrf_token %} in the 'register.html' form. 

Luckily these are easy enough fixes. 
Step 1: Remove the @csrf_exempt decorator in views.py.
Step 2: Add {% csrf_token %} above the '{{form.as_p}}' line in register.html.