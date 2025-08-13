from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Aluno, Responsavel, Professor, Materia, Turma, Contrato, Nota, DesempenhoAcademico, Presenca, Agenda, Livro

class AlunoSerializer(serializers.ModelSerializer):
    responsavel_nome = serializers.CharField(source='responsavel.first_name', read_only=True)
    class Meta:
        model = Aluno
        fields = ['registration_number', 'full_name', 'email_aluno', 'class_choices', 'responsavel', 'responsavel_nome']
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
    professor_nome = serializers.CharField(source='professor.first_name', read_only=True)
    class Meta:
        model = Materia
        fields = '__all__'
class TurmaSerializer(serializers.ModelSerializer):
    representante_nome = serializers.CharField(source='representante.full_name', read_only=True)
    vice_representante_nome = serializers.CharField(source='vice_representante.full_name', read_only=True)
    padrinho_nome = serializers.CharField(source='padrinho.first_name', read_only=True)
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
    aluno_nome = serializers.CharField(source='aluno.full_name', read_only=True)
    turma_nome = serializers.CharField(source='turma.turma', read_only=True)
    responsavel_nome = serializers.CharField(source='responsavel.first_name', read_only=True)
    class Meta:
        model = Contrato
        fields = '__all__'
class NotaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.full_name', read_only=True)
    turma_nome = serializers.CharField(source='turma.turma', read_only=True)
    materia_nome = serializers.CharField(source='materia.name', read_only=True)
    class Meta:
        model = Nota
        fields = '__all__'
class DesempenhoAcademicoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.full_name', read_only=True)
    turma_nome = serializers.CharField(source='turma.turma', read_only=True)
    materia_nome = serializers.CharField(source='materia.name', read_only=True)
    class Meta:
        model = DesempenhoAcademico
        fields = '__all__'
class PresencaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.full_name', read_only=True)
    class Meta:
        model = Presenca
        fields = '__all__'
class AgendaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    class Meta:
        model = Agenda
        fields = '__all__'
class LivroSerializer(serializers.ModelSerializer):
    usuario_em_uso_nome = serializers.CharField(source='usuario_em_uso.username', read_only=True)
    class Meta:
        model = Livro
        fields = '__all__'
