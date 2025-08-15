from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Aluno, Responsavel, Professor, Materia, Turma, Contrato, Nota, DesempenhoAcademico, Presenca, Agenda, Livro

class AlunoSerializer(serializers.ModelSerializer):
    responsavel_nome = serializers.SerializerMethodField()

    def get_responsavel_nome(self, obj):
        if obj.responsavel:
            first = getattr(obj.responsavel, 'first_name', '')
            last = getattr(obj.responsavel, 'last_name', '')
            nome = (first + ' ' + last).strip()
            return nome if nome else '--'
        return '--'
    class Meta:
        model = Aluno
        fields = [
            'registration_number',
            'full_name',
            'email_aluno',
            'class_choices',
            'responsavel',
            'responsavel_nome',
            'phone_number_aluno',
            'cpf_aluno',
            'birthday_aluno',
        ]
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user
class ResponsavelSerializer(serializers.ModelSerializer):
    alunos_nomes = serializers.SerializerMethodField()
    def get_alunos_nomes(self, obj):
        nomes = [a.full_name for a in obj.alunos.all()]
        return nomes if nomes else []
    class Meta:
        model = Responsavel
        fields = '__all__'
class ProfessorSerializer(serializers.ModelSerializer):
    materias_nomes = serializers.SerializerMethodField()
    def get_materias_nomes(self, obj):
        nomes = [m.name for m in obj.materias.all()]
        return nomes if nomes else []
    class Meta:
        model = Professor
        fields = '__all__'
class MateriaSerializer(serializers.ModelSerializer):
    professor_nome = serializers.SerializerMethodField()

    def get_professor_nome(self, obj):
        if obj.professor:
            return getattr(obj.professor, 'full_name', None) or getattr(obj.professor, 'nome', None) or getattr(obj.professor, 'first_name', None) or '--'
        return '--'
    class Meta:
        model = Materia
        fields = '__all__'
class TurmaSerializer(serializers.ModelSerializer):
    representante_nome = serializers.SerializerMethodField()
    vice_representante_nome = serializers.SerializerMethodField()
    padrinho_nome = serializers.SerializerMethodField()

    def get_representante_nome(self, obj):
        if obj.representante:
            return getattr(obj.representante, 'full_name', None) or getattr(obj.representante, 'nome', None) or '--'
        return '--'

    def get_vice_representante_nome(self, obj):
        if obj.vice_representante:
            return getattr(obj.vice_representante, 'full_name', None) or getattr(obj.vice_representante, 'nome', None) or '--'
        return '--'

    def get_padrinho_nome(self, obj):
        if obj.padrinho:
            return getattr(obj.padrinho, 'full_name', None) or getattr(obj.padrinho, 'nome', None) or getattr(obj.padrinho, 'first_name', None) or '--'
        return '--'
    materias_nomes = serializers.SerializerMethodField()
    def get_materias_nomes(self, obj):
        nomes = []
        for m in [obj.materia_1, obj.materia_2, obj.materia_3, obj.materia_4]:
            if m: nomes.append(m.name)
        return nomes if nomes else []
    class Meta:
        model = Turma
        fields = '__all__'
class ContratoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.SerializerMethodField()
    turma_nome = serializers.CharField(source='turma.turma', read_only=True)
    responsavel_nome = serializers.SerializerMethodField()

    def get_aluno_nome(self, obj):
        if obj.aluno:
            return getattr(obj.aluno, 'full_name', None) or getattr(obj.aluno, 'nome', None) or '--'
        return '--'

    def get_responsavel_nome(self, obj):
        if obj.responsavel:
            return getattr(obj.responsavel, 'full_name', None) or getattr(obj.responsavel, 'nome', None) or getattr(obj.responsavel, 'first_name', None) or '--'
        return '--'
    class Meta:
        model = Contrato
        fields = '__all__'
class NotaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.SerializerMethodField()
    turma_nome = serializers.CharField(source='turma.turma', read_only=True)
    materia_nome = serializers.SerializerMethodField()

    def get_aluno_nome(self, obj):
        if obj.aluno:
            return getattr(obj.aluno, 'full_name', None) or getattr(obj.aluno, 'nome', None) or '--'
        return '--'

    def get_materia_nome(self, obj):
        if obj.materia:
            return getattr(obj.materia, 'name', None) or getattr(obj.materia, 'nome', None) or '--'
        return '--'
    class Meta:
        model = Nota
        fields = '__all__'
class DesempenhoAcademicoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.SerializerMethodField()
    turma_nome = serializers.CharField(source='turma.turma', read_only=True)
    materia_nome = serializers.SerializerMethodField()

    def get_aluno_nome(self, obj):
        if obj.aluno:
            return getattr(obj.aluno, 'full_name', None) or getattr(obj.aluno, 'nome', None) or '--'
        return '--'

    def get_materia_nome(self, obj):
        if obj.materia:
            return getattr(obj.materia, 'name', None) or getattr(obj.materia, 'nome', None) or '--'
        return '--'
    class Meta:
        model = DesempenhoAcademico
        fields = '__all__'
class PresencaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.SerializerMethodField()

    def get_aluno_nome(self, obj):
        if obj.aluno:
            return getattr(obj.aluno, 'full_name', None) or getattr(obj.aluno, 'nome', None) or '--'
        return '--'
    class Meta:
        model = Presenca
        fields = '__all__'
class AgendaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.SerializerMethodField()

    def get_usuario_nome(self, obj):
        if obj.usuario:
            return getattr(obj.usuario, 'full_name', None) or getattr(obj.usuario, 'nome', None) or getattr(obj.usuario, 'username', None) or '--'
        return '--'
    class Meta:
        model = Agenda
        fields = '__all__'
class LivroSerializer(serializers.ModelSerializer):
    usuario_em_uso_nome = serializers.SerializerMethodField()

    def get_usuario_em_uso_nome(self, obj):
        if obj.usuario_em_uso:
            return getattr(obj.usuario_em_uso, 'full_name', None) or getattr(obj.usuario_em_uso, 'nome', None) or getattr(obj.usuario_em_uso, 'username', None) or '--'
        return '--'
    class Meta:
        model = Livro
        fields = '__all__'