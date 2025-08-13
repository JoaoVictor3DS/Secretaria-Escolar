from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/materias', views.MateriaViewSet, basename='materias')
router.register(r'api/turmas', views.TurmaViewSet, basename='turmas')
router.register(r'api/contratos', views.ContratoViewSet, basename='contratos')
router.register(r'api/notas', views.NotaViewSet, basename='notas')
router.register(r'api/desempenhoacademico', views.DesempenhoAcademicoViewSet, basename='desempenhoacademico')
router.register(r'api/presencas', views.PresencaViewSet, basename='presencas')
router.register(r'api/agendas', views.AgendaViewSet, basename='agendas')
router.register(r'api/livros', views.LivroViewSet, basename='livros')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('api/alunos/', views.alunos_api, name='alunos_api'),
    path('api/register/', views.CreateUserView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('api/user-data/', views.user_data_api, name='user_data'),
    path('api/responsaveis/', views.responsaveis_api, name='responsaveis_api'),
    path('api/professores/', views.ProfessorListView.as_view(), name='professores_api'),
    path('api/alunos/<int:registration_number>/', views.AlunoDetailView.as_view(), name='aluno_detail_api'),
    path('api/professores/<int:id>/', views.ProfessorDetailView.as_view(), name='professor_detail_api'),
    path('api/responsaveis/<int:id>/', views.ResponsavelDetailView.as_view(), name='responsavel_detail_api'),
    path('contratos/', views.ContratoListView.as_view(), name='contratos_list'),
    path('contrato/<int:pk>/edit/', views.ContratoUpdateView.as_view(), name='contrato_edit'),
    path('contrato/<int:pk>/download/', views.contrato_download, name='contrato_download'),
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)