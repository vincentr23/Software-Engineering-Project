from django.shortcuts import render, redirect, get_object_or_404

from .models import MainMenu, Favorite, Book, ShoppingCart, Comment
from .forms import BookForm, FeedbackForm, CommentForm

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required


@login_required(login_url=reverse_lazy('login'))
def index(request):
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


def aboutus(request):
    return render(request,
                  'bookMng/aboutus.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
                book.rating = 0
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'form': form,
                      'submitted': submitted
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.all()
    for b in books:
        b.is_favorite = request.user.is_authenticated and request.user.favorite_set.filter(book=b).exists()
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.is_favorite = request.user.is_authenticated and request.user.favorite_set.filter(book=b).exists()
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                       'item_list': MainMenu.objects.all(),
                       'books': books
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.is_favorite = request.user.is_authenticated and request.user.favorite_set.filter(book=book).exists()
    book.pic_path = book.picture.url[14:]
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )


def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )


def searchbook(request):
    books = Book.objects.filter(name=request.GET.get('search', ''))
    for b in books:
        b.is_favorite = request.user.is_authenticated and request.user.favorite_set.filter(book=b).exists()
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/searchbook.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


@login_required
def favorite_book(request, book_id):
    books = Book.objects.get(id=book_id)
    user = request.user

    # Check if the user has already favorited the book
    if user.favorite_set.filter(book=books).exists():
        # User has already favorited the book, unfavorite it
        user.favorite_set.filter(book=books).delete()
    else:
        # User has not favorited the book, favorite it
        Favorite.objects.create(user=user, book=books)

    # Retrieve the list of books again after updating favorites
    books = Book.objects.all()
    for b in books:
        b.is_favorite = request.user.is_authenticated and request.user.favorite_set.filter(book=b).exists()
        b.pic_path = b.picture.url[14:]

    return redirect(request.META.get('HTTP_REFERER', 'displaybooks'))


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                'Feedback from {}'.format(name),
                'Email: {}\n\n{}'.format(email, message),
                email,  # Replace with your email address
                [''],  # Replace with the recipient's email address
                fail_silently=False,
            )

            return redirect('thank_you')
    else:
        form = FeedbackForm()

    return render(request,
                  'bookMng/feedback.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'form': form
                  }
                  )


def thank_you(request):
    return render(request,
                  'bookMng/thank_you.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def viewcart(request):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    books = shopping_cart.books.all()

    total_price = sum(book.price for book in books)

    return render(request,
                  'bookMng/shoppingCart.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'total_price': total_price,
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def addtocart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Assuming you have a ShoppingCart model to store cart items
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    shopping_cart.books.add(book)

    # Redirect to the shopping cart page with the updated information
    return redirect('displaybooks')  # Assuming the name of your shopping cart URL is 'view_cart'


@login_required(login_url=reverse_lazy('login'))
def deletefromcart(request, book_id):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    book = get_object_or_404(Book, id=book_id)

    if book in shopping_cart.books.all():
        shopping_cart.books.remove(book)
        return redirect('viewcart')


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    comments = Comment.objects.filter(book=book).order_by('-created_at')  # Get comments for the book
    return render(request, 'bookMng/book_detail.html', {'item_list': MainMenu.objects.all(), 'book': book, 'comments': comments})


@login_required(login_url=reverse_lazy('login'))
def add_comment(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            Comment.objects.create(book=book, user=request.user, text=text)
    return redirect('book_detail', book_id=book_id)


def purchase_cart(request):
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=request.user)

    for book in shopping_cart.books.all():
        shopping_cart.books.remove(book)
    return redirect('purchase_success')


def purchase_success(request):
    return render(request,
                  'bookMng/purchase_success.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def favorites(request):
    books = Book.objects.all()
    for b in books:
        b.is_favorite = request.user.is_authenticated and request.user.favorite_set.filter(book=b).exists()
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/favorites.html',
                  {
                       'item_list': MainMenu.objects.all(),
                       'books': books
                  }
                  )