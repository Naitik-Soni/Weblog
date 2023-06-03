from django.urls import path
from .views import *

urlpatterns = [
    path('', serveHomePage, name="homepage"),
    path('registeruser/', newUserRegister, name="userregistration"),
    path('loginuser/', loginUser, name="userlogin"),
    path('forgot-password/', serveForgotPassfile, name="forgotpassword"),
    path('forgot-password/update-password/', updatePassword, name="updatepassword"),
    path('WriteBlog/', serverWritingBlogPage, name="writeblog"),
    path("WriteBlog/postblog/", getBlogPostData, name="postblog"),
    path("getblog/<str:q>", getBlogdata, name="getstories"),
    path("Blog/<str:query>", serverBlogPost, name="blogpost"),
    path("myblogs/", serverMyBlogsPage, name="myblogs"),
    path('sendmail/<str:email>', sendMail, name="sendmail")
]