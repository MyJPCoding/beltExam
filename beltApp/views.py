from django.shortcuts import render, redirect
from beltApp.models import User, Wish
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):

    return render(request,'index.html')

def register(request):
    print(request.POST)
    # TODO
    # read post data
    errors = User.objects.register_validator(request.POST)
    # validate
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        # hash the pw
        hash_browns = bcrypt.hashpw(
            request.POST['password'].encode(),
            bcrypt.gensalt()
        ).decode()
        print('hash_browns: ', hash_browns)
        # create a user
        created_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            # password=request.POST['password']
            password=hash_browns
        )
        print('created_user.password: ', created_user.password)
        # set them up in session
        request.session['uuid'] = created_user.id
        return redirect('/wishes')

def logout(request):
    request.session.flush()
    return redirect('/')

def login(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        # check the email in the db
        users_list = User.objects.filter(email=request.POST['email'])
        # set up user in session
        request.session['uuid'] = users_list[0].id
        return redirect('/wishes')

def wishes(request):
    # check if a user is not in session
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['uuid']),

        'user_name': User.objects.get(id=request.session['uuid']).first_name,

        'all_my_active_wishes': Wish.objects.filter(
            uploaded_by=User.objects.get(id=request.session['uuid']), 
            is_granted="False"
        ),

        'all_granted_wishes': Wish.objects.filter( 
            is_granted="True"
        ),
    }
    return render(request, 'wishes.html', context)

def new_wish(request):
    context = {
        'user': User.objects.get(id=request.session['uuid']),
        'user_name': User.objects.get(id=request.session['uuid']).first_name,
        # 'all_the_BOOKS': BOOK.objects.all(),
    }
    return render(request, 'new_wish.html', context)

def create_wish(request):
    errors = User.objects.wish_validator(request.POST)
    # validate
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        created_wish = Wish.objects.create(
            name=request.POST['wish_name'], 
            desc=request.POST['wish_desc'],
            uploaded_by=User.objects.get(id=request.session['uuid']),
        )
        return redirect('/wishes')

def like_wish(request, wish_id ):
    # update the wish to likedd
    # get the pet
    user = User.objects.get(id=request.session['uuid'])
    wish = Wish.objects.get(id=wish_id)
    user.liked_wishes.add(wish)
    user.save()
    return redirect('/wishes')

def grant_wish(request, wish_id):
    # user = User.objects.get(id=request.session['uuid'])
    wish = Wish.objects.get(id=wish_id)
    wish.is_granted = True
    wish.save()
    return redirect('/wishes')

def edit_wish(request, wish_id):
    context = {
        'wish': Wish.objects.get(id=wish_id),
        'user': User.objects.get(id=request.session['uuid']),
    }
    return render(request, 'edit.html', context)

def post_edit(request, wish_id):
    errors = User.objects.wish_validator(request.POST)
    # validate
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/wishes/edit/{wish_id}')
    else:
        updated_wish = Wish.objects.get(id=wish_id)
        updated_wish.name = request.POST['wish_name']
        updated_wish.desc = request.POST['wish_desc']
        updated_wish.save()
    return redirect('/wishes')

def remove(request, wish_id):
    removed_wish = Wish.objects.get(id=wish_id)
    removed_wish.delete()
    return redirect('/wishes')

def stats(request):
    

    context = {
        'user': User.objects.get(id=request.session['uuid']),

        'wishes': Wish.objects.all(),

        'all_my_active_wishes': Wish.objects.filter(
            uploaded_by=User.objects.get(id=request.session['uuid']), 
            is_granted="False"
        ),

        'all_granted_wishes': Wish.objects.filter( 
            uploaded_by=User.objects.get(id=request.session['uuid']),
            is_granted="True"
        ),

        'total_count': Wish.objects.filter( 
        is_granted="True"
        ),
    }
    return render(request, 'stats.html', context)