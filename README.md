2411081501
OSAMA SAMSOUM
https://uniproject-vh4c.onrender.com/

1. Projenin Amacı (Neden bu proje?)
Bu proje neden yapıldı?
Bu proje, temel bir kullanıcı yönetimi ve kişisel veri (örneğin, günlük girdileri) depolama sistemi oluşturarak, Flask framework'ünün temel özelliklerini ve web uygulaması geliştirme prensiplerini uygulamalı olarak öğrenmek amacıyla yapılmıştır. Kullanıcı kimlik doğrulama, oturum yönetimi ve basit CRUD (Oluşturma, Okuma, Güncelleme, Silme) operasyonlarının nasıl entegre edildiğini göstermeyi hedeflemektedir.

Hangi problemi çözüyor?
Proje, kullanıcıların güvenli bir şekilde hesap oluşturup giriş yapabildiği ve kendilerine ait özel bilgileri (bu örnekte "günlük girdileri") saklayabildiği basit bir platform ihtiyacını çözmektedir. Geleneksel not defterleri veya dijital metin dosyaları yerine, web tabanlı ve kullanıcıya özel bir depolama alanı sunar. Ayrıca, verilerin JSON formatında dışa aktarılabilmesi, veri taşınabilirliği ve yedekleme sorunlarına basit bir çözüm getirir.

Gerçek dünyadaki karşılığı var mı?
Evet, bu projenin gerçek dünyada birçok karşılığı bulunmaktadır. Örneğin:

Kişisel Not Uygulamaları: Kullanıcıların notlarını, fikirlerini veya günlüklerini sakladığı uygulamalar (Evernote, Google Keep benzeri, ancak çok daha basit bir ölçekte).

Basit Blog Sistemleri: Kullanıcıların kendi yazılarını oluşturup yönetebildiği kişisel blog platformlarının temelini oluşturabilir.

Envanter Takip Sistemleri: Kullanıcıların kendi envanterlerini (kitap, film koleksiyonu vb.) takip ettiği basit uygulamalar için bir başlangıç noktası olabilir.

Eğitim Platformları: Kullanıcıların ilerlemelerini veya ödevlerini kaydedebileceği basit modüller.

2. Projenin Kapsamı ve Özellikleri
Sistem ne yapabiliyor, ne yapamıyor?
Yapabiliyor:

Yeni kullanıcı kaydı yapabiliyor (kullanıcı adı, şifre ve isteğe bağlı e-posta ile).

Kayıtlı kullanıcıların giriş yapmasını ve oturum açmasını sağlayabiliyor.

Kullanıcıların çıkış yapmasını sağlayabiliyor.

Giriş yapmış kullanıcıların kişisel kontrol paneline erişmesini sağlayabiliyor.

Kullanıcıların kendi günlük girdilerini (başlık ve içerik ile) oluşturmasını, okumasını, düzenlemesini ve silmesini sağlayabiliyor.

Veritabanındaki tüm kullanıcı ve onlara ait girdileri hiyerarşik bir JSON yapısında dışa aktarabiliyor (şifre hash'leri hariç).

Flash mesajları ile kullanıcıya geri bildirim sağlayabiliyor.

Yapamıyor:

Gelişmiş şifre kurtarma veya parola sıfırlama işlevleri sunmuyor.

Kullanıcı profili güncelleme (e-posta veya kullanıcı adı değiştirme) işlevselliği yok.

Veritabanı olarak sadece basit bir JSON dosyası kullanıyor, bu da büyük ölçekli veya eş zamanlı çok kullanıcılı uygulamalar için uygun değildir.

Girdi arama veya filtreleme özellikleri bulunmuyor.

Dosya yükleme veya medya yönetimi gibi gelişmiş özellikler içermiyor.

API güvenliği (rate limiting, CORS vb.) gibi konular ele alınmamıştır.

Hangi işlevleri içeriyor?

Kullanıcı Yönetimi:

/register: Yeni kullanıcı kaydı.

/login: Mevcut kullanıcı girişi.

/logout: Kullanıcı çıkışı.

Oturum yönetimi (session).

Günlük Girdisi Yönetimi (CRUD):

/dashboard: Kullanıcının kendi girdilerini listelediği kontrol paneli.

/entries/new: Yeni bir günlük girdisi oluşturma.

/entries/edit/<int:entry_id>: Mevcut bir günlük girdisini düzenleme.

/entries/delete/<int:entry_id>: Mevcut bir günlük girdisini silme.

Veri Dışa Aktarma:

/export_database_json: Veritabanını JSON formatında dışa aktarma (kullanıcıya ait girdiler hiyerarşik olarak listelenir).

Kapsam dışında neler kaldı? Neden?

Gelişmiş Güvenlik Özellikleri: Örneğin, iki faktörlü kimlik doğrulama, CAPTCHA, şifre politikaları (karmaşıklık kontrolü) kapsam dışı bırakıldı. Bu, projenin temel Flask ve CRUD operasyonlarına odaklanmasını sağlamak ve karmaşıklığı azaltmak içindi.

Gelişmiş Veritabanı Sistemleri: PostgreSQL, MySQL gibi ilişkisel veritabanları veya MongoDB gibi NoSQL veritabanları kullanılmadı. Bunun yerine basit bir JSON dosyası tercih edildi. Amaç, veritabanı kurulumu ve ORM (Object-Relational Mapping) gibi konularla uğraşmadan Flask'ın temel işlevselliğini göstermekti.

Kullanıcı Rolleri/Yetkilendirme: Admin, normal kullanıcı gibi farklı roller ve bu rollere özel yetkilendirmeler (örneğin, sadece adminlerin veritabanını dışa aktarabilmesi) eklenmedi. Bu, projenin temel kullanıcı deneyimine odaklanmasını sağlamak içindi.

Arama ve Filtreleme: Günlük girdileri arasında arama veya filtreleme özellikleri eklenmedi. Projenin ana odağı CRUD işlemleri ve kullanıcı yönetimi olduğu için bu tür ek işlevler basitlik adına dışarıda bırakıldı.

Frontend Framework'leri: React, Vue, Angular gibi modern JavaScript framework'leri kullanılmadı. Jinja2 şablon motoru ve Tailwind CSS ile basit, sunucu tarafında render edilen bir arayüz yeterli görüldü.