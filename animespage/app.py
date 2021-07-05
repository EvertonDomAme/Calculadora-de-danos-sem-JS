from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

user = 'ikdmsigy'
password = 'GmHfxkFvc8MruFuY6GhZe_U_hWWqJXuR'
host = 'tuffi.db.elephantsql.com'
database = 'ikdmsigy'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "chave secreta Dudom"

db = SQLAlchemy(app)

class Animes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable = False)
    imagem_url = db.Column(db.String(255), nullable = False)
    genero = db.Column(db.String(255), nullable = False)
    """ sinopse = db.column(db.String(2550), nullable = False) """

    def __init__(self, nome, imagem_url, genero, sinopse):#adicionar sinopse
        self.nome = nome
        self.imagem_url = imagem_url
        self.genero = genero
        self.sinopse = sinopse#adicionar sinopse

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, novo_nome, nova_imagem_url, novo_genero, nova_sinopse):#adicionar sinopse
        self.nome = novo_nome
        self.imagem_url = nova_imagem_url
        self.genero = novo_genero
        self.sinopse = nova_sinopse #adicionar sinopse

        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    @staticmethod
    def read_all():
        return Animes.query.order_by(Animes.nome.asc()).all()
    
    @staticmethod
    def read_single(id_registro):
	    return Animes.query.get(id_registro)

    @staticmethod
    def conta():
        return Animes.query.count()


@app.route("/")
def index():
    total = Animes.conta()
    return render_template("index.html", total=total)

@app.route("/read")
def read_all():
    registros = Animes.read_all()
    return render_template("read.html", registros = registros)

@app.route("/read/<id_registro>")
def read_id(id_registro):
	registro = Animes.read_single(id_registro)
	return render_template("read_single.html", registro=registro)

@app.route("/create", methods=('GET', 'POST'))
def create():
	novo_id = None

	if request.method == 'POST':
		form = request.form
		
		registro = Animes(form['nome'], form['imagem_url'], form['genero'], form['sinopse'])
		registro.save()

		novo_id = registro.id


	return render_template("create.html", novo_id = novo_id)

@app.route('/update/<id_registro>', methods=('GET', 'POST'))
def update(id_registro):
    sucesso = False

    registro = Animes.read_single(id_registro)

    if request.method == 'POST':
        form = request.form 
        
        #novo_registro = Animes(form['nome'], form['imagem_url'],form['genero'], form['sinopse'])#adicionar sinopse
        #registro.update(novo_registro)

        registro.update(form['nome'], form['imagem_url'],form['genero'], form['sinopse']) 

        sucesso = True
    
    return render_template('update.html', registro=registro, sucesso=sucesso)


@app.route('/delete/<id_registro>')
def delete(id_registro):
    registro = Animes.read_single(id_registro)
    return render_template("delete.html", registro=registro)

@app.route('/delete/<id_registro>/confirmed')
def delete_confirmed(id_registro):
    sucesso = False 

    registro = Animes.read_single(id_registro)

    if registro:
        registro.delete()
        sucesso = True 

    return render_template("delete.html", registro=registro, sucesso=sucesso)

if (__name__ == "__main__"):
    app.run(debug=True)
