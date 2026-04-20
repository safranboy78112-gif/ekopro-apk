[app]
# (str) Uygulama Adı
title = EKG Analiz Pro

# (str) Paket adı
package.name = ekganalizpro

# (str) Paket domain (Örnek: com.isim.uygulama)
package.domain = org.test

# (str) Kaynak dosyalar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Versiyon
version = 0.1

# (list) Kütüphaneler (Uygulamanın çalışması için gerekenler)
# Eğer uygulamanın içinde ek kütüphaneler varsa (pandas, numpy gibi), virgülle buraya ekle.
requirements = python3,kivy

# (int) Android API seviyesi
android.api = 33
android.minapi = 21

# (int) NDK sürümü (GitHub için en kararlısı)
android.ndk = 25b

# (list) Mimari (Hata almamak için ikisini de yazıyoruz)
android.archs = armeabi-v7a,arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
