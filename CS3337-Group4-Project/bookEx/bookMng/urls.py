from django.urls import path
from . import views
from .views import feedback, thank_you

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('searchbook', views.searchbook, name='searchbook'),
    path('favorite_book/<int:book_id>/', views.favorite_book, name='favorite_book'),
    path('feedback/', feedback, name='feedback'),
    path('thank_you/', thank_you, name='thank_you'),
    path('shoppingcart', views.viewcart, name='viewcart'),
    path('addtocart/<int:book_id>', views.addtocart, name='addtocart'),
    path('deletefromcart/<int:book_id>', views.deletefromcart, name='deletefromcart'),
    path('book_detail/<int:book_id>/add_comment/', views.add_comment, name='add_comment'),
    path('purchasecart/', views.purchase_cart, name='purchasecart'),
    path('purchase_success/', views.purchase_success, name='purchase_success'),
    path('favorites', views.favorites, name='favorites'),
]
