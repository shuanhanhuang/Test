"""
URL configuration for Test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from testapp.views import HomePage,login,logout,homeDelete,homeEdit,homeIndex,HomePost,\
    signIndex,signPost,signEdit,signallIndex,Detail,\
    meetingallIndex,meetingIndex,meetingPost,meetingEdit,\
    meetinginnerEdit,meetinginnerPost,meetinginnerIndex,meetinginnerDelete,\
    contactallIndex,contactIndex,contactPost,contactEdit,\
    contractallIndex,contractIndex,contractPost,contractEdit,\
    contractinnerDelete,contractinnerIndex,contractinnerEdit,contractinnerPost,\
    changeallIndex,changeIndex,changeEdit,changePost
urlpatterns = [
    path('',HomePage),
    path('HomePage/',HomePage),
    path('login/', login),
    path('logout/', logout),

    path('homeIndex/',homeIndex),
    path('homePost/',HomePost),
    path('homeEdit/<int:id>/<str:mode>',homeEdit),
    path('homeDelete/<int:id>/',homeDelete),

    path('signallIndex/',signallIndex),
    path('signIndex/<str:cNumber>/',signIndex),
    path('signPost/<str:cNumber>/',signPost),
    path('signEdit/<str:cNumber>/<int:id>/<str:mode>',signEdit),
    path('Detail/<str:cNumber>/',Detail),

    path('meetingallIndex/',meetingallIndex),
    path('meetingIndex/<str:cNumber>/',meetingIndex),
    path('meetingPost/<str:cNumber>/',meetingPost),
    path('meetingEdit/<str:cNumber>/<int:id>/<str:mode>',meetingEdit),

    path('meetinginnerDelete/<str:cNumber>/<int:id>/',meetinginnerDelete),
    path('meetinginnerIndex/<str:cNumber>/',meetinginnerIndex),
    path('meetinginnerEdit/<str:cNumber>/<int:id>/<str:mode>',meetinginnerEdit),
    path('meetinginnerPost/<str:cNumber>/',meetinginnerPost),

    path('contactallIndex/',contactallIndex),
    path('contactIndex/<str:cNumber>/',contactIndex),
    path('contactPost/<str:cNumber>/',contactPost),
    path('contactEdit/<str:cNumber>/<int:id>/<str:mode>',contactEdit),

    path('contractallIndex/',contractallIndex),
    path('contractIndex/<str:cNumber>/',contractIndex),
    path('contractPost/<str:cNumber>/',contractPost),
    path('contractEdit/<str:cNumber>/<int:id>/<str:mode>',contractEdit),

    path('contractinnerDelete/<str:cNumber>/<int:id>/',contractinnerDelete),
    path('contractinnerIndex/<str:cNumber>/',contractinnerIndex),
    path('contractinnerEdit/<str:cNumber>/<int:id>/<str:mode>',contractinnerEdit),
    path('contractinnerPost/<str:cNumber>/',contractinnerPost),

    path('changeallIndex/',changeallIndex),
    path('changeIndex/<str:cNumber>/',changeIndex),
    path('changeEdit/<str:cNumber>/<int:id>/<str:mode>',changeEdit),
    path('changePost/<str:cNumber>/',changePost),


    path('admin/', admin.site.urls),
]
