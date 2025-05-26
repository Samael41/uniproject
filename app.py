# Gerekli Flask modüllerini ve diğer kütüphaneleri import edelim
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import random

# Flask uygulamasını başlatalım
app = Flask(__name__)
app.secret_key = 'çok_gizli_bir_anahtar'  # Session yönetimi için gizli anahtar (production'da değiştirin)

# Veritabanı dosyası için yol (basitlik açısından JSON dosyası kullanacağız)
DATABASE_FILE = 'database.json'

# --- Veritabanı Yardımcı Fonksiyonları ---

def load_db():
    """Veritabanını JSON dosyasından yükler."""
    if not os.path.exists(DATABASE_FILE):
        # Eğer veritabanı dosyası yoksa, örnek bir yapı ile oluşturalım
        initial_data = {
            "users": [],  # Kullanıcılar listesi
            "entries": [] # Örnek olarak 'günlük girdileri' için bir liste (ikinci class)
        }
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=4)
        return initial_data
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Hata durumunda veya dosya boşsa başlangıç verisiyle dön
        return {"users": [], "entries": []}

def save_db(data):
    """Veritabanını JSON dosyasına kaydeder."""
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_user_by_username(username):
    """Kullanıcı adına göre kullanıcıyı bulur."""
    db = load_db()
    for user in db['users']:
        if user['username'] == username:
            return user
    return None

def get_user_by_id(user_id):
    """Kullanıcı ID'sine göre kullanıcıyı bulur."""
    db = load_db()
    for user in db['users']:
        if user['id'] == user_id:
            return user
    return None

def get_next_user_id():
    """Yeni kullanıcı için bir sonraki ID'yi alır."""
    db = load_db()
    if not db['users']:
        return 1
    return max(user['id'] for user in db['users']) + 1

def get_next_entry_id():
    """Yeni girdi için bir sonraki ID'yi alır."""
    db = load_db()
    if not db['entries']:
        return 1
    return max(entry['id'] for entry in db['entries']) + 1

# --- Rotalar (Routes) ---

@app.route('/')
def index():
    """Ana sayfa."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Kullanıcı kayıt sayfası."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form.get('email', '') # E-posta alanı isteğe bağlı olabilir

        db = load_db()

        if get_user_by_username(username):
            flash('Bu kullanıcı adı zaten alınmış!', 'danger')
            return redirect(url_for('register'))

        # Şifreyi hash'leyelim (SHA-256 veya benzeri güvenli bir algoritma)
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = {
            "id": get_next_user_id(),
            "username": username,
            "password_hash": hashed_password,
            "email": email
        }
        db['users'].append(new_user)
        save_db(db)

        flash('Kayıt başarılı! Lütfen giriş yapın.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Kullanıcı giriş sayfası."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Kullanıcı çıkış işlemi."""
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Kullanıcıya özel kontrol paneli (login gerektirir)."""
    if 'user_id' not in session:
        flash('Bu sayfayı görüntülemek için giriş yapmalısınız.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = load_db()
    # Kullanıcıya ait girdileri filtrele
    user_entries = [entry for entry in db['entries'] if entry.get('user_id') == user_id]

    return render_template('dashboard.html', entries=user_entries)

# --- Örnek CRUD İşlemleri (Günlük Girdileri için) ---
# Bu kısım, projenizin konusuna göre (kitap, stok vb.) uyarlanmalıdır.

@app.route('/entries/new', methods=['GET', 'POST'])
def new_entry():
    """Yeni bir girdi ekleme sayfası (login gerektirir)."""
    if 'user_id' not in session:
        flash('Girdi eklemek için giriş yapmalısınız.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']

        db = load_db()
        new_entry_item = {
            "id": get_next_entry_id(),
            "user_id": user_id,
            "title": title,
            "content": content,
            # "timestamp": datetime.utcnow().isoformat() # Zaman damgası eklenebilir
        }
        db['entries'].append(new_entry_item)
        save_db(db)
        flash('Yeni girdi başarıyla eklendi!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('new_entry.html')

@app.route('/entries/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    """Bir girdiyi düzenleme sayfası (login gerektirir)."""
    if 'user_id' not in session:
        flash('Girdi düzenlemek için giriş yapmalısınız.', 'warning')
        return redirect(url_for('login'))

    db = load_db()
    entry = next((e for e in db['entries'] if e['id'] == entry_id and e.get('user_id') == session['user_id']), None)

    if not entry:
        flash('Düzenlenecek girdi bulunamadı veya yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        entry['title'] = request.form['title']
        entry['content'] = request.form['content']
        save_db(db)
        flash('Girdi başarıyla güncellendi!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_entry.html', entry=entry)

@app.route('/entries/delete/<int:entry_id>', methods=['POST']) # Genellikle POST ile silme yapılır
def delete_entry(entry_id):
    """Bir girdiyi silme işlemi (login gerektirir)."""
    if 'user_id' not in session:
        flash('Girdi silmek için giriş yapmalısınız.', 'warning')
        return redirect(url_for('login'))

    db = load_db()
    # Girdiyi bul ve sil (sadece kullanıcıya aitse)
    original_length = len(db['entries'])
    db['entries'] = [e for e in db['entries'] if not (e['id'] == entry_id and e.get('user_id') == session['user_id'])]

    if len(db['entries']) < original_length:
        save_db(db)
        flash('Girdi başarıyla silindi!', 'success')
    else:
        flash('Silinecek girdi bulunamadı veya yetkiniz yok.', 'danger')

    return redirect(url_for('dashboard'))


# --- Veritabanı JSON Çıktısı ---
@app.route('/export_database_json')
def export_database_json():
    """Veritabanının tamamını JSON olarak dışa aktarır."""
    if 'user_id' not in session: # İsteğe bağlı: Sadece adminler için kısıtlanabilir
        flash('Bu işlem için yetkiniz yok.', 'danger')
        return redirect(url_for('index'))

    db_content = load_db()
    # Kullanıcı şifre hash'lerini güvenlik nedeniyle çıktıdan kaldıralım
    # Proje gereksinimine göre bu kısım ayarlanabilir.
    # Eğer tüm verinin (şifre hash'leri dahil) dışa aktarılması gerekiyorsa, aşağıdaki satırları kaldırın.
    users_without_passwords = []
    for user in db_content.get("users", []):
        user_copy = user.copy()
        user_copy.pop("password_hash", None) # Şifre hash'ini kaldır
        users_without_passwords.append(user_copy)
    
    # Kullanıcılara ait girdileri hiyerarşik olarak ekleyelim
    # Bu kısım, "1.8 JSON veri çıktısı" gereksinimini karşılar:
    # "Json dosyası hiyerarşik veri yapısı ile sunulmalı. Derste gösterilen örnek çıktı gibi,
    # kullanıcı ve ona bağlı olan kayıtların listelenmesi."
    
    output_data = {"users": []}
    all_entries = db_content.get("entries", [])

    for user_data in users_without_passwords:
        user_id = user_data["id"]
        user_data["user_entries"] = [entry for entry in all_entries if entry.get("user_id") == user_id]
        output_data["users"].append(user_data)

    # Eğer "entries" anahtarı altında kullanıcıya bağlı olmayan girdiler varsa, onları da ekleyebiliriz.
    # Ya da sadece kullanıcılara bağlı girdileri göstermek yeterliyse bu kısım atlanabilir.
    # output_data["other_entries"] = [entry for entry in all_entries if "user_id" not in entry]


    # Proje klasörüne 'database_export.json' olarak kaydetmek için:
    
    fileName = f'database_export-{random.randint(10**8, 10**9 - 1)}.json'
    export_file_path = os.path.join(os.path.dirname(__file__), 'files', fileName)
    with open(export_file_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
    
    flash(f"<a class=\"underline text-blue-50\" href=\"/files/{fileName}\" download>{fileName}</a> dosyası proje klasörüne kaydedildi.", 'info')
    # return jsonify(db_content) # Tarayıcıda göstermek için
    return redirect(url_for('dashboard')) # Veya başka bir sayfaya yönlendir

# Route to retrieve files
@app.route('/files/<filename>')
def retrieve_file(filename):
    try:
        # Define the directory where files are stored
        directory = os.path.join(os.path.dirname(__file__), 'files')
        # Serve the file from the directory
        return send_from_directory(directory, filename, as_attachment=True)
    except FileNotFoundError:
        flash("Requested file not found.", "error")
        return redirect(url_for('dashboard'))


# Uygulamayı çalıştırma (debug modu geliştirme için aktif)
if __name__ == '__main__':
    # Render.com gibi platformlar kendi WSGI sunucularını kullanır,
    # bu yüzden `app.run` genellikle `if __name__ == '__main__':` bloğunda olmalıdır.
    # Render için bir `gunicorn` komutu (örn: gunicorn app:app) kullanılır.
    app.run(debug=True)