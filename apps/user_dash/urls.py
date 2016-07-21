from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	# url(r'^register$', views.registerPage, name = 'registerPage'),
	url(r'^registering$', views.register, name = 'register'),
	url(r'^login$', views.loginPage, name = 'loginPage'),
	url(r'^loggingin$', views.login, name = 'login'),
	url(r'^logout$', views.logout, name = 'logOut'),
	url(r'^dashboard$', views.dashboard, name = 'dashboard'),
	url(r'^addUser$', views.addUser, name = 'addUser'),
	url(r'^addUserPage$', views.addUserPage, name = 'addUserPage'),
	url(r'^remove/(?P<id>[0-9]+)$', views.remove, name = 'remove'),
	url(r'^edit/(?P<id>[0-9]+)$', views.edit, name = 'edit'),
	url(r'^update/(?P<id>[0-9]+)$', views.update, name = 'update'),
	url(r'^profile/(?P<id>[0-9]+)$', views.profile, name = 'profile'),
	url(r'^editProfile/(?P<id>[0-9]+)$', views.editProfile, name = 'editProfile'),
	url(r'^editProfileProcess/(?P<id>[0-9]+)$', views.editProfileProcess, name = 'editProfileProcess'),
	url(r'^writeMessage/(?P<id>[0-9]+)/(?P<page_id>[0-9]+)$', views.writeMessage, name = 'write_message'),
	url(r'^writeComment/(?P<id>[0-9]+)/(?P<message_id>[0-9]+)/(?P<page_id>[0-9]+)$', views.writeComment, name = 'write_comment'),

]