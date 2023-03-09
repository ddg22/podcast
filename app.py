# Librerie: Flask, Flask-Session, flask-login
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_session import Session
from datetime import *
from operator import itemgetter
from werkzeug.utils import secure_filename
# Libreria per criptare la password mediante funzione di hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import os

import users_dao
import podcast_dao
import episode_dao
from models import User


app = Flask(__name__)

app.config['SECRET_KEY'] = 'T3Uh+sgG4gJt6+^v'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)


# Gestisce la pagina non esistente
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=404), 404


# Gestisce la pagina per cui non si hanno i permessi di accesso
@app.errorhandler(401)
def page_not_found(e):
    return render_template('error.html', error=401), 401


# Home del sito
@app.route('/')
def home():
    # Estraggo i podcast dal db
    podcasts = podcast_dao.get_podcasts_users()

    return render_template("home.html", podcasts=podcasts)


# Crea un nuovo podcast
@app.route('/newPodcast', methods=['POST'])
@login_required
def new_podcast():
    extensions = ['jpeg', 'png', 'jpg']
    podcast = request.form.to_dict()

    # Verifico di non avere problemi nel form
    if 'Img' not in request.files:
        flash('Errore nel caricamento dell\'immagine, riporva', 'danger')
        return redirect(url_for('home'))

    # Verifico che ci siano tutti i campi obbligatori
    if podcast['Title'] == '' or podcast['Description'] == '' or podcast['Category'] == '' or secure_filename(request.files['Img'].filename) == '':
        flash('Campi obbligatori mancanti', 'danger')
        return redirect(url_for('home'))

    # Verifico che i campi testuali siano conformi
    if len(podcast['Description']) < 30 or len(podcast['Description']) > 300 or len(podcast['Category']) < 4 or len(podcast['Category']) > 25 or len(podcast['Title']) < 5 or len(podcast['Title']) > 50:
        flash('Campi testuali con lunghezza non appropriata, riprova', 'danger')
        return redirect(url_for('home'))

    podcast_image = request.files['Img']
    filename = secure_filename(podcast_image.filename)
    filename = filename.rsplit('.', 1)

    # Verifico che l'immagine abbia la giusta estensione
    if filename[1].lower() not in extensions:
        flash('Formato immagine non supportato, riprova', 'danger')
        return redirect(url_for('home'))

    # Calcolo l'id del nuovo podcast prendendo quello più alto da db
    if podcast_dao.get_max_id()['Max']:
        podcast_id = (podcast_dao.get_max_id())['Max']+1
    else:
        podcast_id = 1

    img_name = f"{podcast_id}_{current_user.id}.{filename[1]}"
    img_name = secure_filename(img_name)
    podcast_image.save(f"static/{img_name}")

    podcast = {
        'PdId' : podcast_id,
        'Title' : podcast['Title'],
        'Img' : img_name,
        'Description' : podcast['Description'],
        'Category' : podcast['Category'].lower(),
        'UserId' : current_user.id,
    }
    #Inserisco il podcast nel db, verificando che non ci siano errori
    if podcast_dao.insert_podcast(podcast) == False:
        flash('Errore nella creazione del podcast, riprova', 'danger')

    return redirect(url_for('home'))


# Visualizza la pagina di ogni podcast
@app.route('/podcast<int:pdId>')
def podcast_page(pdId):
    # Prendo l'utente che ha creato il podcast
    podcast = podcast_dao.get_podcast_user(pdId)

    if not podcast:
        return render_template('error.html', error=404)

    # Prendo tutti gli episodi del podcast
    episodes = episode_dao.get_episodes_podcast(pdId)

    today = date.today()

    # Verifico se l'utente corrente segue o no il podcast
    follow = False
    if current_user.is_authenticated:
        # Prendo il follow dell'utente corrente rispetto al podcast corrente
        follow_db = users_dao.get_follow(current_user.id, pdId)
        if follow_db:
            follow = True
    
    return render_template('singlePodcast.html', podcast=podcast, episodes=episodes, follow=follow, today=today)


# Segue un podcast
@app.route('/podcast<int:pdId>/follow')
@login_required
def follow(pdId):
    if users_dao.insert_follow(current_user.id, pdId) == False:
        flash('Errore durante la procedura, riporva', 'danger')
    return redirect(url_for('podcast_page', pdId=pdId))


# Smette di seguire un podcast
@app.route('/podcast<int:pdId>/unfollow')
@login_required
def unfollow(pdId):
    # Elimino il follow dal db
    if users_dao.delete_follow(current_user.id, pdId) == False:
        flash("Errore durante la procedura, riprova", 'danger')
    return redirect(url_for('podcast_page', pdId=pdId))


# Modifica un podcast
@app.route('/podcast<int:pdId>/modifyPodcast', methods=['POST'])
@login_required
def modify_podcast(pdId):
    extensios = ['jpeg', 'png', 'jpg']
    podcast = request.form.to_dict()

    # Verifico che ci siano tutti i campi obbligatori
    if podcast['Title'] == '' or podcast['Description'] == '' or podcast['Category'] == '':
        flash('Campi obbligatori mancanti', 'danger')
        return redirect(url_for('podcast_page', pdId=pdId))

    # Verifico che i campi testuali siano conformi
    if len(podcast['Description']) < 30 or len(podcast['Description']) > 300 or len(podcast['Category']) < 4 or len(podcast['Category']) > 25 or len(podcast['Title']) < 5 or len(podcast['Title']) > 50:
        flash('Campi testuali con lunghezza non appropriata, riprova', 'danger')
        return redirect(url_for('podcast_page', pdId=pdId))

    # Immagine podcast
    if 'Img' in request.files:
        podcast_image = request.files['Img']
        old_img = podcast_dao.get_podcast_img(pdId)['Img']
        # Se ho il vecchio file lo mantengo
        if secure_filename(podcast_image.filename) == '':
            img_name = old_img
        # Se ho la nuova immagine la aggiorno
        else:
            if os.path.exists(f"static/{old_img}"):
                os.remove(f"static/{old_img}")

            filename = secure_filename(podcast_image.filename)
            filename = filename.rsplit('.', 1)

            if filename[1].lower() not in extensios:
                flash('Formato immagine non supportato, riprova', 'danger')
                return redirect(url_for('podcast_page', pdId=pdId))

            img_name = f"{pdId}_{current_user.id}.{filename[1]}"
            img_name = secure_filename(img_name)
            podcast_image.save(f"static/{img_name}")
    # Se ho problemi nel form ritorno errore
    else:
        flash('Errore nel caricamento dell\'immagine, riprova', 'danger')
        return redirect(url_for('podcast_page', pdId=pdId))

    podcast = {
        'PdId' : pdId,
        'Title' : podcast['Title'],
        'Img' : img_name,
        'Description' : podcast['Description'],
        'Category' : podcast['Category'].lower(),
    }
    
    if podcast_dao.modify_podcast(podcast) == True:
        flash('Podcast modificato con successo', 'success')
    else:
        flash('Errore nella modifica del podcast, riprova', 'danger')

    return redirect(url_for('podcast_page', pdId=pdId))


# Elimina un podcast
@app.route('/podcast<int:pdId>/deletePodcast')
@login_required
def delete_podcast(pdId):
    # Verifico che l'utente possa cancellare
    podcast = podcast_dao.get_podcast_user(pdId)
    if not current_user.is_authenticated or current_user.id != podcast['UserId']:
        return render_template('error.html', error=401)

    # Prendo il nome dell'immagine dal db
    img = podcast_dao.get_podcast_img(pdId)['Img']
    # Prendo tutti i nomi dei file degli episodi del podcast
    episodes = episode_dao.get_episodes_audio(pdId)

    for audio in episodes:
        if os.path.exists(f"static/{audio['Audio']}"):
            os.remove(f"static/{audio['Audio']}")

    if os.path.exists(f"static/{img}"):
        os.remove(f"static/{img}")

    if podcast_dao.delete_podcast(pdId) == True:
        flash('Podcast eliminato con successo', 'success')
    else:
        flash('Errore nell\'eliminazione del podcast', 'danger')

    return redirect(url_for('home')) 


# Crea un nuovo episodio
@app.route('/podcast<int:pdId>/newEpisode', methods=['POST'])
@login_required
def new_episode(pdId):
    extensions = ['mp3', 'wav', 'ogg']
    episode = request.form.to_dict()

    # Verifico di non avere problemi nel form
    if 'Audio' not in request.files:
        flash('Errore nel caricamento del file audio, riprova', 'danger')
        return redirect(url_for('podcast_page', pdId=pdId))

    # Verifico che tutti i campi obbligatori ci siano
    if episode['Title'] == '' or episode['Description'] == '' or episode['Date'] == '' or secure_filename(request.files['Audio'].filename) == '':
        flash('Campi obbligatori mancanti', 'danger')
        return redirect(url_for('podcast_page', pdId=pdId))

    # Verifico che i campi testuali siano conformi
    if len(episode['Description']) < 30 or len(episode['Description']) > 300 or len(episode['Title']) < 5 or len(episode['Title']) > 50 or datetime.strptime(episode['Date'], '%Y-%m-%d').date() > date.today():
        flash('Errore nella compilazione dei campi, riprova', 'danger')
        return redirect(url_for('home'))   

    episode_audio = request.files['Audio']
    filename = secure_filename(episode_audio.filename)
    filename = filename.rsplit('.', 1)

    # Verifico che il file audio inserito abbia la giusta estensione
    if filename[1].lower() not in extensions:
        flash('File audio non supportato, riprova', 'danger')
        return redirect(url_for('podcast_page', pdId=pdId))

    # Prendo l'id più alto tra gli episodi del db per nominare il file audio
    if episode_dao.get_max_id()['Max']:
        episode_id = (episode_dao.get_max_id())['Max']+1
    else:
        episode_id = 1

    audio_name = f"{pdId}_{episode_id}_{current_user.id}.{filename[1].lower()}"
    audio_name = secure_filename(audio_name)
    episode_audio.save(f"static/{audio_name}")
    
    episode = {
        'EpId' : episode_id,
        'Title' : episode['Title'],
        'PdId' : pdId,
        'Description' : episode['Description'],
        'Date' : episode['Date'],
        'Audio' : audio_name
    }
    # Inserisco l'episodio nel db, verificando che non ci siano errori
    if episode_dao.insert_episode(episode) == False:
        flash('Errore nella creazione dell\'episodio, riprova', 'danger')

    return redirect(url_for('podcast_page', pdId=pdId))


# Pagina di ogni singolo episodio
@app.route('/podcast<int:pdId>/<int:epId>')
def episode_page(pdId, epId):
    # Prendo il podcast relativo all'episodio
    podcast = podcast_dao.get_podcast_user(pdId)
    # Prendo dal db l'episodio
    episode = episode_dao.get_episode(epId)

    if not podcast or not episode:
        return render_template('error.html', error=404)

    # Prendo dal db tutti i commenti dell'episodio
    comments = episode_dao.get_comments_users(epId)

    today = date.today()

    return render_template('singleEpisode.html', podcast=podcast, episode=episode, comments=comments, today=today) 


# Modifica un episodio
@app.route('/podcast<int:pdId>/<int:epId>/modifyEpisode', methods=['POST'])
@login_required
def modify_episode(pdId, epId):
    extensions = ['mp3', 'wav', 'ogg']
    episode = request.form.to_dict()

    # Verifico che ci siano tutti i campi obbligatori
    if episode['Title'] == '' or episode['Description'] == '' or episode['Date'] == '':
        flash('Campi obbligatori mancanti', 'danger')
        return redirect(url_for('episode_page', pdId=pdId, epId=epId))

    # Verifico che i campi testuali siano conformi
    if len(episode['Description']) < 30 or len(episode['Description']) > 300 or len(episode['Title']) < 5 or len(episode['Title']) > 50 or datetime.strptime(episode['Date'], '%Y-%m-%d').date() > date.today():
        flash('Errore nella compilazione dei campi, riprova', 'danger')
        return redirect(url_for('home')) 

    # Traccia audio episodio
    if 'Audio' in request.files:
        episode_audio = request.files['Audio']
        audio_old = episode_dao.get_episode_audio(epId)['Audio']
        # Se ho la vecchia traccia audio la lascio
        if secure_filename(episode_audio.filename) == '':
            audio_name = audio_old
        # Se ho la nuova traccia audio la aggiorno
        else:
            if os.path.exists(f"static/{audio_old}"):
                os.remove(f"static/{audio_old}")

            filename = secure_filename(episode_audio.filename)
            filename = filename.rsplit('.', 1)
            
            if filename[1].lower() not in extensions:
                flash('File audio non supportato, riprova', 'danger')
                return redirect(url_for('episode_page', pdId=pdId, epId=epId))

            audio_name = f"{pdId}_{epId}_{current_user.id}.{filename[1].lower()}"
            audio_name = secure_filename(audio_name)
            episode_audio.save(f"static/{audio_name}")
    # Se ho avuto problemi nel form ritorno errore 
    else:
        flash('Errore nel caricamento del file audio, riprova', 'danger')
        return redirect(url_for('episode_page', pdId=pdId, epId=epId))

    episode = {
        'EpId' : epId,
        'Title' : episode['Title'],
        'Description' : episode['Description'],
        'Date' : episode['Date'],
        'Audio' : audio_name
    }

    if episode_dao.modify_episode(episode) == True:
        flash('Episodio modificato con successo', 'success')
    else:
        flash('Errore nella modifica dell\'episodio, riprova', 'danger')

    return redirect(url_for('episode_page', pdId=pdId, epId=epId))


# Elimina un episodio
@app.route('/podcast<int:pdId>/<int:epId>/deleteEpisode')
@login_required
def delete_episode(pdId, epId):
    podcast = podcast_dao.get_podcast_user(pdId)
    # Verifico che l'utente possa cancellare
    if not current_user.is_authenticated or current_user.id != podcast['UserId']:
        return render_template('error.html', error=401)

    # Prendo il nome della traccia audio dell'episodio
    audio = episode_dao.get_episode_audio(epId)['Audio']

    # Cancello la traccia audio
    if os.path.exists(f"static/{audio}"):
        os.remove(f"static/{audio}")

    # Verifico che non ci siano stati errori nel db
    if episode_dao.delete_episode(epId) == True:
        flash('Episodio eliminato con successo', 'success')
    else:
        flash('Errore nell\'eliminazione dell\'episodio', 'danger')

    return redirect(url_for('podcast_page', pdId=pdId))


# Inserisce un nuovo commento
@app.route('/podcast<int:pdId>/<int:epId>/newComment', methods=['POST'])
@login_required
def new_comment(pdId, epId):
    comment = request.form.to_dict()

    if comment['Text'] == '':
        return redirect(url_for('episode_page', pdId=pdId, epId=epId))

    if len(comment['Text']) < 1 or len(comment['Text']) > 200:
        flash('Lunghezza commento non valida, riprova', 'danger')
        return redirect(url_for('episode_page', pdId=pdId, epId=epId))

    comment = {
        'EpId' : epId,
        'UserId' : current_user.id,
        'Text' : comment['Text'],
        'Date' : date.today()
    }

    if episode_dao.insert_comment(comment) == False:
        flash('Errore nell\'inserimento del commento, riprovare', 'danger')

    return redirect(url_for('episode_page', pdId=pdId, epId=epId))


# Modifica un commento
@app.route('/podcast<int:pdId>/<int:epId>/<int:comId>/modifyComment', methods=['POST'])
@login_required
def modify_comment(pdId, epId, comId):
    comment = request.form.to_dict()

    if len(comment['Text']) < 1 or len(comment['Text']) > 200:
        flash('Lunghezza commento non valida, riprova', 'danger')
        return redirect(url_for('episode_page', pdId=pdId, epId=epId))
    
    comment = {
        'ComId' : comId,
        'Text' : comment['Text']
    }

    if episode_dao.modify_comment(comment) == False:
        flash('Errore nella modifica del commento, riprova', 'danger')
    else:
        flash('Commento modificato con successo', 'success')

    return redirect(url_for('episode_page', pdId=pdId, epId=epId))


# Emilina un commento
@app.route('/podcast<int:pdId>/<int:epId>/<int:comId>/deleteComment')
@login_required
def delete_comment(pdId, epId, comId):
    comment = episode_dao.get_comment(comId)
    # Verifico che l'utente possa eliminare
    if not current_user.is_authenticated or current_user.id != comment['UserId']:
        return render_template('error.html', error=401)

    # Cancello un commento, verificando che non ci siano errori nel db
    if episode_dao.delete_comment(comId) ==  True:
        flash('Commento eliminato con successo', 'success')
    else:
        flash('Errore nella cancellazione del commento, riporvare', 'danger')

    return redirect(url_for('episode_page', pdId=pdId, epId=epId))


# Mostra la pagina personale di ciascun utente
@app.route('/user')
@login_required
def user_page():

    # Cerco tutti i podcast seguiti dall'utente
    podcasts = users_dao.get_podcasts_followed(current_user.id)

    return render_template('userPage.html', podcasts=podcasts)


# Fa accedere l'utente
@app.route('/logIn', methods=['POST'])
def log_in():
    log = request.form.to_dict()

    # Verifico che i campi obbligatori siano presenti
    if log['Email'] == '' or log['Password'] == '':
        flash('Campi obbligatori mancanti', 'danger')
        return redirect(request.referrer)

    # Cerco l'utente corrispondente all'email
    userdb = users_dao.get_user_by_email(log['Email'])

    # Verifico se l'utente esiste e se la password corrisponde
    if not userdb or not check_password_hash(userdb['Password'], log['Password']):
        flash('Credenziali non valide, riprovare', 'danger')
        return redirect(request.referrer)
    
    user = User(id=userdb['UserId'], email=userdb['Email'], name=userdb['Name'], surname=userdb['Surname'], creator=userdb['Creator'], password=userdb['Password'])
    login_user(user, True)

    return redirect(request.referrer)


# Registra un utente
@app.route('/signUp', methods=['POST'])
def sign_up():
    user = request.form.to_dict()

    # Se mancano dei campi obbligatori nella registrazione ritorno errore
    if user['Email'] == '' or user['Name'] == '' or user['Surname'] == '' or user['Password'] == '':
        flash('Campi obbligatori mancanti', 'danger')
        return redirect(request.referrer)

    # Verifico che il formato della mail sia giusto
    if '@' not in user['Email'] or '.' not in (user['Email'].split('@'))[1]:
        flash('Email inserita non valida', 'danger')
        return redirect(request.referrer)

    # Se c'è già un untente con questa email ritorno errore 
    if users_dao.get_user_by_email((user['Email']).lower()):
        flash('C\'è già un utente registrato con questa email', 'danger')
        return redirect(request.referrer)

    if 'Creator' in user:
        creator = 'Yes'
    else:
        creator = 'No'

    user = {
        'Email' : (user['Email']).lower(),
        'Name' : user['Name'].title(),
        'Surname' : user['Surname'].title(),
        'Creator' : creator,
        'Password' : generate_password_hash(user['Password'], method="sha256")
    }

    # Inserisco l'utente nel database
    if users_dao.insert_user(user) == False:
        flash('Errore nella creazione dell\'utente, riprovare', 'danger')
        return redirect(request.referrer)
    else:
        flash('Utente registrato correttamente', 'success')

    # Cerco l'utente nel database
    userdb = users_dao.get_user_by_email(user['Email'])

    # La registrazione mi porta ad avere l'accesso automaticamente
    user = User(id=userdb['UserId'], email=userdb['Email'], name=userdb['Name'], surname=userdb['Surname'], creator=userdb['Creator'], password=userdb['Password'])
    login_user(user, True)

    

    return redirect(request.referrer)


# Fa il loug out
@app.route('/logOut')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('home'))


# Dice a flask come ricavare uno user
@login_manager.user_loader
def load_user(user_id):
    # Prendo lo user da db
    userdb = users_dao.get_user(user_id)
    if userdb:
        # Creo lo User
        user = User(id=userdb['UserId'], email=userdb['Email'], name=userdb['Name'], surname=userdb['Surname'], creator=userdb['Creator'], password=userdb['Password'])
    else:
        user = None

    return user


# Imposta il server
if __name__ == "__main__":
    # Imposta i parametri per il server locale
    app.run(host='0.0.0.0', port=3000, debug=True)
