from django.views import generic 
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from tools.gurls import gurls 
from accounts.models import OthersInfo
from accounts.forms import UserCreateForm, OthersInfoForm
from django.db.models import Q

from django.contrib.auth import get_user_model
User = get_user_model()

# Cadastrando os usuários
class SignUp(generic.CreateView):
    template_name = 'accounts/signup.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')

# Controlando as outras informações do usario
class UserOthersInfo(LoginRequiredMixin, generic.CreateView):
    template_name = 'accounts/others-info.html'
    form_class = OthersInfoForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        
        if(self.object.sexo == 'Masculino'):
            self.object.avatar = 'accounts/image/avatar-m.jpg'
        elif(self.object.sexo == 'Feminino'):
            self.object.avatar = 'accounts/image/avatar-f.jpg'

        self.object.save()
        return super().form_valid(form)


# Redirecionando o usuario caso já tenha as outras informações ou não na plataforma
class RedirectInfo(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # Controlando os outros dados
        if self.request.user.is_authenticated:
            if not OthersInfo.objects.filter(user_id=self.request.user.id).exists():
                return reverse('accounts:others-info', kwargs={
                    'username':self.request.user.username,
                    'token':str(gurls())
                })
        return reverse_lazy('index')

# Informações do usuario cadastrado
class UserDetail(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'accounts/authenticated/accounts_perfil_detail.html'
    context_object_name = 'user'

# Atualizando os dados
class UserUpdate(LoginRequiredMixin, generic.UpdateView):
    template_name = 'accounts/authenticated/update/accounts_perfil_update.html'
    form_class = UserCreateForm
    model = User

    def get_success_url(self):
        return reverse('accounts:comments-list', kwargs={
        'username': self.request.user.username,
        'pk': self.request.user.id
    })

# Atualizando a foto de perfil
class UserUpdateProfile(LoginRequiredMixin, generic.UpdateView):
    model = OthersInfo
    fields = ['image']
    template_name = 'accounts/authenticated/update/accounts_image_update.html'

    def get_success_url(self):
        return reverse('accounts:detail-user', kwargs={
                'username': self.request.user.username,
                'pk': self.request.user.id
        })