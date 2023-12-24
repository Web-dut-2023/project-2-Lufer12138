from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from .forms import *
from .models import *


def index(request):
    # selecting all list and all category
    AllCategory = Category.objects.all()
    CreatedList = CreateListing.objects.all()
    return render(request, "auctions/index.html", {
        "create_list": CreatedList,
        'all_Category': AllCategory,
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
# ----------------------------MyCode-------------------------------------#
# creating function for creating_list page
def create_list(request):
    # calling the form when user click on add list
    form = CreateListingForm()
    # if request is crating new list get create list page
    if request.method == "GET":
        # and display all category fro category table
        AllCategory = Category.objects.all()
        return render(request, "auctions/create_list.html", {
            'categories': AllCategory,
            'form': form
        })
    # if user enter data
    if request.method == 'POST':
        # insert user input to creating list in db
        # request.FILES for direct user upload data to media folder
        form = CreateListingForm(request.POST, request.FILES)
        # if it valid as forms requirement save it
        if form.is_valid():
            form.save()
    # and return to main page
    return HttpResponseRedirect(reverse(index))
# ---------------------------------------------------------------------------#
#function that get all category type 
def DisplayCategory(request):
    data = Category.objects.all()
    if request.method == "GET":
        return render(request, "auctions/DisplayCategory.html", {
            "data": data,
        })
# ----------------------------------------------------------------------------------#
def DisplayItems(request,CategoryType):
    #using filter if CategoryType is CategoryType and true
    if Category.objects.filter(CategoryType=CategoryType, status=True):
        #then filter the product of creating list by related category name
        product = CreateListing.objects.filter(category__CategoryType=CategoryType)
        #filtering the name of category section by first name only
        cat_name = Category.objects.filter(CategoryType=CategoryType).first()
        #page context for displaying data
        context = {'product':product,"cat_name":cat_name}
        return render(request,"auctions/DisplayItems.html",context)
#---------------------------------------------------------------------------------#
def ItemDetails(request,title,id):
    #giving the item variable category model Variable
    winner = 0
    item = CreateListing.objects.get(title=title,id=id)
    win = UserBid.objects.values_list('bid')
    for winner in win :
        if winner == item.price:
            return (winner)
    list_user = request.user.username == item.user
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = UserComment.objects.create(
                post=item,
                content=content,
                name=request.user
            )
    # return redirect('ItemDetails',title=title)
    #pass item variable to context
    context = {"item":item,"list_user":list_user,"winner":winner}
    #return view page with context
    return render(request,"auctions/ItemDetails.html",context)
#---------------------------------------------------------------------------------#
#displaying item of user WatchList
#1)
def watchList(request):
    if request.method=="GET":
        item = CreateListing.objects.filter(WatchList=request.user)
        return render(request,"auctions/WatchList.html",{
            "item":item
        })
# -------------->
#Adding items
#2)
def add_WatchList(request,id):
    #getting the item id from table
    item = CreateListing.objects.get(id=id)
    #if item is already exist inside WatchList
    if item.WatchList.filter(id=request.user.id).exists():
        messages.error(request,"the item is already in your WatchList")
        return HttpResponseRedirect(reverse("watchList"))
    else:
        #add_it
        item.WatchList.add(request.user)
        messages.success(request,"has been added successfully")
        return HttpResponseRedirect(reverse("watchList"))
#----------->
#removing items
#3)
def Remove_WatchList(request,id):
    item = CreateListing.objects.get(id=id)
    if item.WatchList.filter(id=request.user.id).exists():
        #remove it 
        item.WatchList.remove(request.user)
        messages.success(request,"has been Removed successfully")
        return HttpResponseRedirect(reverse("watchList"))
#---------------------------------------------------------------------------------#
def AddBid(request,id):
    item =CreateListing.objects.get(id=id)
    if request.method=="POST":
        input_bid = request.POST['input_bid']
        if float(input_bid) > item.price:
            new_price = UserBid(bidders=request.user,bid=float(input_bid),item_price=item)
            new_price.save()
            item.price = new_price.bid
            item.save()
            messages.success(request,"Bid has been added successfully") 
            return render(request,'auctions/ItemDetails.html',{'item':item})
        else:
            messages.warning(request,"Bid value must be more than the current") 
            return render(request,'auctions/ItemDetails.html',{'item':item})
#---------------------------------------------------------------------------------#
def status(request, id):
    item = CreateListing.objects.get(id=id)
    if request.method == "POST":
        item.status = False
        item.save()
        messages.success(request,"Auction has been closed successfully")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"auctions/ItemDetails.html",{
            "item":item,
        })