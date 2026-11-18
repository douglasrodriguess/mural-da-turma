# Mural da Turma: Flask + Postgres + Login

Um mural de comentários **compartilhado**: todos que apontam para o mesmo banco
(ex.: Neon) veem os comentários uns dos outros, em qualquer computador.

## Funcionalidades

1. Cadastro, login e logout (senha salva com hash)
2. Publicar comentário (o nome vem do usuário logado)
3. Lista de comentários com nome, mensagem e data
4. Excluir comentário (só o autor pode excluir o próprio)
5. Contador de comentários publicados

## Rodando

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # Windows: copy .env.example .env
# edite o .env: DATABASE_URL e SECRET_KEY

python seed.py                    # (opcional) usuários e comentários de exemplo
flask run                         # http://127.0.0.1:5000
```

Logins de teste (senha **123456**): professor@teste.com, ana@teste.com, pedro@teste.com

> No Neon, use a connection string **sem** `-pooler` no endereço.

## Backup e restauração

```bash
pg_dump "URL_DO_BANCO" --no-owner --no-privileges -f backup.sql
psql "URL_DO_OUTRO_BANCO" -f backup.sql
```
