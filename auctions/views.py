from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

from .models import User


def index(request):
    return render(request, "auctions/index.html", {
        "all_listings": Listing.objects.filter(active=True).all(),
        "categories": Category.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "categories": Category.objects.all()
        })
    else:
        user = request.user
        title = request.POST["title"]
        price = request.POST["price"]
        description = request.POST["description"]
        image = request.POST["image"]
        category = request.POST["category"]

        category_name = Category.objects.get(category_name=category)

        bid = Bid(bid=float(price), user=user)
        bid.save()

        new_listing = Listing(
            title=title,
            price=bid,
            description=description,
            image=image,
            category=category_name,
            seller=user
        )
        new_listing.save()

        return HttpResponseRedirect(reverse(index))


def filter(request):
    if request.method == "POST":
        selected_filter = request.POST["category"]
        filtered_items = Category.objects.get(category_name=selected_filter)
    return render(request, "auctions/index.html", {
        "all_listings": Listing.objects.filter(active=True, category=filtered_items).all(),
        "categories": Category.objects.all(),
    })


def listing(request, id):
    is_owner = request.user.username == Listing.objects.get(pk=id).seller.username

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=id),
        "listing_in_watchlist": request.user in Listing.objects.get(pk=id).watchlist.all(),
        "comments": Comment.objects.filter(listing=Listing.objects.get(pk=id)),
        "is_owner": is_owner
    })


def remove_from_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args={id, }))


def add_to_watchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args={id, }))


def display_watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "user": request.user,
        "all_listings": request.user.watchlist.all()
    })


def add_comment(request, id):
    new_comment = Comment(
        commenter=request.user,
        listing=Listing.objects.get(pk=id),
        message=request.POST['new_comment']
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args={id, }))


def add_bid(request, id):
    newBid = request.POST['new_bid']
    listing = Listing.objects.get(pk=id)

    is_owner = request.user.username == Listing.objects.get(pk=id).seller.username

    if int(newBid) > listing.price.bid:
        updated_bid = Bid(user=request.user, bid=int(newBid))
        updated_bid.save()
        listing.price = updated_bid
        listing.save()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Bid was placed successfully",
            "update": True,
            "listing_in_watchlist": request.user in Listing.objects.get(pk=id).watchlist.all(),
            "comments": Comment.objects.filter(listing=Listing.objects.get(pk=id)),
            "is_owner": is_owner
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Failed to place bid",
            "update": True,
            "listing_in_watchlist": request.user in Listing.objects.get(pk=id).watchlist.all(),
            "comments": Comment.objects.filter(listing=Listing.objects.get(pk=id)),
            "is_owner": is_owner
        })


def close_auction(request, id):
    listing_data = Listing.objects.get(pk=id)
    listing_data.active = False
    listing_data.save()

    is_owner = request.user.username == Listing.objects.get(pk=id).seller.username

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=id),
        "listing_in_watchlist": request.user in Listing.objects.get(pk=id).watchlist.all(),
        "comments": Comment.objects.filter(listing=Listing.objects.get(pk=id)),
        "is_owner": is_owner,
        "update": True,
        "message": "Your auction is now closed"
    })
