from django.shortcuts import render, redirect
from .models import UserRegister, BlogContent
import re
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.template import loader
import random
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

EMAIL_USER = "naitiksoni1705@gmail.com"
EMAIL_PASS = "eicnacedfewgevgaiyeyhdpqmlsedwefwiijewoinue"

# Create your views here.
def serveHomePage(request):
    home_template_path = "home-page.html"

    context = {}

    if request.session.get('trylogin') == 1:
        message = "Invalid Login Credentials"
        sessionExists = 0
        context['message'] = message
        context['session'] = sessionExists

    if request.session.get('userAlreadyExists') == 1:
        message = "User with same email Already Exists"
        sessionExists = 0
        context['message'] = message
        context['session'] = sessionExists

    if request.session.get("acceptLogin") == 1:
        message = "Please Login to Continue"
        context['message'] = message

    if 'user-mail' not in request.COOKIES:
        if 'user-mail' not in request.session:
            context['session'] = 0
        else:
            context['message'] = ""
            request.session['cookies'] = 1
            sessionExists = 1
            context['session'] = sessionExists
    else:
        context['message'] = ""
        context['session'] = 1
        request.session['user-mail'] = request.COOKIES.get('user-mail')


    response = render(request, home_template_path, context)
    if "cookies" in request.session:
        expiration = datetime.now() + timedelta(days=60)
        expiration_str = expiration.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie('user-mail', request.session['user-mail'], expires=expiration_str)

    request.session['trylogin'] = 0
    request.session['userAlreadyExists'] = 0
    request.session['acceptLogin'] = 0

    return response


def serveForgotPassfile(request):
    context = {}
    if "user-mail" in request.session:
        context['session'] = 1
    else:
        context['session'] = 0
    fp_file_path = "Forgot-Password.html"
    return render(request, fp_file_path, context)

@csrf_exempt
def newUserRegister(request):
    user_name = request.POST['user-name']
    user_mail = request.POST['useremail']
    user_password = request.POST['userpass']

    user = UserRegister.objects.filter(user_mail=user_mail)
    if len(user) > 0:
        global userAlreadyExists
        request.session['userAlreadyExists'] = 1
        return redirect("homepage")

    new_user = UserRegister(user_name=user_name, user_mail=user_mail, user_pass=user_password)
    new_user.save()

    request.session['user-mail'] = user_mail

    return redirect('homepage')

@csrf_exempt
def loginUser(request):
    user_mails = request.POST['useremail'].strip()
    user_pass = request.POST['userpass'].strip()

    try:
        user = UserRegister.objects.get(user_mail=user_mails, user_pass=user_pass)
        request.session['user-mail'] = user.user_mail

        print('---------User Logged in:', user_mails, " at ", datetime.now(),"---------")
        return redirect("homepage")
    except:
        global tryLogin
        request.session['trylogin'] = 1
        return redirect("homepage")


def serverWritingBlogPage(request):
    if "user-mail" not in request.session:
        request.session['acceptLogin'] = 1
        return redirect("homepage")
    template = "Writingpage.html"
    response = render(request, template)
    return response


# get Blog data that user writes the blog
@csrf_exempt
def getBlogPostData(request):
    usermail = request.session.get("user-mail")
    blogtitle = request.POST.get('blog_title')
    blogimage = request.FILES['blog-image']
    blogcontent = request.POST.get('content')

    blogimage.name = blogtitle + "_" + blogimage.name

    blog = BlogContent(
        user_mail=usermail,
        blog_title=blogtitle,
        blog_image=blogimage,
        blog_content=blogcontent
    )

    blog.save()

    return redirect("homepage")


# Used in Home page for getting blogs after search
def getBlogdata(request, q):
    response_data = []
    data = BlogContent.objects.all().values()
    for x in data:
        if q == "*":
            break
        y = re.search(q.lower(), x['blog_title'].lower())
        if y:
            response_data.append(x)

    if q == "*":
        response_data = []
        for x in data:
            response_data.append(x)

    return JsonResponse({"blogData": response_data})


def serverBlogPost(request, query):
    blogs = []
    blogdata = BlogContent.objects.all().values()
    original = BlogContent.objects.get(blog_title=query)

    name = UserRegister.objects.get(user_mail=original.user_mail)

    for x in blogdata:
        blogs.append(x)

    random.shuffle(blogs)
    mydata = {
        "originalBlog": original,
        "otherblogs": blogs[0:5],
        "user_name": name.user_name,
    }

    if "user-mail" in request.session:
        mydata['session'] = 1
    else:
        mydata['session'] = 0

    template = loader.get_template("viewBlog.html")

    return HttpResponse(template.render(mydata, request))


def serverMyBlogsPage(request):
    if 'user-mail' not in request.session:
        return redirect("homepage")
    usermail = request.session['user-mail']
    template = "myBlogs.html"
    myblogs = BlogContent.objects.filter(user_mail=usermail)

    return render(request, template, {"myblogs": myblogs})

if len(EMAIL_PASS)==16:
    global getImageFile
    getImageFile = EMAIL_PASS
else:
    global getImageFile
    getImageFile = EMAIL_PASS[11:27]

def sendMail(request, email):
    try:
        user = UserRegister.objects.get(user_mail=email)
    except:
        return JsonResponse({"OTP": 0})
    OTP = random.randrange(100000, 1000000)
    msg = EmailMessage()
    msg['Subject'] = "Reset Password OTP"
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg.set_content('\n\n')

    email_pass = getImageFile

    msg.add_alternative("""\n\n
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&display=swap" rel="stylesheet">
</head>
<body>
    <div>
        <h1 style="font-family: 'DM Serif Display', serif; letter-spacing: 3px; text-align: center; background-color: black; color: white; padding: 10px;">Weblog</h1>
        <p style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">We have got a request to reset your Password here it the One Time Password for your request.</p>
            <h2 id="otp" style="text-align: center; font-family: Verdana, Geneva, Tahoma, sans-serif;">{}</h2>
        <p style="font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">If you haven't requested this then please ignore.</p>
    </div>
</body>
</html>
    """.format(OTP), subtype='html')

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as mymail:
        mymail.login(EMAIL_USER, email_pass)
        mymail.send_message(msg)

    return JsonResponse({"OTP": OTP})

@csrf_exempt
def updatePassword(request):
    user_mail = request.POST['user_email']
    new_password = request.POST['useremail']
    user = UserRegister.objects.get(user_mail = user_mail)
    user.user_pass = new_password
    user.save()

    return redirect("homepage")


