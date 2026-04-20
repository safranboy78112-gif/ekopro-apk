import os
import json
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivy.utils import platform

# Android Paylaşım İntenti
if platform == 'android':
    from jnius import autoclass

class EKGPro(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # 1. Kamera (Hız: Başlangıçta açık)
        self.camera = Camera(play=True, resolution=(640, 480))
        self.add_widget(self.camera)
        
        # 2. Bilgi ve Sonuç
        self.label = Label(text="Hazır: EKG'yi hizala ve ANALİZ ET.", size_hint_y=0.2)
        self.add_widget(self.label)
        
        # 3. İsim Girişi (Opsiyonel)
        self.name_input = TextInput(hint_text="Hasta Adı (İsteğe bağlı)", size_hint_y=None, height=40, multiline=False)
        self.add_widget(self.name_input)
        
        # 4. Butonlar (Hız ve Fonksiyon)
        btn_layout = BoxLayout(size_hint_y=0.2)
        btn_analiz = Button(text="ANALİZ ET", background_color=(0, 1, 0, 1), on_press=self.baslat_analiz)
        btn_kaydet = Button(text="KAYDET", on_press=self.kaydet)
        btn_sil = Button(text="SİL", on_press=self.sil)
        btn_paylas = Button(text="PAYLAŞ", background_color=(0, 0, 1, 1), on_press=self.paylas)
        
        btn_layout.add_widget(btn_analiz)
        btn_layout.add_widget(btn_kaydet)
        btn_layout.add_widget(btn_sil)
        btn_layout.add_widget(btn_paylas)
        self.add_widget(btn_layout)

        # 5. Sabit Uyarı
        self.add_widget(Label(text="YASAL UYARI: Teşhis koymaz, yardımcı araçtır.", color=(1, 0, 0, 1), size_hint_y=0.05))

    def baslat_analiz(self, *args):
        self.label.text = "Analiz ediliyor..."
        self.camera.play = False 
        threading.Thread(target=self.analiz_mantigi).start()

    def analiz_mantigi(self):
        """
        RİTİM VE MORFOLOJİ ANALİZ MOTORU
        TFLite modelin veya eşik değerlerin burada çalışır.
        """
        # ÖRNEK: Buraya QRS morfoloji kontrolünü koyacaksın
        # qrs_width = measure_qrs()
        # if qrs_width > 120: sonuc = "Geniş QRS (Anomali)"
        
        sonuc = "Ritim: Sinüs, Morfoloji: Normal" 
        Clock.schedule_once(lambda dt: self.set_sonuc(sonuc))

    def set_sonuc(self, sonuc):
        self.label.text = f"SONUÇ: {sonuc}"

    def kaydet(self, *args):
        isim = self.name_input.text or "Hasta_Kayıtsız"
        data = {"sonuc": self.label.text}
        path = os.path.join(App.get_running_app().user_data_dir, f"{isim}.json")
        with open(path, 'w', encoding='utf-8') as f: json.dump(data, f)
        self.label.text = f"{isim} kaydedildi."
        self.camera.play = True

    def sil(self, *args):
        isim = self.name_input.text
        path = os.path.join(App.get_running_app().user_data_dir, f"{isim}.json")
        if os.path.exists(path):
            os.remove(path)
            self.label.text = "Kayıt silindi."
        self.camera.play = True

    def paylas(self, *args):
        if platform == 'android':
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            intent = Intent(Intent.ACTION_SEND)
            intent.setType("text/plain")
            intent.putExtra(Intent.EXTRA_TEXT, self.label.text)
            currentActivity = PythonActivity.mActivity
            currentActivity.startActivity(Intent.createChooser(intent, "Paylaş:"))
        else:
            self.label.text = "Paylaşım sadece Android'de."

class EKGApp(App):
    def build(self):
        return EKGPro()

if __name__ == '__main__':
    EKGApp().run()