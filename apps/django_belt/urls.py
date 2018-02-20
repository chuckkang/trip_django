from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
# url(r'^$', views.index), # This line has changed!
url(r'^$', views.index),
url(r'^main$', views.main), #main page after login
url(r'^addtrip$', views.addtrip),
url(r'^tripdetails/(?P<trip_id>\d+)$', views.tripdetails),
url(r'^join/(?P<trip_id>\d+)$', views.join),
url(r'^submittrip$', views.submittrip),
url(r'^register$', views.register),
url(r'^login$', views.login),
url(r'^logout$', views.logout),
url(r'^$', views.index)
]