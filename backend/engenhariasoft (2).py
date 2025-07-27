
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Text,
    Boolean,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///sistema_adocao.db", echo=False)
Session = sessionmaker(bind=engine)


class Tutor(Base):
    __tablename__ = "tutores"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(11), unique=True)
    dataNascimento = Column(DateTime)
    email = Column(String, unique=True)
    endereco = Column(String)
    senha = Column(String)  


    adocoes = relationship("Adocao", back_populates="tutor")

    def __repr__(self):
        return f"<Tutor {self.nome}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "dataNascimento": (
                self.dataNascimento.strftime("%Y-%m-%d")
                if self.dataNascimento
                else None
            ),
            "email": self.email,
            "endereco": self.endereco,
        }


class Administrador(Base):
    __tablename__ = "administradores"
    id = Column(Integer, primary_key=True)
    senha = Column(String)

    def __repr__(self):
        return f"<Admin {self.id}>"


class Animal(Base):
    __tablename__ = "animais"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    especie = Column(String)
    idade = Column(Integer)
    raca = Column(String)
    temperamento = Column(String)
    historicoMedico = Column(Text)
    adotado = Column(Boolean, default=False)

    adocao = relationship("Adocao", back_populates="animal", uselist=False)

    def __repr__(self):
        return f"<Animal {self.nome}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especie": self.especie,
            "idade": self.idade,
            "raca": self.raca,
            "temperamento": self.temperamento,
            "historicoMedico": self.historicoMedico,
            "adotado": self.adotado,
        }


class Adocao(Base):
    __tablename__ = "adocoes"
    id = Column(Integer, primary_key=True)
    idTutor = Column(Integer, ForeignKey("tutores.id"))
    idAnimal = Column(Integer, ForeignKey("animais.id"))
    dataSolicitacao = Column(DateTime)
    status = Column(String)

    tutor = relationship("Tutor", back_populates="adocoes")
    animal = relationship("Animal", back_populates="adocao")

    def __repr__(self):
        return f"<Adocao {self.id} - Status: {self.status}>"

    def to_dict(self):
        return {
            "id": self.id,
            "idTutor": self.idTutor,
            "idAnimal": self.idAnimal,
            "dataSolicitacao": (
                self.dataSolicitacao.strftime("%Y-%m-%d %H:%M:%S")
                if self.dataSolicitacao
                else None
            ),
            "status": self.status,
            "tutor_nome": self.tutor.nome if self.tutor else None,
            "animal_nome": self.animal.nome if self.animal else None,
        }


def criar_banco():
    Base.metadata.create_all(engine)
    print("Banco de dados criado (ou já existente).")


app = Flask(__name__)
CORS(app)

criar_banco()


@app.route("/tutores", methods=["POST"])
def cadastrar_tutor():
    session = Session()
    try:
        data = request.json

        if not data or not all(
            k in data for k in ["nome", "cpf", "dataNascimento", "email", "endereco",  "senha"]
        ):
            return jsonify({"erro": "Dados incompletos para o tutor."}), 400

        dataNascimento = datetime.strptime(data["dataNascimento"], "%Y-%m-%d")

        tutor = Tutor(
        nome=data["nome"],
        cpf=data["cpf"],
        dataNascimento=dataNascimento,
        email=data["email"],
        endereco=data["endereco"],
        senha=data["senha"],
        )

        session.add(tutor)
        session.commit()
        return (
            jsonify(
                {"mensagem": "Tutor cadastrado com sucesso.", "tutor": tutor.to_dict()}
            ),
            201,
        )
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 400
    finally:
        session.close()


@app.route("/animais", methods=["GET"])
def listar_animais():
    session = Session()
    try:
        animais = session.query(Animal).all()
        resultado = [animal.to_dict() for animal in animais]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        session.close()


@app.route("/solicitar_adocao", methods=["POST"])
def solicitar_adocao():
    session = Session()
    try:
        data = request.json
        tutor_id = data.get("tutor_id")
        animal_id = data.get("animal_id")

        tutor = session.query(Tutor).get(tutor_id)
        animal = session.query(Animal).get(animal_id)

        if not tutor or not animal:
            return jsonify({"erro": "Tutor ou Animal não encontrados."}), 404
        if animal.adotado:
            return jsonify({"erro": "Animal já foi adotado."}), 409

        adocao = Adocao(
            idTutor=tutor_id,
            idAnimal=animal_id,
            dataSolicitacao=datetime.now(),
            status="pendente",
        )
        session.add(adocao)
        session.commit()
        return (
            jsonify(
                {
                    "mensagem": "Solicitação de adoção registrada.",
                    "adocao": adocao.to_dict(),
                }
            ),
            201,
        )
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 400
    finally:
        session.close()


@app.route("/confirmar_adocao", methods=["POST"])
def confirmar_adocao():
    session = Session()
    try:
        data = request.json
        adocao_id = data.get("adocao_id")
        admin_id = data.get("admin_id")

        if not session.query(Administrador).get(admin_id):
            return jsonify({"erro": "Administrador não autorizado."}), 403

        adocao = session.query(Adocao).get(adocao_id)

        if not adocao:
            return jsonify({"erro": "Adoção não encontrada."}), 404
        if adocao.status != "pendente":
            return (
                jsonify(
                    {
                        "erro": f"Adoção não está pendente (status atual: {adocao.status})."
                    }
                ),
                409,
            )

        adocao.status = "confirmado"
        adocao.animal.adotado = True
        session.commit()
        return (
            jsonify({"mensagem": "Adoção confirmada.", "adocao": adocao.to_dict()}),
            200,
        )
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 400
    finally:
        session.close()


@app.route("/admin/animais", methods=["POST"])
def admin_cadastrar_animal():
    session = Session()
    try:
        data = request.json
        if not session.query(Administrador).get(data.get("admin_id")):
            return (
                jsonify({"erro": "Apenas administradores podem cadastrar animais."}),
                403,
            )

        animal = Animal(
            nome=data["nome"],
            especie=data["especie"],
            idade=data["idade"],
            raca=data["raca"],
            temperamento=data["temperamento"],
            historicoMedico=data["historicoMedico"],
        )
        session.add(animal)
        session.commit()
        return (
            jsonify({"mensagem": "Animal cadastrado.", "animal": animal.to_dict()}),
            201,
        )
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 400
    finally:
        session.close()


@app.route("/")
def home():
    return "API de Adoção de Animais funcionando corretamente!"

from flask import render_template

@app.route("/cadastro")
def cadastro():
    return render_template("Cadastro.html")

@app.route("/controleadocao")
def controleadocao():
    return render_template("ControleAdocao.html")

@app.route("/criarsenha")
def criarsenha():
    return render_template("CriarSenha.html")

@app.route("/gerenciaanimais")
def gerenciaanimais():
    return render_template("GerenciaAnimais.html")

@app.route("/gerenciatutor")
def gerenciatutor():
    return render_template("GerenciaTutor.html")

# ... (código anterior) ...

# --- CORREÇÃO AQUI: Funções de login separadas por método HTTP ---
@app.route("/login", methods=["GET"])
def pagina_login():  # AQUI! Renomeie a função para algo como 'pagina_login'
    """Renderiza a página de login."""
    return render_template("Login.html")

@app.route("/login", methods=["POST"])
def processar_login():  # E AQUI! Renomeie a função para algo como 'processar_login'
    """Processa as credenciais de login."""
    session = Session()
    try:
        data = request.json
        usuario = data.get("usuario")
        senha = data.get("senha")

        if not usuario or not senha:
            return jsonify({"erro": "Usuário e senha são obrigatórios."}), 400

        # Verifica se é admin (login por senha de admin)
        admin = session.query(Administrador).filter_by(senha=senha).first()
        if admin:
            return jsonify({"tipo": "admin", "mensagem": "Login de administrador validado."}), 200

        # Verifica se é tutor (por email + senha)
        tutor = session.query(Tutor).filter_by(email=usuario, senha=senha).first()
        if tutor:
            return jsonify({"tipo": "tutor", "mensagem": "Login de tutor validado.", "tutor_id": tutor.id}), 200

        return jsonify({"erro": "Usuário ou senha inválidos."}), 401

    except Exception as e:
        return jsonify({"erro": str(e)}), 400
    finally:
        session.close()


@app.route("/telacontrole")
def telacontrole():
    return render_template("TelaControle.html")

@app.route("/telamostraanimais")
def telamostraanimais():
    return render_template("TelaMostraAnimais.html")

@app.route("/telaprincipal")
def telaprincipal():
    return render_template("TelaPrincipal.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/salvar_senha", methods=["POST"])
def salvar_senha():
    session = Session()
    try:
        data = request.json
        senha = data.get("senha")

        # Aqui vamos assumir que o último tutor cadastrado é quem está criando a senha
        # Em produção, isso seria feito com autenticação/session
        tutor = session.query(Tutor).order_by(Tutor.id.desc()).first()
        if not tutor:
            return jsonify({"erro": "Nenhum tutor encontrado."}), 404

        # Cria um Administrador com a senha (ou em outro lugar se preferir)
        novo_admin = Administrador(senha=senha)
        session.add(novo_admin)
        session.commit()

        return jsonify({"mensagem": "Senha salva com sucesso."}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"erro": str(e)}), 400
    finally:
        session.close()

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not usuario or not senha:
        return jsonify({"erro": "Preencha todos os campos"}), 400

    # Aqui você pode adaptar para verificar no banco de dados ou lista
    if usuario == "teste@email.com" and senha == "senha123":
        return jsonify({"tipo": "tutor"}), 200

    # Para teste com admin, por exemplo:
    # if usuario == "admin@email.com" and senha == "admin123":
    #     return jsonify({"tipo": "admin"}), 200

    return jsonify({"erro": "Usuário ou senha inválidos"}), 401


if __name__ == "__main__":
    with Session() as session:
        if not session.query(Administrador).first():
            print("Criando admin padrão...")
            admin = Administrador(senha="admin")
            session.add(admin)
            session.commit()
        if not session.query(Tutor).first():
            print("Criando tutor padrão...")
            tutor = Tutor(
                nome="João",
                cpf="00000000000",
                dataNascimento=datetime(1990, 1, 1),
                email="joao@example.com",
                endereco="Rua Teste, 123",
                senha="joao@example.com" 
            )
            session.add(tutor)
            session.commit()
        if not session.query(Animal).first():
            print("Criando animal padrão...")
            animal = Animal(
                nome="Totó",
                especie="Cachorro",
                idade=2,
                raca="Vira-lata",
                temperamento="Calmo",
                historicoMedico="Nenhum",
            )
            session.add(animal)
            session.commit()

    app.run(debug=True)

