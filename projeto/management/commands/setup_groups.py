from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from projeto.models import (
    Agenda, Aluno, Contrato, DesempenhoAcademico, Livro,
    Materia, Nota, Presenca, Professor, Responsavel, Turma
)

class Command(BaseCommand):
    help = "Configura os grupos e permissões iniciais"

    def handle(self, *args, **kwargs):
        # Define os grupos e os modelos associados
        groups_permissions = {
            "STAFF": [Agenda, Livro, Turma],
            "aluno(a)": [Agenda, Aluno, Nota, DesempenhoAcademico],
            "cordenacao": [Agenda, Aluno, Professor, Turma, Nota, DesempenhoAcademico],
            "devs": [Agenda, Aluno, Professor, Responsavel, Turma, Nota, Livro, Presenca, Contrato],
            "professor(a)": [Agenda, Nota, Presenca, Materia, Turma],
            "responsavel": [Agenda, Aluno, Contrato, Responsavel],
        }

        for group_name, models in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            self.stdout.write(f"Grupo '{group_name}' {'criado' if created else 'já existe'}.")

            for model in models:
                content_type = ContentType.objects.get_for_model(model)
                permissions = Permission.objects.filter(content_type=content_type)
                group.permissions.add(*permissions)
                self.stdout.write(f"Permissões atribuídas ao grupo '{group_name}' para o modelo '{model.__name__}'.")

        self.stdout.write(self.style.SUCCESS("Grupos e permissões configurados com sucesso!"))