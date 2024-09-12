from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from blog.models import Article
from .models import User
from .forms import PofileForm, SignupForm
from .mixins import (FieldMixin,
                     FormValidMixin,
                     AuthorAccessMixin,
                     AuthorsAccessMixin,
                     SuperUserAccessMixin
                    )


@login_required
def home(request):
    #defult send user object
    #user.get_full_name
    return render(request, 'registration/home.html')


# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            login(request, user)
            return render(request, 'registration/home.html')
            
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})

# def login(request):
#     user = request.user
#     if user.is_authenticated():
#         return reverse_lazy("account:home") if (user.is_superuser or user.is_author) \
#             else reverse_lazy("account:profile")

class Login(LoginView):
    
    def get_success_url(self) -> str:
        user = self.request.user

        if user.is_superuser or user.is_author :
            return reverse_lazy("account:home")
        else:
            return reverse_lazy("account:profile")
        

@login_required
def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def users_list(request):
    #get all user list
    #show user information and edit
    pass




class ArticleList(AuthorsAccessMixin, ListView):
    
    template_name = 'registration/home.html'

    def get_queryset(self) :
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author = self.request.user)
        

class ArticleCreate(AuthorsAccessMixin, FormValidMixin, FieldMixin, CreateView):
    model = Article
    template_name = 'registration/article-create-update.html'



class ArticleUpdate(AuthorAccessMixin, FormValidMixin, FieldMixin, UpdateView):
    model = Article
    template_name = 'registration/article-create-update.html'


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("account:home")
    template_name = "registration/article_confirm_delete.html"


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = PofileForm
    success_url = reverse_lazy("account:profile")
    

    def get_object(self) :
        return User.objects.get(pk = self.request.user.pk)
    
    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()

        kwargs.update({
            'user':self.request.user
        })
        return kwargs
    







# class PasswordChange(PasswordChangeView):
#     django.contrib.auth.views import PasswordChangeView
#     # success_url = reverse_lazy("account:profile")
#     success_url = reverse_lazy("account:password_change_done")


