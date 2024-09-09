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


































#این کد های پایین روش قدیمی بود 



# from django.http import HttpResponse
# from django.contrib.auth import login
# from .forms import SignupForm
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from .tokens import account_activation_token
# from django.core.mail import EmailMessage

#CreateView برای ایجاد کردن یه یوذر از این مدل استفاده میکنیم


# class Register(CreateView):
#     form_class = SignupForm
#     template_name = 'registration/register.html'

#     def form_valid(self, form):
#         #اگر فرم ولید بود وارد این فانکش میشه
#         #بعد فرم رو سیو میکنه ولی نهاییش نمیکنه
#         #فعال بودن بوذر رو هم غیرفعال میکنه
#         #بعدش یوذر رو ایجاد میکنه
#         #get_current_site میاد ادرس سایت رو میگیره

#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()
#         current_site = get_current_site(self.request)
#         mail_subject = 'فعالسازی اکانت'

#         #پارامتر اول میگه برو کدوم تمپلیت پارامتر دوم میگه کانتکسش چی باشه
#         message = render_to_string('registration/activate_account.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#             'token':account_activation_token.make_token(user),
#         })
#         #ادرس ایمیل که توی فرم یوذر وارد کرده بود رو گرفته و بقیه کارهارو انجام داه
#         to_email = form.cleaned_data.get('email')
#         email = EmailMessage(
#                     mail_subject, message, to=[to_email]
#         )
#         email.send()
#         return HttpResponse('لینک فعالسازی به ایمیل شما ارسال شد.')




# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         #این خط پایین میاد بعد از اینکه روی لینک ثبت نام زد وارد حساب بشه اگه نباشه هم چیزی نمیشه
#         login(request, user)
#         # return redirect('home')
#         return HttpResponse('اکانت شما با موفقیت فعال شد')
#     else:
#         return HttpResponse('لینک فعالسازی منقضی شده است دوباره امتحان کنید <a href="/register">ثبت نام</a>!')





#این روش فانکشن بیس هست و روش کلس بیس رو بالا نوشتم
#دوخط اول با این دوخط اول برابر هستن ایجاد فرم و نوع درخواست
# if form.is_valid() == def form_valid(self, form) -> True

# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your blog account.'
#             message = render_to_string('acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('لینک فعال سازی به ایمیل شما ارسال شد<a href="/login">ورود</a>')
#     else:
#         form = SignupForm()
#     return render(request, 'signup.html', {'form': form})