# Comandos Docker, PostgreSQL e Django-Tenants

## Docker

### Listar containers
- Containers em execução: `docker ps`
- Todos os containers (incluindo parados): `docker ps -a`
- Formatar saída customizada: `docker ps -a --format "table {{.ID}}\t{{.Image}}\t{{.Names}}"`
- Filtrar por nome: `docker ps -a --filter "name=postgres"`
- Filtrar por status: `docker ps -a --filter "status=exited"`

### Gerenciar containers
- Iniciar container existente: `docker start plataforma_user`
- Iniciar e anexar output: `docker start -ai plataforma_user`
- Ver logs em tempo real: `docker logs -f plataforma_user`
- Inspecionar container (volumes/portas/config): `docker inspect plataforma_user`
- Inspecionar mounts específicos: `docker inspect plataforma_user | grep -A3 -E '"Mounts"|"/var/lib/postgresql/data"'`
- Parar container: `docker stop plataforma_user`
- Remover container (preserva volume nomeado): `docker rm plataforma_user`

### Criar e rodar PostgreSQL
- Rodar Postgres com porta customizada e volume: 
  ```bash
  docker run -d --name plataforma_user \
    -e POSTGRES_PASSWORD=senha \
    -p 5433:5432 \
    -v pgdata:/var/lib/postgresql/data \
    postgres:16
  ```
- Com bind mount (pasta no host):
  ```bash
  docker run -d --name plataforma_user \
    -e POSTGRES_PASSWORD=senha \
    -p 5433:5432 \
    -v /caminho/no/host:/var/lib/postgresql/data \
    postgres:16
  ```

## Diagnóstico de Portas (Host Ubuntu)

### Verificar porta em uso
- Via `ss`: `sudo ss -ltnp | grep 5432`
- Via `lsof`: `sudo lsof -i :5432`
- Ver todos os listeners: `sudo ss -ltnp` ou `sudo lsof -i`

## PostgreSQL - Serviço Systemd

### Gerenciar serviço (Ubuntu/Debian)
- Parar o serviço: `sudo systemctl stop postgresql`
- Ver status: `systemctl status postgresql`
- Reiniciar: `sudo systemctl restart postgresql`
- Habilitar no boot: `sudo systemctl enable postgresql`
- Desabilitar no boot: `sudo systemctl disable postgresql`

### Verificar clusters (Debian/Ubuntu com múltiplos clusters)
- Listar clusters: `pg_lsclusters`
- Parar cluster específico: `sudo systemctl stop postgresql@16-main` ou `sudo pg_ctlcluster 16 main -m fast stop`
- Ver portas por cluster: `grep '^port' /etc/postgresql/*/*/postgresql.conf`

## PostgreSQL - Backup e Restauração

### Dentro de um container
- Executar comando no container: `docker exec -i <container> <comando>`

### Gerar backups
- Dump SQL simples:
  ```bash
  docker exec -i plataforma_user pg_dump -U <usuario> -h localhost -d postgres_user > dump.sql
  ```
- Dump formato custom (-Fc, mais eficiente para grandes bases):
  ```bash
  docker exec -i plataforma_user pg_dump -U <usuario> -h localhost -d postgres_user -Fc > dump.dump
  ```
- Dump format diretório (paralelizável):
  ```bash
  docker exec -i plataforma_user pg_dump -Fd -j 4 -U <usuario> -d postgres_user -f backup_dir
  ```
- Exportar apenas roles (usuários globais):
  ```bash
  docker exec -i plataforma_user pg_dumpall -U <usuario> --roles-only > roles.sql
  ```

### Preparar banco destino
- Criar banco (CLI): `createdb -U postgres postres_user`
- Criar banco (SQL): `psql -U postgres -c "CREATE DATABASE postres_user;"`
- Criar com proprietário específico:
  ```bash
  createdb -U postgres -O dono_desejado postres_user
  ```

### Restaurar backups
- Restaurar dump SQL:
  ```bash
  psql -U postgres -d postres_user -f dump.sql
  ```
- Restaurar dump custom:
  ```bash
  pg_restore -U postgres -d postres_user dump.dump
  ```
- Restaurar sem recriar donos/privilégios (útil para migrar entre usuários):
  ```bash
  pg_restore -U postgres --no-owner --no-privileges -d postres_user dump.dump
  ```
- Restaurar e reatribuir dono:
  ```bash
  pg_restore -U postgres --no-owner --role novo_dono -d postres_user dump.dump
  ```
- Restaurar roles antes de restaurar dados (se necessário):
  ```bash
  psql -U postgres -f roles.sql
  psql -U postgres -d postres_user -f dump.sql
  ```

### Dump paralelo (diretório)
- Gerar dump: `pg_dump -Fd -j 4 -U postgres -d postgres_user -f backup_dir`
- Restaurar: `pg_restore -Fd -j 4 -U postgres -d postres_user backup_dir`

## Django - Configuração Básica

### Virtual environment
- Criar venv: `python -m venv venv`
- Ativar venv (Linux/Mac): `source venv/bin/activate`
- Ativar venv (Windows): `venv\Scripts\activate`
- Instalar dependências: `pip install -r requirements.txt`

### Migrations padrão
- Criar migrações: `python manage.py makemigrations`
- Aplicar migrações: `python manage.py migrate`
- Ver status de migrações: `python manage.py showmigrations`
- Reverter última migração: `python manage.py migrate <app> <numero_migração_anterior>`

## Django-Tenants - Múltiplos Schemas

### Configuração do modelo
- Adicionar EmbedVideoField:
  ```python
  from embed_video.fields import EmbedVideoField
  
  class Post(models.Model):
      # ... outros campos ...
      video = EmbedVideoField(blank=True, help_text="URL do vídeo (YouTube/Vimeo)")
  ```

- Ou usar URLField simples:
  ```python
  class Post(models.Model):
      # ... outros campos ...
      video_url = models.URLField(blank=True, help_text="URL do YouTube")
  ```

### Instalar django-embed-video (opcional)
```bash
pip install django-embed-video
```

Adicionar em `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    'embed_video',
]
```

### Migrações em multi-tenant
- Gerar migrações: `python manage.py makemigrations`
- Aplicar para todos os schemas (público + tenants):
  ```bash
  python manage.py migrate_schemas
  ```
- Aplicar em um tenant específico (teste):
  ```bash
  python manage.py migrate_schemas --schema=schema_name
  ```
- Ver migrações pendentes:
  ```bash
  python manage.py showmigrations
  ```

### Criar/gerenciar tenants
- Criar tenant via manage.py:
  ```bash
  python manage.py shell
  from django_tenants.models import Client, Domain
  tenant = Client.objects.create(name="Meu Tenant", schema_name="tenant_name")
  Domain.objects.create(domain="tenant.example.com", tenant=tenant, is_primary=True)
  ```

### Arquivos de configuração importantes
- `settings.py`: SHARED_APPS (público), TENANT_APPS (tenants), DATABASES
- `pg_hba.conf`: autenticação PostgreSQL
- `postgresql.conf`: configurações do servidor (porta, conexões, etc.)

## Verificar Configurações

### PostgreSQL no host
- Ver porta em uso: `SHOW port;` (dentro de psql)
- Ver usuário padrão: `SELECT current_user;` (dentro de psql)
- Listar bancos: `\l` (dentro de psql)
- Conectar a um banco: `\c nome_banco` (dentro de psql)
- Listar tabelas: `\dt` (dentro de psql)

### Django-tenants
- Ver apps em SHARED_APPS e TENANT_APPS: `python manage.py shell` e `from django.conf import settings; print(settings.SHARED_APPS); print(settings.TENANT_APPS)`

## Troubleshooting Comum

### Porta 5432 já em uso
1. Identificar quem usa: `sudo lsof -i :5432`
2. Parar serviço: `sudo systemctl stop postgresql`
3. Parar container antigo: `docker stop <container_id>`
4. Liberar porta: `sudo kill -9 <pid>` (último recurso)
5. Usar porta alternativa: `docker run -p 5433:5432 ...`

### Erro "address already in use"
- Verificar se docker-proxy mantém bind: `sudo ss -ltnp | grep 5432`
- Remover container e recriar com nova porta ou após liberar a 5432

### Tenant não herda migrações
- Garantir que app está em TENANT_APPS (não em SHARED_APPS)
- Rodar: `python manage.py migrate_schemas --schema=schema_name`
- Criar novo tenant: garante que as migrações mais recentes são aplicadas automaticamente

### Conectar via psql remoto
- Local: `psql -U postgres -h localhost -p 5432 -d nome_banco`
- Remoto: `psql -U postgres -h IP_OU_HOST -p 5432 -d nome_banco`
- Via container: `docker exec -it plataforma_user psql -U postgres -d nome_banco`

---

**Data de criação:** Novembro 2025  
**Contexto:** Migração de PostgreSQL (Docker → Ubuntu local), campo de vídeo YouTube em modelo Django multi-tenant

python manage.py create_tenant_superuser --username=miguelnatus --schema=annasebba
