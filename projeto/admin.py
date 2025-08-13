from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.utils.html import format_html
from django.urls import reverse
from .models import Responsavel, Aluno, Professor, Turma, Contrato
from .models import Nota, Materia
from .models import DesempenhoAcademico, Presenca, Agenda, Livro

class ResponsaveisAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'cpf', 'birthday')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'cpf', 'email')  # Add CPF and email to search fields
    list_filter = ('first_name', 'last_name', 'birthday')  # Add birthday to filters
    filter_horizontal = ('alunos',)  # Allow selecting multiple alunos dynamically

class NotasInline(admin.TabularInline):
    model = Nota
    fields = ('materia', 'nota_presenca', 'nota_atividade', 'nota_avaliativa', 'nota_final')
    readonly_fields = ('nota_final',)
    extra = 0  # Do not show extra empty forms

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number_aluno', 'email_aluno', 'cpf_aluno', 'birthday_aluno', 'registration_number', 'class_choices', 'responsavel')
    list_display_links = ('full_name',)
    search_fields = ('full_name', 'registration_number', 'responsavel__first_name', 'responsavel__last_name')
    list_filter = ('class_choices', 'responsavel')
    inlines = [NotasInline]  # Add NotasInline to display and edit Notas for each Materia

    def view_notas(self, obj):
        url = reverse('admin:projeto_notas_changelist') + f'?aluno__id__exact={obj.id}'
        return format_html('<a href="{}">Ver Notas</a>', url)

    view_notas.short_description = "Notas"

class MateriaInline(admin.TabularInline):
    model = Materia
    extra = 1

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'cpf', 'registration_number')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    list_filter = ('first_name', 'last_name')
    filter_horizontal = ('materias',)  # Allow selecting multiple existing Materias
    inlines = [MateriaInline]

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('turma', 'materia_1', 'materia_2', 'materia_3', 'materia_4', 'representante', 'vice_representante', 'padrinho')
    list_display_links = ('turma',)
    search_fields = ('turma', 'materia_1__name', 'materia_2__name', 'materia_3__name', 'materia_4__name')
    list_filter = ('turma',)

class ContratoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'responsavel', 'turma', 'email_responsavel', 'download_signed_contract')
    list_display_links = ('aluno',)
    search_fields = ('aluno__full_name', 'responsavel__first_name', 'turma__turma')
    list_filter = ('turma',)

    actions = ['generate_pdf']

    def generate_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="contratos.pdf"'

        p = canvas.Canvas(response)
        line_height = 15  # Define line spacing

        for contrato in queryset:
            current_y = 800  # Reset Y position for each contract

            # Header
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, current_y, "CONTRATO DE MATRÍCULA ESCOLAR")
            current_y -= 30

            # Introduction
            p.setFont("Helvetica", 10)
            p.drawString(100, current_y, "Pelo presente instrumento particular, as partes abaixo assinadas, de um lado, a Escola Pedro Ludovico,")
            current_y -= line_height
            p.drawString(100, current_y, "doravante denominada Escola, e de outro lado, o responsável pelo aluno(a):")
            current_y -= 2 * line_height

            # Responsible Party Information
            p.setFont("Helvetica-Bold", 10)
            p.drawString(100, current_y, f"Responsável: {contrato.responsavel.first_name} {contrato.responsavel.last_name}")
            current_y -= line_height
            p.drawString(100, current_y, f"CPF: {contrato.responsavel.cpf}")
            current_y -= line_height
            p.drawString(100, current_y, f"Endereço: {contrato.responsavel.address}")
            current_y -= line_height
            p.drawString(100, current_y, f"E-mail: {contrato.responsavel.email}")
            current_y -= 2 * line_height

            # Student Information
            p.drawString(100, current_y, f"Aluno: {contrato.aluno.full_name}")
            current_y -= line_height
            p.drawString(100, current_y, f"Turma: {contrato.turma}")
            current_y -= 2 * line_height

            # Contract Clauses
            p.setFont("Helvetica", 10)
            p.drawString(100, current_y, "Cláusula 1 - OBJETO DO CONTRATO")
            current_y -= line_height
            p.drawString(100, current_y, f"1.1 O presente contrato tem por objeto a matrícula do aluno(a) {contrato.aluno.full_name},")
            current_y -= line_height
            p.drawString(100, current_y, f"na turma {contrato.turma} do ano letivo de {contrato.turma.turma} na Escola Pedro Ludovico.")
            current_y -= 2 * line_height

            p.drawString(100, current_y, "Cláusula 2 - OBRIGAÇÕES DO RESPONSÁVEL")
            current_y -= line_height
            p.drawString(100, current_y, "2.1 O Responsável compromete-se a realizar o pagamento das ")
            current_y -= line_height
            p.drawString(100, current_y, "    mensalidades escolares dentro dos prazos estabelecidos.")
            current_y -= line_height
            p.drawString(100, current_y, "2.2 O Responsável deverá comunicar à Escola qualquer alteração nos dados cadastrais do aluno(a).")
            current_y -= 2 * line_height

            p.drawString(100, current_y, "Cláusula 3 - DISPOSIÇÕES GERAIS")
            current_y -= line_height
            p.drawString(100, current_y, "3.1 As partes acordam que todas as informações fornecidas durante o processo de matrícula")
            current_y -= line_height
            p.drawString(100, current_y, "    serão tratadas de forma confidencial.")
            current_y -= line_height
            p.drawString(100, current_y, "3.2 Este contrato poderá ser alterado mediante acordo mútuo entre as partes.")
            current_y -= 2 * line_height

            # Signatures
            p.setFont("Helvetica-Bold", 10)
            p.drawString(100, current_y, "Responsável:")
            current_y -= line_height
            p.drawString(100, current_y, "Assinatura: ________________________________")
            current_y -= line_height
            p.drawString(100, current_y, f"Nome: {contrato.responsavel.first_name} {contrato.responsavel.last_name}")
            current_y -= line_height
            p.drawString(100, current_y, f"CPF: {contrato.responsavel.cpf}")
            current_y -= line_height
            p.drawString(100, current_y, "Data: ____/____/________")
            current_y -= 2 * line_height

            p.drawString(100, current_y, "Escola:")
            current_y -= line_height
            p.drawString(100, current_y, "Assinatura: ________________________________")
            current_y -= line_height
            p.drawString(100, current_y, "Nome do Representante: Calabreso")
            current_y -= line_height
            p.drawString(100, current_y, "Cargo: Coordenador de Turno")
            current_y -= line_height
            p.drawString(100, current_y, "Data: ____/____/________")
            current_y -= 2 * line_height

            # Witnesses
            p.drawString(100, current_y, "Testemunhas:")
            current_y -= line_height
            p.drawString(100, current_y, "Nome: ______________________________________")
            current_y -= line_height
            p.drawString(100, current_y, "Assinatura: ________________________________")
            current_y -= line_height
            p.drawString(100, current_y, "Nome: ______________________________________")
            current_y -= line_height
            p.drawString(100, current_y, "Assinatura: ________________________________")
            current_y -= 2 * line_height

            p.showPage()

        p.save()
        return response

    def download_signed_contract(self, obj):
        if obj.signed_contract:
            return format_html('<a href="{}" download>Baixar Contrato Assinado</a>', obj.signed_contract.url)
        return "Contrato não enviado"

    download_signed_contract.short_description = "Contrato Assinado"

    generate_pdf.short_description = "Gerar PDF dos Contratos"

class NotasAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'materia', 'nota_presenca', 'nota_atividade', 'nota_avaliativa', 'nota_final')
    search_fields = ('aluno__full_name', 'materia__name', 'turma__turma')
    list_filter = ('turma', 'materia')  # Filter by Turma and Materia
    readonly_fields = ('nota_final',)

    def get_queryset(self, request):
        # Filter queryset to show only relevant data
        qs = super().get_queryset(request)
        turma_id = request.GET.get('turma__id__exact')
        aluno_id = request.GET.get('aluno__id__exact')
        if turma_id:
            qs = qs.filter(turma_id=turma_id)
        if aluno_id:
            qs = qs.filter(aluno_id=aluno_id)
        return qs

    def changelist_view(self, request, extra_context=None):
        # Add hierarchical filtering to the admin interface
        turma_id = request.GET.get('turma__id__exact')
        aluno_id = request.GET.get('aluno__id__exact')
        extra_context = extra_context or {}
        if turma_id:
            extra_context['title'] = f"Notas - Turma {Turma.objects.get(id=turma_id)}"
        if aluno_id:
            extra_context['title'] = f"Notas - Aluno {Aluno.objects.get(id=aluno_id)}"
        return super().changelist_view(request, extra_context=extra_context)

class DesempenhoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'turma', 'materia', 'media_final')
    list_filter = ('turma', 'materia')
    search_fields = ('aluno__full_name', 'materia__name')

class PresencaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'data', 'status', 'observacao')
    list_filter = ('data', 'status')
    search_fields = ('aluno__full_name',)

class AgendaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'data_evento', 'lembrete')
    list_filter = ('data_evento', 'lembrete')
    search_fields = ('usuario__username', 'titulo')

class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'status', 'usuario_em_uso')
    list_filter = ('status',)
    search_fields = ('titulo', 'autor')

admin.site.register(Materia)
admin.site.register(Responsavel, ResponsaveisAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Nota, NotasAdmin)
admin.site.register(DesempenhoAcademico, DesempenhoAcademicoAdmin)
admin.site.register(Presenca, PresencaAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Livro, LivroAdmin)
