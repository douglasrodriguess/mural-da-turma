"""
Insere usuários e comentários de exemplo (dados fictícios!):

    python seed.py
"""
from app import Comentario, Usuario, app, db

USUARIOS = [
    ("Professor", "professor@teste.com"),
    ("Ana", "ana@teste.com"),
    ("Pedro", "pedro@teste.com"),
]

COMENTARIOS = [
    ("ana@teste.com", "Gostei muito da aula de Flask!"),
    ("pedro@teste.com", "Minha primeira página com banco na nuvem 😎"),
    ("professor@teste.com", "Bem-vindos ao mural da turma! Deixem seus comentários."),
]

with app.app_context():
    db.create_all()

    for nome, email in USUARIOS:
        if not Usuario.query.filter_by(email=email).first():
            u = Usuario(nome=nome, email=email)
            u.definir_senha("123456")
            db.session.add(u)
    db.session.commit()

    if Comentario.query.count() == 0:
        for email, texto in COMENTARIOS:
            autor = Usuario.query.filter_by(email=email).first()
            db.session.add(Comentario(texto=texto, autor=autor))
        db.session.commit()
        print(f"{len(COMENTARIOS)} comentários inseridos!")
    else:
        print("O mural já tem comentários. Nada foi inserido.")

    print("Logins de teste (senha 123456): " + ", ".join(e for _, e in USUARIOS))
