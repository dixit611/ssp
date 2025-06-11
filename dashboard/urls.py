from django.urls import path
from . import views
from dashboard.views import register
from dashboard.views import login_page
from dashboard.views import logout_view




urlpatterns = [
    path('', views.home,name='home'),
    path('notes', views.notes,name='notes'),
    path('delete_note/<int:pk>', views.delete_note,name='delete_note'),
    path('notes_detail/<int:pk>/', views.NotesDetailView.as_view(), name='notes_detail'),



    path('homework', views.homework,name='homework'),
    path('update_homework/<int:pk>', views.update_homework,name='update_homework'),
    path('delete_homework/<int:pk>', views.delete_homework,name='delete_homework'),


    path('youtube', views.youtube,name='youtube'),


    path('todo', views.todo,name='todo'),
    path('update_todo/<int:pk>', views.update_todo,name='update_todo'),
    path('delete_todo/<int:pk>', views.delete_todo,name='delete_todo'),


    path('books', views.books,name='books'),


    path('dictionary', views.dictionary,name='dictionary'),

    path('wiki', views.wiki,name='wiki'),

    path('editor', views.editor,name='editor'),
    path('save', views.save_code,name='save'),
    path('fetch', views.fetch_code, name='fetch'),
    path('update_code/', views.update_code, name='update_code'),
    path('delete_code/', views.delete_code, name='delete_code'),
    path('run', views.run_code_view, name='run'),

    path('duckduckgo_search/', views.duckduckgo_search, name='duckduckgo_search'),
    path('w3schools_search/', views.w3schools_search, name='w3schools_search'),

    path('calculator/', views.calculator, name='calculator'),
    path('timer/', views.timer, name='timer'),


    path('general/', views.general, name='general'),
    



    path('conversion', views.conversion,name='conversion'),



    path('login_page/', login_page, name='login_page'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    
    



    path('videocall', views.videocall,name='videocall'),

    
    path('typing/', views.typing, name='typing'),
    path('time_table/', views.time_table, name='time_table'),
    path('add/', views.add_event, name='add_event'),


    
    # path('add/', views.add_event, name='add_event'),
    # path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    # path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    
   
    
]
