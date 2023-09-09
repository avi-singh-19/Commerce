from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create"),
    path("filter", views.filter, name="filter"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("remove_from_watchlist/<int:id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("add_to_watchlist/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.display_watchlist, name="watchlist"),
    path("comment/<int:id>", views.add_comment, name="comment"),
    path("add_bid/<int:id>", views.add_bid, name="add_bid")
]
