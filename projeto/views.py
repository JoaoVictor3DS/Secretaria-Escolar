from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from .models import Contrato, Aluno, Responsavel, Professor, Turma, Nota, DesempenhoAcademico, Presenca, Agenda, Livro, Materia
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from .serializers import (
    AlunoSerializer, UserSerializer, ProfessorSerializer, ResponsavelSerializer,
    MateriaSerializer, TurmaSerializer, ContratoSerializer, NotaSerializer,
    DesempenhoAcademicoSerializer, PresencaSerializer, AgendaSerializer, LivroSerializer
)
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.apps import apps
from rest_framework import serializers
from rest_framework.permissions import BasePermission
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

class GroupPermission(BasePermission):
    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list('name', flat=True)
        model_name = view.queryset.model.__name__.lower()
        # Grupo devs tem permissão total
        #if 'devs' in user_groups:
            #return True
        group_permissions = {
            "devs": ["agenda", "aluno", "nota", "desempenhoacademico", "presenca", "materia", "turma", "contrato", "livro"],
            "aluno(a)": ["agenda", "aluno", "nota", "desempenhoacademico"],
            "professor(a)": ["agenda", "nota", "presenca", "materia", "turma"],
            "responsavel": ["agenda", "aluno", "contrato", "responsavel"],
            "cordenacao": ["agenda", "aluno", "nota", "desempenhoacademico", "presenca", "materia", "turma", "contrato", "livro"],
            "STAFF":["agenda", "aluno", "nota", "desempenhoacademico", "presenca", "materia", "turma", "contrato", "livro"],
        }
        for group in user_groups:
            if model_name in group_permissions.get(group, []):
                return True
        return 

def home(request):
    return render(request, 'home.html')

def contrato_pdf(request, contrato_id):
    contrato = get_object_or_404(Contrato, id=contrato_id)

    if contrato.aluno not in contrato.responsavel.alunos.all():
        return HttpResponse("Erro: O aluno não pertence ao responsável informado.", status=400)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contrato_{contrato.id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    margin_x = 50
    margin_y = 50
    line_height = 15
    current_y = height - margin_y

    def draw_wrapped_text(text, x, y, max_width):
        lines = simpleSplit(text, "Helvetica", 10, max_width)
        for line in lines:
            p.drawString(x, y, line)
            y -= line_height
        return y

    # Header
    p.setFont("Helvetica-Bold", 16)
    current_y -= 20
    p.drawString(margin_x, current_y, "CONTRATO DE MATRÍCULA ESCOLAR")

    # Introduction
    p.setFont("Helvetica", 10)
    current_y -= 30
    current_y = draw_wrapped_text(
        "Pelo presente instrumento particular, as partes abaixo assinadas, de um lado, a Escola Pedro Ludovico, "
        "doravante denominada Escola, e de outro lado, o responsável pelo aluno(a):",
        margin_x, current_y, width - 2 * margin_x
    )

    # Responsible Party Information
    p.setFont("Helvetica-Bold", 10)
    current_y -= 10
    current_y = draw_wrapped_text(
        f"Responsável: {contrato.responsavel.first_name} {contrato.responsavel.last_name}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"CPF: {contrato.responsavel.cpf}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"Endereço: {contrato.responsavel.address}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"E-mail: {contrato.responsavel.email}",
        margin_x, current_y, width - 2 * margin_x
    )

    # Student Information
    current_y -= 10
    current_y = draw_wrapped_text(
        f"Aluno: {contrato.aluno.full_name}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"Turma: {contrato.turma}",
        margin_x, current_y, width - 2 * margin_x
    )

    # Contract Clauses
    p.setFont("Helvetica", 10)
    current_y -= 20
    current_y = draw_wrapped_text(
        "Cláusula 1 - OBJETO DO CONTRATO",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"1.1 O presente contrato tem por objeto a matrícula do aluno(a) {contrato.aluno.full_name}, "
        f"na turma {contrato.turma} do ano letivo de {contrato.turma.turma} na Escola Pedro Ludovico.",
        margin_x, current_y, width - 2 * margin_x
    )

    current_y -= 10
    current_y = draw_wrapped_text(
        "Cláusula 2 - OBRIGAÇÕES DO RESPONSÁVEL",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        """2.1 O Responsável compromete-se a realizar o pagamento das mensalidades escolares 
        dentro dos prazos estabelecidos.""",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "2.2 O Responsável deverá comunicar à Escola qualquer alteração nos dados cadastrais do aluno(a).",
        margin_x, current_y, width - 2 * margin_x
    )

    current_y -= 10
    current_y = draw_wrapped_text(
        "Cláusula 3 - DISPOSIÇÕES GERAIS",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        """3.1 As partes acordam que todas as informações fornecidas durante o processo 
        de matrícula serão tratadas de forma confidencial.""",        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "3.2 Este contrato poderá ser alterado mediante acordo mútuo entre as partes.",
        margin_x, current_y, width - 2 * margin_x
    )

    # Signatures
    p.setFont("Helvetica-Bold", 10)
    current_y -= 30
    current_y = draw_wrapped_text(
        "Responsável:",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Assinatura: ________________________________",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"Nome: {contrato.responsavel.first_name} {contrato.responsavel.last_name}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        f"CPF: {contrato.responsavel.cpf}",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Data: ____/____/________",
        margin_x, current_y, width - 2 * margin_x
    )

    current_y -= 20
    current_y = draw_wrapped_text(
        "Escola:",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Assinatura: ________________________________",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Nome do Representante: Clabreso",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Cargo: Coordenador de Turno",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Data: ____/____/________",
        margin_x, current_y, width - 2 * margin_x
    )

    # Witnesses
    current_y -= 20
    current_y = draw_wrapped_text(
        "Testemunhas:",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Nome: ______________________________________",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Assinatura: ________________________________",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Nome: ______________________________________",
        margin_x, current_y, width - 2 * margin_x
    )
    current_y = draw_wrapped_text(
        "Assinatura: ________________________________",
        margin_x, current_y, width - 2 * margin_x
    )

    p.save()

    return response

def login_view(request):
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alunos_api(request):
    alunos = Aluno.objects.all()
    serializer = AlunoSerializer(alunos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def responsaveis_api(request):
    responsaveis = Responsavel.objects.all()
    serializer = ResponsavelSerializer(responsaveis, many=True)
    return Response(serializer.data)

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        group_name = self.request.data.get('group')
        valid_groups = ['devs', 'cordenacao', 'STAFF', 'aluno(a)', 'professor(a)', 'responsavel']
        if group_name not in valid_groups:
            raise serializers.ValidationError({'group': 'Grupo inválido.'})
        user = serializer.save()
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        user.save()

        if group_name == 'responsavel':
            responsavel_data = {
                'first_name': self.request.data.get('first_name'),
                'last_name': self.request.data.get('last_name'),
                'phone_number': self.request.data.get('phone_number'),
                'email': user.email,
                'address': self.request.data.get('address'),
                'cpf': self.request.data.get('cpf'),
                'birthday': self.request.data.get('birthday'),
                'user_group': group,
                'user': user
            }
            responsavel = Responsavel.objects.create(**responsavel_data)
            alunos_ids = self.request.data.get('alunos', [])
            responsavel.alunos.set(Aluno.objects.filter(registration_number__in=alunos_ids))
        elif group_name == 'professor(a)':
            professor_data = {
                'first_name': self.request.data.get('first_name'),
                'last_name': self.request.data.get('last_name'),
                'phone_number': self.request.data.get('phone_number'),
                'email': user.email,
                'address': self.request.data.get('address'),
                'cpf': self.request.data.get('cpf'),
                'registration_number': self.request.data.get('registration_number'),
                'user_group': group,
                'user': user
            }
            professor = Professor.objects.create(**professor_data)
            materias_ids = self.request.data.get('materias', [])
            if materias_ids:
                professor.materias.set(Materia.objects.filter(id__in=materias_ids))
            professor.save()
        elif group_name == 'aluno(a)':
            aluno_data = {
                'full_name': self.request.data.get('full_name'),
                'phone_number_aluno': self.request.data.get('phone_number_aluno'),
                'email_aluno': self.request.data.get('email_aluno'),
                'cpf_aluno': self.request.data.get('cpf_aluno'),
                'birthday_aluno': self.request.data.get('birthday_aluno'),
                'class_choices': self.request.data.get('class_choices'),
                'responsavel_id': self.request.data.get('responsavel'),
                'user_group': group,
                'user': user
            }
            Aluno.objects.create(**aluno_data)

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ResponsavelListView(generics.ListAPIView):
    queryset = Responsavel.objects.all()
    serializer_class = ResponsavelSerializer
    permission_classes = [IsAuthenticated]

class ProfessorListView(generics.ListAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]

class AlunoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'registration_number'

class ProfessorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class ResponsavelDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Responsavel.objects.all()
    serializer_class = ResponsavelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

# Serializers para os outros modelos
class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'

class DesempenhoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesempenhoAcademico
        fields = '__all__'

class PresencaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        fields = '__all__'

class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = '__all__'

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = '__all__'

# ViewSets para os outros modelos
class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

    def get_permissions(self):
        # Permite acesso público para listagem (GET), exige autenticação para outros métodos
        if self.action == 'list':
            return []
        return [IsAuthenticated()]

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [IsAuthenticated]

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    permission_classes = [IsAuthenticated]

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticated]

class DesempenhoAcademicoViewSet(viewsets.ModelViewSet):
    queryset = DesempenhoAcademico.objects.all()
    serializer_class = DesempenhoAcademicoSerializer
    permission_classes = [IsAuthenticated]

class PresencaViewSet(viewsets.ModelViewSet):
    queryset = Presenca.objects.all()
    serializer_class = PresencaSerializer
    permission_classes = [IsAuthenticated]

class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    permission_classes = [IsAuthenticated, GroupPermission]

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_data_api(request):
    user = request.user
    groups = list(user.groups.values_list('name', flat=True))
    is_superuser = user.is_superuser

    # Descobre todos os models do app 'projeto' que possuem API
    app_models = apps.get_app_config('projeto').get_models()
    model_names = [m.__name__.lower() for m in app_models]
    # Mapeia nomes amigáveis para URLs (ajuste se necessário)
    model_url_map = {
        'aluno': 'alunos',
        'professor': 'professores',
        'responsavel': 'responsaveis',
        'materia': 'materias',
        'turma': 'turmas',
        'contrato': 'contratos',
        'nota': 'notas',
        'desempenhoacademico': 'desempenhoacademico',
        'presenca': 'presencas',
        'agenda': 'agendas',
        'livro': 'livros',
    }
    # Permissões padrão por grupo
    group_perms = {
        'devs': ['view', 'add', 'edit', 'delete'],
        'cordenacao': ['view', 'add', 'edit', 'delete'],
        'STAFF': ['view', 'edit'],
        'responsavel': ['view'],
        'aluno(a)':['view'],
        'professor(a)':['view','add','edit'],  # Permissão de view para todos os modelos
    }
    # Calcula permissões do usuário para cada model
    user_models = {}
    lower_groups = [g.lower() for g in groups]
    for model in model_names:
        url_name = model_url_map.get(model, model)
        perms = set()
        if 'devs' in lower_groups:
            perms = set(group_perms['devs'])
        elif 'cordenacao' in lower_groups:
            perms = set(group_perms['cordenacao'])
        elif 'STAFF' in lower_groups:
            perms = set(group_perms['STAFF'])
        elif 'responsavel' in lower_groups:
            perms = set(group_perms['responsavel'])
        user_models[url_name] = list(perms)

    # Substitui grupos por models equivalentes
    user_profile_data = {}
    if 'responsavel' in lower_groups:
        try:
            responsavel = Responsavel.objects.get(email=user.email)
            user_profile_data['responsavel'] = ResponsavelSerializer(responsavel).data
        except Responsavel.DoesNotExist:
            user_profile_data['responsavel'] = None
    if 'aluno(a)' in lower_groups:
        try:
            aluno = Aluno.objects.get(email_aluno=user.email)
            user_profile_data['aluno'] = AlunoSerializer(aluno).data
        except Aluno.DoesNotExist:
            user_profile_data['aluno'] = None
    if 'professor(a)' in lower_groups:
        try:
            professor = Professor.objects.get(email=user.email)
            user_profile_data['professor'] = ProfessorSerializer(professor).data
        except Professor.DoesNotExist:
            user_profile_data['professor'] = None
    return Response({
        'username': user.username,
        'email': user.email,
        'groups': groups,
        'models_permissions': user_models,
        'profile_data': user_profile_data,
    })

# Função utilitária para checar grupo

def user_in_group(user, group_names):
    return user.is_authenticated and any(g.name in group_names for g in user.groups.all())

# View home pública, sem login_required
def home(request):
    return render(request, 'home.html')

# View para listar contratos com permissões
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy

@method_decorator(login_required, name='dispatch')
class ContratoListView(ListView):
    model = Contrato
    template_name = 'contratos_list.html'
    context_object_name = 'contratos'

    def get_queryset(self):
        user = self.request.user
        groups = list(user.groups.values_list('name', flat=True))
        qs = Contrato.objects.all()
        if 'STAFF' in groups:
            return qs
        elif 'cordenacao' in groups or 'devs' in groups:
            return qs
        else:
            return Contrato.objects.none()

@method_decorator(login_required, name='dispatch')
class ContratoUpdateView(UpdateView):
    model = Contrato
    fields = ['turma', 'aluno', 'responsavel', 'email_responsavel', 'signed_contract']
    template_name = 'contrato_edit.html'
    success_url = reverse_lazy('contratos_list')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        groups = list(user.groups.values_list('name', flat=True))
        if 'cordenacao' in groups or 'devs' in groups:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponse('Acesso negado', status=403)

# View para baixar contrato
@login_required
def contrato_download(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if not contrato.signed_contract:
        return HttpResponse('Contrato não enviado.', status=404)
    response = HttpResponse(contrato.signed_contract, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{contrato.signed_contract.name.split("/")[-1]}"'
    return response

# View para listar usuários com filtro por grupo
@login_required
def usuarios_list(request):
    group_filter = request.GET.get('group')
    users = User.objects.all()
    if group_filter:
        users = users.filter(groups__name=group_filter)
    grupos = Group.objects.all()
    return render(request, 'usuarios_list.html', {'usuarios': users, 'grupos': grupos, 'group_filter': group_filter})