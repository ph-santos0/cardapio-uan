from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

# SemanaCardapio foi removido da importação
from cardapio.models import Cardapio, ItemCardapio, DiaCardapio, Refeicao, CategoriaItem

class Command(BaseCommand):
    help = 'Cria o grupo Nutricionistas, atribui permissões e cria um usuário de teste.'

    def handle(self, *args, **kwargs):
        # 1. Cria o grupo ou pega se já existir
        grupo, created = Group.objects.get_or_create(name='Nutricionistas')
        
        # 2. Lista os models permitidos (SemanaCardapio removido)
        models_permitidos = [
            Cardapio, ItemCardapio, DiaCardapio, Refeicao, CategoriaItem
        ]
        
        # 3. Adiciona as permissões de Adicionar/Mudar/Deletar/Ver ao Grupo
        for model in models_permitidos:
            content_type = ContentType.objects.get_for_model(model)
            permissoes = Permission.objects.filter(content_type=content_type)
            for perm in permissoes:
                grupo.permissions.add(perm)

        # 4. Cria o usuário nutricionista de teste (com is_staff=True para acessar o /admin)
        if not User.objects.filter(username='nutri').exists():
            user = User.objects.create_user(username='nutri', password='nutri123', is_staff=True)
            user.groups.add(grupo)
            self.stdout.write(self.style.SUCCESS('✅ Usuário "nutri" (senha: nutri123) criado e adicionado ao grupo!'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Usuário "nutri" já existe.'))
                
        self.stdout.write(self.style.SUCCESS('✅ Grupo "Nutricionistas" configurado com sucesso!'))