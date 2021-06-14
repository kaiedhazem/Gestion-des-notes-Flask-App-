from flask import  render_template ,url_for,flash,redirect,request
from mainapp.forms import RegistrationForm, LoginForm ,UpdateUserForm,MatiereForm,ReaserchForm
from mainapp import app, db, bcrypt,fa
from mainapp.models import User,Matiere,Note
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('accueil'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout',methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/accueil',methods=['GET','POST']) 
@login_required
def accueil():
    nombreuser= User.query.filter(User.role == 'etudiant').count()
    return render_template('home.html',nbr=nombreuser)

@app.route('/home',methods=['GET','POST']) 
@login_required
def home():
    notesDS = Note.query.filter(Note.user_id == current_user.id,Note.nature=='ds').all()
    notesExamen = Note.query.filter(Note.user_id == current_user.id,Note.nature=='examen').all()
    if request.method == 'POST':
       matieres = Matiere.query.order_by(Matiere.module).filter(Matiere.niveau == current_user.niveau , Matiere.specialite == current_user.specialite ,Matiere.semestre == request.form['semestre']).all()
       return render_template('layout.html',matieres=matieres,notesexamen=notesExamen,notesds=notesDS)
    else:  
       return render_template('layout.html')
 
@app.route('/notes',methods=['GET','POST'])  
@login_required
def notes():
    form = ReaserchForm()
    if form.validate_on_submit():
        users = User.query.filter(User.specialite==form.specialite.data,User.niveau==form.niveau.data)
        matieres= Matiere.query.filter(Matiere.specialite==form.specialite.data,Matiere.niveau==form.niveau.data,
        Matiere.semestre==form.semestre.data)
        return render_template('notes.html',form=form,users=users,matieres=matieres,sem=form.semestre.data)
    elif request.method == 'GET':
        return render_template('notes.html',form=form)

@app.route('/ajouternote',methods=['GET','POST'])
@login_required
def ajouternote():
    if request.method == 'POST':
       matiere= Matiere.query.filter(Matiere.id == request.form['mat']).first()
       user= User.query.filter(User.id == request.form['userid']).first()
       noteds = Note(note=request.form['ds'],nature='ds',matiere_id=request.form['mat'],user_id=
       request.form['userid'])
       noteexamen = Note(note=request.form['examen'],nature='examen',matiere_id=request.form['mat'],user_id=
       request.form['userid'])
       db.session.add(noteds)
       db.session.add(noteexamen)
       user.notes.append(noteds)
       user.notes.append(noteexamen)
       matiere.notes.append(noteds)
       matiere.notes.append(noteexamen)
       db.session.commit()
       flash('The note has been created!', 'success')
       return redirect(url_for('notes'))

@app.route('/notes/<int:user_id>/<int:sem>/consulternote',methods=['GET','POST'])
@login_required
def consulternote(user_id,sem):
       user = User.query.filter(User.id == user_id).first()
    
       notesDS = Note.query.filter(Note.user_id == user_id,Note.nature=='ds').all()
       notesExamen = Note.query.filter(Note.user_id == user_id,Note.nature=='examen').all()
       matieres = Matiere.query.order_by(Matiere.module).filter(Matiere.niveau == user.niveau , Matiere.specialite == user.specialite ,Matiere.semestre == sem ).all()
       return render_template('affichagenote.html',matieres=matieres,notesexamen=notesExamen,notesds=notesDS,user=user,sem=sem)

    

@app.route('/compte', methods=['GET', 'POST'])  
@login_required
def compte():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(nom=form.nom.data,prenom=form.prenom.data,email=form.email.data, password=hashed_password,
        niveau=form.niveau.data,specialite=form.specialite.data,role='etudiant')
        db.session.add(user)
        db.session.commit()
        flash('The account has been created!', 'success')
        return redirect(url_for('compte'))
    elif request.method == 'GET':
        users = User.query.order_by(User.niveau.desc(),User.specialite).filter(User.role != 'admin').all()
    return render_template('compte.html',
                           form=form, users=users)

@app.route("/compte/<int:user_id>/delete", methods=['GET','POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    notes = Note.query.filter(Note.user_id == user_id).all()
    for note in notes:
        db.session.delete(note)
    db.session.delete(user)
    db.session.commit()
    flash('Your user has been deleted!', 'success')
    return redirect(url_for('compte'))

@app.route("/compte/<int:user_id>/update", methods=['GET','POST'])
@login_required
def update_user(user_id):
    print(user_id)
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['mdp']).decode('utf-8')
        user.nom= request.form['nom']
        user.prenom= request.form['prenom']
        user.email= request.form['email']
        user.password=hashed_password
        user.niveau= request.form['niveau']
        user.specialite= request.form['specialite']
        db.session.commit()
        flash('Your account has been Updated!', 'success')
        return redirect(url_for('compte'))
    elif request.method == 'GET':
        return render_template('updateuser.html',user_id=user_id,user=user)


@app.route('/matiere')  
@login_required
def matiere():
    return render_template('matiere.html')

@app.route('/matieresem2',methods=['GET','POST'])  
@login_required
def matieresem2():
    form = MatiereForm()
    if form.validate_on_submit():
        mat=Matiere(nom=form.nom.data,semestre=2,niveau=form.niveau.data,specialite=form.specialite.data,
        module=form.module.data,coefficient=form.coefficient.data)
        db.session.add(mat)
        db.session.commit()
        flash('La matiére a été crée avec succés', 'success')
        return redirect(url_for('matieresem2'))
    elif request.method == 'GET':
        matieres = Matiere.query.order_by(Matiere.niveau.desc(),Matiere.specialite).filter(Matiere.semestre == 2).all()
        return render_template('matieresem2.html',form=form,matieres=matieres)


@app.route('/matieresem1',methods=['GET','POST'])  
@login_required
def matieresem1():
    form = MatiereForm()
    if form.validate_on_submit():
        mat=Matiere(nom=form.nom.data,semestre=1,niveau=form.niveau.data,specialite=form.specialite.data,
        module=form.module.data,coefficient=form.coefficient.data)
        db.session.add(mat)
        db.session.commit()
        flash('La matiére a été crée avec succés', 'success')
        return redirect(url_for('matieresem1'))
    elif request.method == 'GET':
         matieres = Matiere.query.order_by(Matiere.niveau.desc(),Matiere.specialite).filter(Matiere.semestre == 1).all()
    return render_template('matieresem1.html',
                           form=form,matieres=matieres)

@app.route("/matieresem1/<int:matiere_id>/delete", methods=['GET','POST'])
@login_required
def delete_matS1(matiere_id):
    mat = Matiere.query.get_or_404(matiere_id)
    notes = Note.query.filter(Note.matiere_id == matiere_id).all()
    for note in notes:
        db.session.delete(note)
    db.session.delete(mat)
    db.session.commit()
    flash('Your Subject has been deleted!', 'success')
    return redirect(url_for('matieresem1'))

@app.route("/matieresem2/<int:matiere_id>/delete", methods=['GET','POST'])
@login_required
def delete_matS2(matiere_id):
    mat = Matiere.query.get_or_404(matiere_id)
    notes = Note.query.filter(Note.matiere_id == matiere_id).all()
    for note in notes:
        db.session.delete(note)
    db.session.delete(mat)
    db.session.commit()
    flash('Your Subject has been deleted!', 'success')
    return redirect(url_for('matieresem2'))

@app.route("/matieresem1/<int:matiere_id>/update", methods=['GET','POST'])
@login_required
def update_mats1(matiere_id):
    matiere = Matiere.query.get_or_404(matiere_id)
    if request.method == 'POST':
        matiere.nom= request.form['nom']
        matiere.semestre= 1
        matiere.niveau= request.form['niveau']
        matiere.specialite= request.form['specialite']
        matiere.module= request.form['module']
        matiere.coefficient = request.form['coeff']
        db.session.commit()
        flash('Your Subject has been Updated!', 'success')
        return redirect(url_for('matieresem1'))
    elif request.method == 'GET':
        return render_template('updatematieresem1.html',matiere_id=matiere.id,matiere=matiere)

@app.route("/matieresem2/<int:matiere_id>/update", methods=['GET','POST'])
@login_required
def update_mats2(matiere_id):
    matiere = Matiere.query.get_or_404(matiere_id)
    if request.method == 'POST':
        matiere.nom= request.form['nom']
        matiere.semestre= 2
        matiere.niveau= request.form['niveau']
        matiere.specialite= request.form['specialite']
        matiere.module= request.form['module']
        matiere.coefficient = request.form['coeff']
        db.session.commit()
        flash('Your Subject has been Updated!', 'success')
        return redirect(url_for('matieresem2'))
    elif request.method == 'GET':
        return render_template('updatematieresem2.html',matiere_id=matiere.id,matiere=matiere)