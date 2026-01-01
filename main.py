import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                               QComboBox, QTextEdit, QDateEdit, QMessageBox,
                               QGroupBox, QFormLayout, QTabWidget, QSplitter,
                               QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea,
                               QDialog)
from PySide6.QtCore import QDate, Qt
from PySide6.QtGui import QFont, QIcon, QColor

# Cloud veritabanı kullan (Supabase)
from database_supabase import SupabaseDB as Database

from datetime import datetime

class SigortaAcenteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
    
    def init_ui(self):
        """Ana pencereyi oluştur"""
        self.setWindowTitle("BUDUN - Sigorta Yönetim Sistemi")
        self.setGeometry(100, 100, 900, 700)
        
        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Başlık
        baslik = QLabel("BUDUN")
        baslik_font = QFont("Courier New", 42, QFont.Weight.Black)
        baslik.setFont(baslik_font)
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("""
            color: #0d47a1; 
            padding: 20px;
            letter-spacing: 30px;
            font-weight: 900;
            background: transparent;
        """)
        main_layout.addWidget(baslik)
        
        # Tab Widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Müşteri ve Poliçe Ekleme Sekmesi
        musteri_police_tab = QWidget()
        tabs.addTab(musteri_police_tab, "POLİÇE GİRİŞ")
        
        self.setup_musteri_police_tab(musteri_police_tab)
        
        # Yenilemeler Sekmesi
        yenilemeler_tab = QWidget()
        tabs.addTab(yenilemeler_tab, "YENİLEMELER")
        
        self.setup_yenilemeler_tab(yenilemeler_tab)
        
        # Raporlar Sekmesi
        raporlar_tab = QWidget()
        tabs.addTab(raporlar_tab, "RAPORLAR")
        
        self.setup_raporlar_tab(raporlar_tab)
        
        # Finans Sekmesi
        finans_tab = QWidget()
        tabs.addTab(finans_tab, "FİNANS")
        
        self.setup_finans_tab(finans_tab)
        
        # Çapraz Satış Sekmesi
        capraz_satis_tab = QWidget()
        tabs.addTab(capraz_satis_tab, "ÇAPRAZ SATIŞ")
        
        self.setup_capraz_satis_tab(capraz_satis_tab)
        
        # Stil ayarları - GRİ MAVİ TEMA
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #bbdefb, stop:1 #cfd8dc);
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #78909c;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #37474f;
            }
            QLineEdit, QComboBox, QDateEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #90a4ae;
                border-radius: 4px;
                background-color: #fafafa;
                font-size: 11pt;
                color: #263238;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
                border: 2px solid #1976d2;
                background-color: #ffffff;
            }
            QPushButton {
                padding: 10px 20px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1976d2, stop:1 #1565c0);
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 11pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1565c0, stop:1 #0d47a1);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #0d47a1, stop:1 #0d47a1);
            }
            QLabel {
                font-size: 10pt;
                color: #37474f;
            }
            QTabWidget::pane {
                border: 2px solid #78909c;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #b0bec5, stop:1 #90a4ae);
                color: #263238;
                padding: 10px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1976d2, stop:1 #1565c0);
                color: white;
            }
        """)
    
    def setup_musteri_police_tab(self, tab):
        """Müşteri ve Poliçe ekleme sekmesini oluştur"""
        # Ana layout
        main_layout = QHBoxLayout()
        tab.setLayout(main_layout)
        
        # Splitter ile sol ve sağ bölüm
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # SOL TARAF - FORM
        sol_widget = QWidget()
        sol_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #37474f, stop:1 #263238);
            }
            QLineEdit, QTextEdit {
                background-color: #eceff1;
                color: #000000;
                border: 2px solid #90a4ae;
                border-radius: 4px;
                padding: 5px;
                font-size: 10pt;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #42a5f5;
                background-color: #ffffff;
            }
            QComboBox {
                background-color: #eceff1;
                color: #000000;
                border: 2px solid #90a4ae;
                border-radius: 4px;
                padding: 5px;
                font-size: 10pt;
            }
            QComboBox:focus {
                border: 2px solid #42a5f5;
                background-color: #ffffff;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #b0bec5;
                width: 30px;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #263238;
                width: 0;
                height: 0;
            }
            QDateEdit {
                background-color: #eceff1;
                color: #000000;
                border: 2px solid #90a4ae;
                border-radius: 4px;
                padding: 5px;
                font-size: 10pt;
            }
            QDateEdit:focus {
                border: 2px solid #42a5f5;
                background-color: #ffffff;
            }
            QDateEdit::drop-down {
                border: none;
                background-color: #b0bec5;
                width: 30px;
                border-top-right-radius: 4px;
                border-bottom-right-radius: 4px;
            }
            QDateEdit::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #263238;
                width: 0;
                height: 0;
            }
        """)
        layout = QVBoxLayout()
        sol_widget.setLayout(layout)
        
        # Scroll area ekle (uzun formlar için)
        scroll = QScrollArea()
        scroll.setWidget(sol_widget)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        splitter.addWidget(scroll)
        
        # MÜŞTER BİLGİLERİ BÖLÜMÜ
        musteri_group = QGroupBox("Müşteri Bilgileri")
        musteri_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                color: white;
                border: 2px solid #546e7a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: rgba(69, 90, 100, 0.3);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 10px;
                background-color: #546e7a;
                border-radius: 5px;
                color: white;
            }
        """)
        musteri_layout = QFormLayout()
        musteri_group.setLayout(musteri_layout)
        
        # Form label'larını beyaz yap
        musteri_layout.setLabelAlignment(Qt.AlignRight)
        
        # Müşteri form alanları
        self.ad_soyad_input = QLineEdit()
        ad_label = QLabel("Ad Soyad:")
        ad_label.setStyleSheet("color: white;")
        musteri_layout.addRow(ad_label, self.ad_soyad_input)
        
        self.tc_no_input = QLineEdit()
        self.tc_no_input.setMaxLength(11)
        tc_label = QLabel("TC No:")
        tc_label.setStyleSheet("color: white;")
        musteri_layout.addRow(tc_label, self.tc_no_input)
        
        self.telefon_input = QLineEdit()
        tel_label = QLabel("Telefon:")
        tel_label.setStyleSheet("color: white;")
        musteri_layout.addRow(tel_label, self.telefon_input)
        
        self.email_input = QLineEdit()
        email_label = QLabel("E-mail:")
        email_label.setStyleSheet("color: white;")
        musteri_layout.addRow(email_label, self.email_input)
        
        layout.addWidget(musteri_group)
        
        # POLİÇE BİLGİLERİ BÖLÜMÜ
        police_group = QGroupBox("Poliçe Bilgileri")
        police_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                color: white;
                border: 2px solid #546e7a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: rgba(69, 90, 100, 0.3);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 10px;
                background-color: #546e7a;
                border-radius: 5px;
                color: white;
            }
        """)
        police_layout = QFormLayout()
        police_group.setLayout(police_layout)
        
        # Form label'larını beyaz yap
        police_layout.setLabelAlignment(Qt.AlignRight)
        
        # Poliçe form alanları
        self.police_no_input = QLineEdit()
        police_no_label = QLabel("Poliçe No:")
        police_no_label.setStyleSheet("color: white;")
        police_layout.addRow(police_no_label, self.police_no_input)
        
        self.sigorta_turu_combo = QComboBox()
        self.sigorta_turu_combo.addItems([
            "Seçiniz",
            "Kasko",
            "Trafik",
            "Konut",
            "İşyeri",
            "Sağlık",
            "Hayat",
            "Dask",
            "Seyahat",
            "Ferdi Kaza"
        ])
        tur_label = QLabel("Poliçe Türü:")
        tur_label.setStyleSheet("color: white;")
        police_layout.addRow(tur_label, self.sigorta_turu_combo)
        
        self.sirket_combo = QComboBox()
        self.sirket_combo.addItems([
            "Seçiniz",
            "Anadolu Sigorta",
            "Allianz",
            "AXA Sigorta",
            "HDI Sigorta",
            "Mapfre Sigorta",
            "Türk Nippon",
            "Aksigorta",
            "Groupama",
            "Ziraat Sigorta",
            "Halk Sigorta"
        ])
        sirket_label = QLabel("Sigorta Şirketi:")
        sirket_label.setStyleSheet("color: white;")
        police_layout.addRow(sirket_label, self.sirket_combo)
        
        self.baslangic_tarihi = QDateEdit()
        self.baslangic_tarihi.setCalendarPopup(True)
        self.baslangic_tarihi.setDate(QDate.currentDate())
        self.baslangic_tarihi.setDisplayFormat("dd.MM.yyyy")
        self.baslangic_tarihi.dateChanged.connect(self.baslangic_tarihi_degisti)
        baslangic_label = QLabel("Başlangıç Tarihi:")
        baslangic_label.setStyleSheet("color: white;")
        police_layout.addRow(baslangic_label, self.baslangic_tarihi)
        
        self.bitis_tarihi = QDateEdit()
        self.bitis_tarihi.setCalendarPopup(True)
        self.bitis_tarihi.setDate(QDate.currentDate().addYears(1))
        self.bitis_tarihi.setDisplayFormat("dd.MM.yyyy")
        bitis_label = QLabel("Bitiş Tarihi:")
        bitis_label.setStyleSheet("color: white;")
        police_layout.addRow(bitis_label, self.bitis_tarihi)
        
        self.prim_tutari_input = QLineEdit()
        prim_label = QLabel("Prim Tutarı (₺):")
        prim_label.setStyleSheet("color: white;")
        police_layout.addRow(prim_label, self.prim_tutari_input)
        
        self.aciklama_input = QTextEdit()
        self.aciklama_input.setMaximumHeight(80)
        aciklama_label = QLabel("Açıklama:")
        aciklama_label.setStyleSheet("color: white;")
        police_layout.addRow(aciklama_label, self.aciklama_input)
        
        # Ödeme şekli
        self.odeme_sekli_combo = QComboBox()
        self.odeme_sekli_combo.addItems(["Nakit", "Müşteri Kartı", "Havale"])
        odeme_label = QLabel("Ödeme Şekli:")
        odeme_label.setStyleSheet("color: white;")
        police_layout.addRow(odeme_label, self.odeme_sekli_combo)
        
        # Satışçı seçimi
        self.satisci_combo = QComboBox()
        self.satiscilari_yukle()
        satisci_label = QLabel("Satışçı:")
        satisci_label.setStyleSheet("color: white;")
        police_layout.addRow(satisci_label, self.satisci_combo)
        
        layout.addWidget(police_group)
        
        # KAYDET BUTONU
        kaydet_btn = QPushButton("💾 KAYDET")
        kaydet_btn.clicked.connect(self.kaydet)
        kaydet_btn.setMinimumHeight(50)
        kaydet_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #546e7a, stop:1 #37474f);
                font-size: 13pt;
                color: white;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #455a64, stop:1 #263238);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #263238, stop:1 #1a1a1a);
            }
        """)
        layout.addWidget(kaydet_btn)
        
        # BUDUN LOGO (Alt - Minimal Pixel)
        budun_logo = QLabel("BUDUN")
        budun_logo_font = QFont("Courier New", 72, QFont.Weight.Black)
        budun_logo.setFont(budun_logo_font)
        budun_logo.setAlignment(Qt.AlignCenter)
        budun_logo.setStyleSheet("""
            QLabel {
                color: #0d47a1;
                padding: 25px;
                margin-top: 30px;
                background: transparent;
                letter-spacing: 28px;
                font-weight: 900;
            }
        """)
        layout.addWidget(budun_logo)
        layout.addStretch()
        
        # SAĞ TARAF - POLİÇE LİSTESİ
        sag_widget = QWidget()
        sag_layout = QVBoxLayout()
        sag_widget.setLayout(sag_layout)
        
        # Liste başlığı
        liste_baslik = QLabel("📋 Kayıtlı Poliçeler")
        liste_baslik.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #37474f;
            padding: 10px;
            background-color: #eceff1;
            border-radius: 5px;
        """)
        sag_layout.addWidget(liste_baslik)
        
        # FİLTRE BÖLÜMÜ
        filtre_widget = QWidget()
        filtre_layout = QHBoxLayout()
        filtre_widget.setLayout(filtre_layout)
        
        # Arama kutusu
        filtre_label = QLabel("🔍 Ara:")
        filtre_label.setStyleSheet("font-weight: bold; color: #37474f;")
        filtre_layout.addWidget(filtre_label)
        
        self.arama_input = QLineEdit()
        self.arama_input.setPlaceholderText("Müşteri adı, poliçe no veya şirket ara...")
        self.arama_input.textChanged.connect(self.police_filtrele)
        filtre_layout.addWidget(self.arama_input)
        
        # Poliçe türü filtresi
        filtre_layout.addWidget(QLabel("Poliçe Türü:"))
        self.filtre_tur_combo = QComboBox()
        self.filtre_tur_combo.addItems([
            "Tümü", "Kasko", "Trafik", "Konut", "İşyeri", 
            "Sağlık", "Hayat", "Dask", "Seyahat", "Ferdi Kaza"
        ])
        self.filtre_tur_combo.currentTextChanged.connect(self.police_filtrele)
        filtre_layout.addWidget(self.filtre_tur_combo)
        
        # Şirket filtresi
        filtre_layout.addWidget(QLabel("Şirket:"))
        self.filtre_sirket_combo = QComboBox()
        self.filtre_sirket_combo.addItems([
            "Tümü", "Anadolu Sigorta", "Allianz", "AXA Sigorta", 
            "HDI Sigorta", "Mapfre Sigorta", "Türk Nippon", 
            "Aksigorta", "Groupama", "Ziraat Sigorta", "Halk Sigorta"
        ])
        self.filtre_sirket_combo.currentTextChanged.connect(self.police_filtrele)
        filtre_layout.addWidget(self.filtre_sirket_combo)
        
        # Temizle butonu
        temizle_btn = QPushButton("🔄 Temizle")
        temizle_btn.clicked.connect(self.filtreleri_temizle)
        temizle_btn.setStyleSheet("""
            QPushButton {
                background: #78909c;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background: #546e7a;
            }
        """)
        filtre_layout.addWidget(temizle_btn)
        
        sag_layout.addWidget(filtre_widget)
        
        # Tablo widget
        self.police_table = QTableWidget()
        self.police_table.setColumnCount(9)
        self.police_table.setHorizontalHeaderLabels([
            "Müşteri", "Poliçe No", "Tür", "Şirket", 
            "Başlangıç", "Bitiş", "Prim (₺)", "Komisyon (₺)", "Satışçı"
        ])
        
        # Tablo stil ayarları
        self.police_table.setAlternatingRowColors(True)
        self.police_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.police_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.police_table.verticalHeader().setVisible(False)
        
        # Çift tıklama eventi
        self.police_table.itemDoubleClicked.connect(self.police_detay_ac)
        
        # Tüm kolonları eşit genişlikte yap
        header = self.police_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Sütunları sürüklenebilir yap
        header.setSectionsMovable(True)
        header.setDragEnabled(True)
        header.setDragDropMode(QHeaderView.InternalMove)
        
        self.police_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #78909c;
                border-radius: 5px;
                gridline-color: #cfd8dc;
            }
            QTableWidget::item {
                padding: 5px;
                color: #000000;
            }
            QTableWidget::item:selected {
                background-color: #64b5f6;
                color: #000000;
                border: 2px solid #1976d2;
            }
            QTableWidget::item:hover {
                background-color: rgba(100, 181, 246, 0.3);
            }
            QHeaderView::section {
                background-color: #546e7a;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        sag_layout.addWidget(self.police_table)
        
        splitter.addWidget(sag_widget)
        
        # Splitter oranları (40% form, 60% liste)
        splitter.setSizes([400, 600])
        
        # İlk açılışta listeyi doldur
        self.tum_policeler = []  # Tüm poliçeleri sakla
        self.police_listesini_guncelle()
    
    def setup_yenilemeler_tab(self, tab):
        """Yenilemeler sekmesini oluştur"""
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Başlık ve filtre butonu
        baslik_widget = QWidget()
        baslik_layout = QHBoxLayout()
        baslik_widget.setLayout(baslik_layout)
        
        baslik = QLabel("🔔 Yenileme Takip Sistemi")
        baslik.setStyleSheet("""
            font-size: 16pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #bbdefb, stop:1 #90caf9);
            border-radius: 8px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        baslik_layout.addWidget(baslik)
        
        # Tarih değiştir butonu
        tarih_degistir_btn = QPushButton("⚙️ Tarih Değiştir")
        tarih_degistir_btn.clicked.connect(self.tarih_filtre_ac)
        tarih_degistir_btn.setMaximumWidth(150)
        tarih_degistir_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1976d2, stop:1 #1565c0);
                color: white;
                font-size: 11pt;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1565c0, stop:1 #0d47a1);
            }
        """)
        baslik_layout.addWidget(tarih_degistir_btn)
        
        layout.addWidget(baslik_widget)
        
        # FİLTRE BÖLÜMÜ
        filtre_widget = QWidget()
        filtre_layout = QHBoxLayout()
        filtre_widget.setLayout(filtre_layout)
        
        # Arama kutusu
        filtre_label = QLabel("🔍 Ara:")
        filtre_label.setStyleSheet("font-weight: bold; color: #37474f;")
        filtre_layout.addWidget(filtre_label)
        
        self.yenileme_arama_input = QLineEdit()
        self.yenileme_arama_input.setPlaceholderText("Müşteri adı, poliçe no veya telefon ara...")
        self.yenileme_arama_input.textChanged.connect(self.yenileme_filtrele)
        filtre_layout.addWidget(self.yenileme_arama_input)
        
        # Poliçe türü filtresi
        filtre_layout.addWidget(QLabel("Poliçe Türü:"))
        self.yenileme_tur_combo = QComboBox()
        self.yenileme_tur_combo.addItems([
            "Tümü", "Kasko", "Trafik", "Konut", "İşyeri", 
            "Sağlık", "Hayat", "Dask", "Seyahat", "Ferdi Kaza"
        ])
        self.yenileme_tur_combo.currentTextChanged.connect(self.yenileme_filtrele)
        filtre_layout.addWidget(self.yenileme_tur_combo)
        
        # Şirket filtresi
        filtre_layout.addWidget(QLabel("Şirket:"))
        self.yenileme_sirket_combo = QComboBox()
        self.yenileme_sirket_combo.addItems([
            "Tümü", "Anadolu Sigorta", "Allianz", "AXA Sigorta", 
            "HDI Sigorta", "Mapfre Sigorta", "Türk Nippon", 
            "Aksigorta", "Groupama", "Ziraat Sigorta", "Halk Sigorta"
        ])
        self.yenileme_sirket_combo.currentTextChanged.connect(self.yenileme_filtrele)
        filtre_layout.addWidget(self.yenileme_sirket_combo)
        
        # Durum filtresi
        filtre_layout.addWidget(QLabel("Durum:"))
        self.yenileme_durum_combo = QComboBox()
        self.yenileme_durum_combo.addItems([
            "Tümü", "🔴 Acil", "🟡 Yakın", "🟢 Normal"
        ])
        self.yenileme_durum_combo.currentTextChanged.connect(self.yenileme_filtrele)
        filtre_layout.addWidget(self.yenileme_durum_combo)
        
        # Temizle butonu
        yenileme_temizle_btn = QPushButton("🔄 Temizle")
        yenileme_temizle_btn.clicked.connect(self.yenileme_filtreleri_temizle)
        yenileme_temizle_btn.setStyleSheet("""
            QPushButton {
                background: #78909c;
                padding: 8px 15px;
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #546e7a;
            }
        """)
        filtre_layout.addWidget(yenileme_temizle_btn)
        
        layout.addWidget(filtre_widget)
        
        # Yenileme tablosu
        self.yenileme_table = QTableWidget()
        self.yenileme_table.setColumnCount(10)
        self.yenileme_table.setHorizontalHeaderLabels([
            "Durum", "Müşteri", "Telefon", "Poliçe No", "Tür", 
            "Şirket", "Bitiş Tarihi", "Kalan Gün", "Satışçı", "Takip Durumu"
        ])
        
        # Tablo stil ayarları
        self.yenileme_table.setAlternatingRowColors(True)
        self.yenileme_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.yenileme_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.yenileme_table.verticalHeader().setVisible(False)
        
        # Çift tıklama - poliçe detayına git
        self.yenileme_table.itemDoubleClicked.connect(self.yenileme_detay_ac)
        
        # Header ayarları
        header = self.yenileme_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionsMovable(True)
        
        self.yenileme_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #78909c;
                border-radius: 5px;
                gridline-color: #cfd8dc;
            }
            QTableWidget::item {
                padding: 8px;
                color: #000000;
            }
            QTableWidget::item:selected {
                background-color: #64b5f6;
                color: #000000;
                border: 2px solid #1976d2;
            }
            QTableWidget::item:hover {
                background-color: rgba(100, 181, 246, 0.3);
            }
            QHeaderView::section {
                background-color: #546e7a;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.yenileme_table)
        
        # Varsayılan filtre değerleri
        self.kalan_gun_limiti = 18
        self.gecen_gun_limiti = 5
        self.tum_yenilemeler = []  # Tüm yenilemeleri sakla
        
        # İlk yükleme
        self.yenilemeleri_yukle()
    
    def tarih_filtre_ac(self):
        """Tarih filtre dialog'unu aç"""
        dialog = TarihFiltreDialog(self, self.kalan_gun_limiti, self.gecen_gun_limiti)
        if dialog.exec():
            # Dialog'dan dönen değerleri al
            self.kalan_gun_limiti = dialog.kalan_gun
            self.gecen_gun_limiti = dialog.gecen_gun
            # Listeyi güncelle
            self.yenilemeleri_yukle()
    
    def yenilemeleri_yukle(self):
        """Yenileme listesini yükle"""
        from datetime import datetime, timedelta
        
        # Filtre değerlerini kullan
        kalan_gun_limiti = self.kalan_gun_limiti
        gecen_gun_limiti = self.gecen_gun_limiti
        
        # Bugünün tarihi
        bugun = datetime.now().date()
        
        # Tarih aralığı hesapla
        # Geçmişe gecen_gun_limiti kadar git
        baslangic_tarih = bugun - timedelta(days=gecen_gun_limiti)
        # Geleceğe kalan_gun_limiti kadar git
        bitis_tarih = bugun + timedelta(days=kalan_gun_limiti)
        
        # Veritabanından çek (Supabase ile)
        policeler = self.db.yenileme_policeleri_getir(
            baslangic_tarih.strftime("%Y-%m-%d"),
            bitis_tarih.strftime("%Y-%m-%d")
        )
        
        # Tüm yenilemeler listesini sakla (filtreleme için)
        self.tum_yenilemeler = []
        for police in policeler:
            bitis_str = police[5]
            bitis_tarih = datetime.strptime(bitis_str, "%Y-%m-%d").date()
            kalan_gun = (bitis_tarih - bugun).days
            
            # Durum belirle
            if kalan_gun <= 30:
                durum = "acil"
            elif kalan_gun <= 60:
                durum = "yakin"
            else:
                durum = "normal"
            
            # Tuple'a ekle (8 police verisi + kalan_gun + durum)
            self.tum_yenilemeler.append(police + (kalan_gun, durum))
        
        # Filtrelenmiş listeyi göster
        self.yenileme_tabloya_yukle(self.tum_yenilemeler)
    
    def yenileme_tabloya_yukle(self, yenilemeler):
        """Yenilemeleri tabloya yükle"""
        from datetime import datetime
        
        # Bugünün tarihi
        bugun = datetime.now().date()
        
        # Tabloyu temizle
        self.yenileme_table.setRowCount(0)
        
        # Tabloya ekle
        for row_idx, yenileme_data in enumerate(yenilemeler):
            # İlk 8 eleman police bilgileri (7 eski + 1 yenileme_durumu), sonraki 2 kalan_gun ve durum
            police = yenileme_data[:8]
            kalan_gun = yenileme_data[8]
            yenileme_durumu = police[7]  # yenileme_durumu son police bilgisi
            
            self.yenileme_table.insertRow(row_idx)
            
            # Bitiş tarihini parse et
            bitis_str = police[5]
            bitis_tarih = datetime.strptime(bitis_str, "%Y-%m-%d").date()
            
            # Satır rengini yenileme durumuna göre belirle - Daha canlı renkler
            if yenileme_durumu == "Poliçeleşti":
                satir_renk = "#a5d6a7"  # Daha canlı yeşil
                yazi_renk = "#000000"
            elif yenileme_durumu == "Olumsuz":
                satir_renk = "#ef9a9a"  # Daha canlı kırmızı
                yazi_renk = "#000000"
            else:  # Süreç devam ediyor
                satir_renk = "#ffcc80"  # Daha canlı turuncu
                yazi_renk = "#000000"
            
            # Durum ikonu (acillik durumu için)
            # Durum ikonu (acillik durumu için)
            if kalan_gun <= 30:
                durum = "🔴"
            elif kalan_gun <= 60:
                durum = "🟡"
            else:
                durum = "🟢"
            
            # Durum
            durum_item = QTableWidgetItem(durum)
            durum_item.setTextAlignment(Qt.AlignCenter)
            durum_item.setBackground(QColor(satir_renk))
            durum_item.setForeground(QColor(yazi_renk))
            self.yenileme_table.setItem(row_idx, 0, durum_item)
            
            # Müşteri
            item = QTableWidgetItem(police[0])
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(satir_renk))
            item.setForeground(QColor(yazi_renk))
            self.yenileme_table.setItem(row_idx, 1, item)
            
            # Telefon
            item = QTableWidgetItem(police[1] or "-")
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(satir_renk))
            item.setForeground(QColor(yazi_renk))
            self.yenileme_table.setItem(row_idx, 2, item)
            
            # Poliçe No
            item = QTableWidgetItem(police[2])
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(satir_renk))
            item.setForeground(QColor(yazi_renk))
            self.yenileme_table.setItem(row_idx, 3, item)
            
            # Tür
            item = QTableWidgetItem(police[3])
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(satir_renk))
            item.setForeground(QColor(yazi_renk))
            self.yenileme_table.setItem(row_idx, 4, item)
            
            # Şirket
            item = QTableWidgetItem(police[4])
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(satir_renk))
            item.setForeground(QColor(yazi_renk))
            self.yenileme_table.setItem(row_idx, 5, item)
            
            # Bitiş tarihi
            tarih_str = bitis_tarih.strftime("%d.%m.%Y")
            item = QTableWidgetItem(tarih_str)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(satir_renk))
            item.setForeground(QColor(yazi_renk))
            self.yenileme_table.setItem(row_idx, 6, item)
            
            # Kalan gün
            kalan_text = f"{kalan_gun} gün"
            if kalan_gun == 0:
                kalan_text = "⚠️ BUGÜN!"
            elif kalan_gun < 0:
                kalan_text = f"❌ {abs(kalan_gun)} gün GEÇTİ!"
            
            item = QTableWidgetItem(kalan_text)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(satir_renk))
            item.setForeground(QColor(yazi_renk))
            if kalan_gun <= 7:
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            self.yenileme_table.setItem(row_idx, 7, item)
            
            # Satışçı
            item = QTableWidgetItem(police[6])
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(satir_renk))
            item.setForeground(QColor(yazi_renk))
            self.yenileme_table.setItem(row_idx, 8, item)
            
            # Takip Durumu Dropdown
            durum_combo = QComboBox()
            durum_combo.addItems(["Süreç devam ediyor", "Poliçeleşti", "Olumsuz"])
            durum_combo.setCurrentText(yenileme_durumu)
            
            # Dropdown'un rengini duruma göre ayarla
            if yenileme_durumu == "Poliçeleşti":
                combo_renk = "#a5d6a7"  # Yeşil
            elif yenileme_durumu == "Olumsuz":
                combo_renk = "#ef9a9a"  # Kırmızı
            else:  # Süreç devam ediyor
                combo_renk = "#ffcc80"  # Turuncu
            
            durum_combo.setStyleSheet(f"""
                QComboBox {{
                    padding: 8px;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                    background-color: {combo_renk};
                    color: #263238;
                }}
                QComboBox:hover {{
                    background-color: {combo_renk};
                    opacity: 0.9;
                }}
                QComboBox::drop-down {{
                    border: none;
                    padding-right: 5px;
                }}
                QComboBox QAbstractItemView {{
                    background-color: white;
                    selection-background-color: #1976d2;
                    selection-color: white;
                    border: 2px solid #1976d2;
                }}
            """)
            
            # Police no'yu data olarak sakla
            durum_combo.setProperty("police_no", police[2])
            durum_combo.currentTextChanged.connect(self.yenileme_durum_degisti)
            
            self.yenileme_table.setCellWidget(row_idx, 9, durum_combo)
        
        self.yenileme_table.resizeRowsToContents()
    
    def yenileme_durum_degisti(self, yeni_durum):
        """Yenileme durumu değiştiğinde çağrılır"""
        # ComboBox'ı bul
        combo = self.sender()
        police_no = combo.property("police_no")
        
        # Veritabanını güncelle
        success, message = self.db.yenileme_durumu_guncelle(police_no, yeni_durum)
        
        if success:
            # Listeyi yenile (renkleri güncelle)
            self.yenilemeleri_yukle()
        else:
            QMessageBox.warning(self, "Hata", message)
    
    def yenileme_filtrele(self):
        """Yenileme listesini filtrele"""
        arama_metni = self.yenileme_arama_input.text().lower()
        tur_filtre = self.yenileme_tur_combo.currentText()
        sirket_filtre = self.yenileme_sirket_combo.currentText()
        durum_filtre = self.yenileme_durum_combo.currentText()
        
        # Filtreleme yap
        filtrelenmis = []
        for yenileme in self.tum_yenilemeler:
            police = yenileme[:8]  # İlk 8 eleman police bilgileri (7 eski + yenileme_durumu)
            durum = yenileme[9]    # Son eleman acillik durumu
            
            # Arama metni kontrolü (müşteri, telefon, poliçe no)
            arama_uygun = True
            if arama_metni:
                musteri = str(police[0]).lower()
                telefon = str(police[1]).lower() if police[1] else ""
                police_no = str(police[2]).lower()
                arama_uygun = (arama_metni in musteri or 
                              arama_metni in telefon or 
                              arama_metni in police_no)
            
            # Tür filtresi kontrolü
            tur_uygun = (tur_filtre == "Tümü" or police[3] == tur_filtre)
            
            # Şirket filtresi kontrolü
            sirket_uygun = (sirket_filtre == "Tümü" or police[4] == sirket_filtre)
            
            # Durum filtresi kontrolü
            durum_uygun = True
            if durum_filtre == "🔴 Acil":
                durum_uygun = (durum == "acil")
            elif durum_filtre == "🟡 Yakın":
                durum_uygun = (durum == "yakin")
            elif durum_filtre == "🟢 Normal":
                durum_uygun = (durum == "normal")
            
            # Tüm koşullar sağlanıyorsa ekle
            if arama_uygun and tur_uygun and sirket_uygun and durum_uygun:
                filtrelenmis.append(yenileme)
        
        # Filtrelenmiş listeyi tabloya yükle
        self.yenileme_tabloya_yukle(filtrelenmis)
    
    def yenileme_filtreleri_temizle(self):
        """Tüm yenileme filtrelerini temizle"""
        self.yenileme_arama_input.clear()
        self.yenileme_tur_combo.setCurrentIndex(0)
        self.yenileme_sirket_combo.setCurrentIndex(0)
        self.yenileme_durum_combo.setCurrentIndex(0)
        self.yenileme_tabloya_yukle(self.tum_yenilemeler)
    
    def yenileme_detay_ac(self, item):
        """Yenileme tablosundan poliçe detayını aç"""
        row = item.row()
        police_no = self.yenileme_table.item(row, 3).text()
        
        # Detay penceresini aç
        dialog = PoliceDetayDialog(self, police_no, self.db)
        if dialog.exec():
            # Dialog kapandığında tüm listeleri güncelle
            self.tum_listeleri_guncelle()
    
    def setup_raporlar_tab(self, tab):
        """Raporlar sekmesini oluştur"""
        # Ana layout
        main_layout = QHBoxLayout()
        tab.setLayout(main_layout)
        
        # Splitter ile sol ve sağ bölüm
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # SOL TARAF - FİLTRELER
        sol_widget = QWidget()
        sol_layout = QVBoxLayout()
        sol_widget.setLayout(sol_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(sol_widget)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        splitter.addWidget(scroll)
        
        # Başlık
        baslik = QLabel("🔍 Filtreler")
        baslik.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 10px;
            background-color: #bbdefb;
            border-radius: 5px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        sol_layout.addWidget(baslik)
        
        # Filtre formu
        form = QFormLayout()
        
        # Tarih filtre seçimi
        tarih_label = QLabel("📅 Tarih Filtresi:")
        tarih_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        form.addRow(tarih_label)
        
        self.rapor_tarih_tip_combo = QComboBox()
        self.rapor_tarih_tip_combo.addItems(["Tanzim Tarihi", "Poliçe Başlangıç Tarihi", "Poliçe Bitiş Tarihi"])
        form.addRow("Filtre Türü:", self.rapor_tarih_tip_combo)
        
        self.rapor_tarih_baslangic = QDateEdit()
        self.rapor_tarih_baslangic.setCalendarPopup(True)
        self.rapor_tarih_baslangic.setDate(QDate.currentDate().addMonths(-1))
        self.rapor_tarih_baslangic.setDisplayFormat("dd.MM.yyyy")
        form.addRow("Başlangıç:", self.rapor_tarih_baslangic)
        
        self.rapor_tarih_bitis = QDateEdit()
        self.rapor_tarih_bitis.setCalendarPopup(True)
        self.rapor_tarih_bitis.setDate(QDate.currentDate())
        self.rapor_tarih_bitis.setDisplayFormat("dd.MM.yyyy")
        form.addRow("Bitiş:", self.rapor_tarih_bitis)
        
        # Müşteri
        musteri_label = QLabel("👤 Müşteri:")
        musteri_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        form.addRow(musteri_label)
        
        self.rapor_musteri_input = QLineEdit()
        form.addRow(self.rapor_musteri_input)
        
        # Satışçı
        satisci_label = QLabel("👨‍💼 Satışçı:")
        satisci_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        form.addRow(satisci_label)
        
        self.rapor_satisci_combo = QComboBox()
        self.rapor_satisci_combo.addItem("Tümü")
        satiscilar = self.db.satiscilari_getir()
        for satisci_id, ad_soyad in satiscilar:
            self.rapor_satisci_combo.addItem(ad_soyad, satisci_id)
        form.addRow(self.rapor_satisci_combo)
        
        # Poliçe türü
        tur_label = QLabel("📋 Poliçe Türü:")
        tur_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        form.addRow(tur_label)
        
        self.rapor_tur_combo = QComboBox()
        self.rapor_tur_combo.addItems([
            "Tümü", "Kasko", "Trafik", "Konut", "İşyeri", 
            "Sağlık", "Hayat", "Dask", "Seyahat", "Ferdi Kaza"
        ])
        form.addRow(self.rapor_tur_combo)
        
        # Şirket
        sirket_label = QLabel("🏢 Şirket:")
        sirket_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        form.addRow(sirket_label)
        
        self.rapor_sirket_combo = QComboBox()
        self.rapor_sirket_combo.addItems([
            "Tümü", "Anadolu Sigorta", "Allianz", "AXA Sigorta", 
            "HDI Sigorta", "Mapfre Sigorta", "Türk Nippon", 
            "Aksigorta", "Groupama", "Ziraat Sigorta", "Halk Sigorta"
        ])
        form.addRow(self.rapor_sirket_combo)
        
        sol_layout.addLayout(form)
        
        # Butonlar
        rapor_olustur_btn = QPushButton("📊 RAPOR OLUŞTUR")
        rapor_olustur_btn.clicked.connect(self.rapor_olustur)
        rapor_olustur_btn.setMinimumHeight(50)
        rapor_olustur_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1976d2, stop:1 #1565c0);
                color: white;
                font-size: 12pt;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1565c0, stop:1 #0d47a1);
            }
        """)
        sol_layout.addWidget(rapor_olustur_btn)
        
        temizle_btn = QPushButton("🔄 Temizle")
        temizle_btn.clicked.connect(self.rapor_filtreleri_temizle)
        temizle_btn.setStyleSheet("""
            QPushButton {
                background: #78909c;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: #546e7a;
            }
        """)
        sol_layout.addWidget(temizle_btn)
        sol_layout.addStretch()
        
        # SAĞ TARAF - RAPOR SONUÇLARI
        sag_widget = QWidget()
        sag_layout = QVBoxLayout()
        sag_widget.setLayout(sag_layout)
        
        # Başlık
        rapor_baslik = QLabel("📊 Rapor Sonuçları")
        rapor_baslik.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 10px;
            background-color: #bbdefb;
            border-radius: 5px;
        """)
        rapor_baslik.setAlignment(Qt.AlignCenter)
        sag_layout.addWidget(rapor_baslik)
        
        # ÖZET BİLGİLER (Kompakt)
        ozet_layout = QHBoxLayout()
        
        # Toplam Poliçe
        self.ozet_adet = QLabel("0")
        ozet_adet_box = self.create_ozet_box_compact("📝", self.ozet_adet, "#e3f2fd")
        ozet_layout.addWidget(ozet_adet_box)
        
        # Toplam Prim
        self.ozet_prim = QLabel("0 ₺")
        ozet_prim_box = self.create_ozet_box_compact("💰", self.ozet_prim, "#fff9c4")
        ozet_layout.addWidget(ozet_prim_box)
        
        # Toplam Komisyon
        self.ozet_komisyon = QLabel("0 ₺")
        ozet_komisyon_box = self.create_ozet_box_compact("💵", self.ozet_komisyon, "#c8e6c9")
        ozet_layout.addWidget(ozet_komisyon_box)
        
        sag_layout.addLayout(ozet_layout)
        
        # RAPOR TABLOSU
        self.rapor_table = QTableWidget()
        self.rapor_table.setColumnCount(10)
        self.rapor_table.setHorizontalHeaderLabels([
            "Tanzim", "Müşteri", "Poliçe No", "Tür", "Şirket",
            "Başlangıç", "Bitiş", "Prim (₺)", "Komisyon (₺)", "Satışçı"
        ])
        
        # Tablo ayarları
        self.rapor_table.setAlternatingRowColors(True)
        self.rapor_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.rapor_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.rapor_table.verticalHeader().setVisible(False)
        
        # Çift tıklama
        self.rapor_table.itemDoubleClicked.connect(self.rapor_detay_ac)
        
        # Header
        header = self.rapor_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionsMovable(True)
        
        self.rapor_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #78909c;
                border-radius: 5px;
                gridline-color: #cfd8dc;
            }
            QTableWidget::item {
                padding: 5px;
                color: #000000;
            }
            QTableWidget::item:selected {
                background-color: #64b5f6;
                color: #000000;
                border: 2px solid #1976d2;
            }
            QTableWidget::item:hover {
                background-color: rgba(100, 181, 246, 0.3);
            }
            QHeaderView::section {
                background-color: #546e7a;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        sag_layout.addWidget(self.rapor_table)
        splitter.addWidget(sag_widget)
        
        # Splitter oranları (30% filtre, 70% rapor)
        splitter.setSizes([300, 700])
    
    def create_ozet_box_compact(self, icon, label_widget, renk):
        """Kompakt özet bilgi kutusu"""
        box = QWidget()
        box_layout = QVBoxLayout()
        box.setLayout(box_layout)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 18pt;")
        icon_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(icon_label)
        
        label_widget.setStyleSheet(f"""
            font-size: 14pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 2px;
        """)
        label_widget.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(label_widget)
        
        # Açıklama metni
        if icon == "📝":
            aciklama = "Toplam Poliçe"
        elif icon == "💰":
            aciklama = "Toplam Prim"
        else:
            aciklama = "Toplam Komisyon"
        
        aciklama_label = QLabel(aciklama)
        aciklama_label.setStyleSheet("font-size: 9pt; color: #546e7a;")
        aciklama_label.setAlignment(Qt.AlignCenter)
        box_layout.addWidget(aciklama_label)
        
        box.setStyleSheet(f"""
            QWidget {{
                background-color: {renk};
                border: 2px solid #1976d2;
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        return box
    
    def rapor_olustur(self):
        """Rapor oluştur"""
        # Filtreleri al
        tarih_tip = self.rapor_tarih_tip_combo.currentText()
        tarih_baslangic = self.rapor_tarih_baslangic.date().toString("yyyy-MM-dd")
        tarih_bitis = self.rapor_tarih_bitis.date().toString("yyyy-MM-dd")
        musteri_ara = self.rapor_musteri_input.text().strip().lower()
        satisci_filtre = self.rapor_satisci_combo.currentText()
        tur_filtre = self.rapor_tur_combo.currentText()
        sirket_filtre = self.rapor_sirket_combo.currentText()
        
        # Tüm poliçeleri çek
        policeler = self.db.police_listesi_getir()
        
        # Filtreleme
        filtered_policeler = []
        for p in policeler:
            # p formatı: (musteri_ad, police_no, sigorta_turu, sirket, baslangic, bitis, prim, komisyon, satisci)
            musteri_ad, police_no, sigorta_turu, sirket, baslangic, bitis, prim, komisyon, satisci = p
            
            # Müşteri filtresi
            if musteri_ara and musteri_ara not in musteri_ad.lower():
                continue
            
            # Satışçı filtresi
            if satisci_filtre != "Tümü" and satisci != satisci_filtre:
                continue
            
            # Tür filtresi
            if tur_filtre != "Tümü" and sigorta_turu != tur_filtre:
                continue
            
            # Şirket filtresi
            if sirket_filtre != "Tümü" and sirket != sirket_filtre:
                continue
            
            # Tarih filtresi
            if tarih_tip == "Poliçe Başlangıç Tarihi":
                if not (tarih_baslangic <= baslangic <= tarih_bitis):
                    continue
            elif tarih_tip == "Poliçe Bitiş Tarihi":
                if not (tarih_baslangic <= bitis <= tarih_bitis):
                    continue
            # Tanzim tarihi filtresini şimdilik atlıyoruz (police_listesi_getir'de yok)
            
            # Tuple'ı rapor formatına çevir (kayit_tarihi placeholder olarak baslangic kullanılıyor)
            filtered_policeler.append((
                baslangic,  # kayit_tarihi yerine
                musteri_ad,
                police_no,
                sigorta_turu,
                sirket,
                baslangic,
                bitis,
                prim,
                komisyon,
                satisci
            ))
        
        policeler = filtered_policeler
        
        # Tabloyu temizle
        self.rapor_table.setRowCount(0)
        
        # Özet hesapla
        toplam_adet = len(policeler)
        toplam_prim = sum(p[7] for p in policeler if p[7])
        toplam_komisyon = sum(p[8] for p in policeler if p[8])
        
        # Özet bilgileri güncelle
        self.ozet_adet.setText(str(toplam_adet))
        self.ozet_prim.setText(f"{toplam_prim:,.2f} ₺")
        self.ozet_komisyon.setText(f"{toplam_komisyon:,.2f} ₺")
        
        # Tabloya ekle
        for row_idx, police in enumerate(policeler):
            self.rapor_table.insertRow(row_idx)
            
            for col_idx, value in enumerate(police):
                # Tarihleri formatla
                if col_idx in [0, 5, 6] and value:
                    try:
                        if col_idx == 0:  # Kayıt tarihi (timestamp)
                            tarih = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                        else:  # Diğer tarihler
                            tarih = datetime.strptime(value, "%Y-%m-%d")
                        value = tarih.strftime("%d.%m.%Y")
                    except:
                        pass
                
                # Tutarları formatla
                if col_idx in [7, 8] and value:
                    value = f"{float(value):,.2f}"
                
                item = QTableWidgetItem(str(value) if value else "-")
                item.setTextAlignment(Qt.AlignCenter)
                self.rapor_table.setItem(row_idx, col_idx, item)
        
        self.rapor_table.resizeRowsToContents()
    
    def rapor_filtreleri_temizle(self):
        """Rapor filtrelerini temizle"""
        self.rapor_tarih_tip_combo.setCurrentIndex(0)
        self.rapor_tarih_baslangic.setDate(QDate.currentDate().addMonths(-1))
        self.rapor_tarih_bitis.setDate(QDate.currentDate())
        self.rapor_musteri_input.clear()
        self.rapor_satisci_combo.setCurrentIndex(0)
        self.rapor_tur_combo.setCurrentIndex(0)
        self.rapor_sirket_combo.setCurrentIndex(0)
        self.rapor_table.setRowCount(0)
        self.ozet_adet.setText("0")
        self.ozet_prim.setText("0 ₺")
        self.ozet_komisyon.setText("0 ₺")
    
    def rapor_detay_ac(self, item):
        """Rapor tablosundan poliçe detayını aç"""
        row = item.row()
        police_no = self.rapor_table.item(row, 2).text()
        
        # Detay penceresini aç
        dialog = PoliceDetayDialog(self, police_no, self.db)
        if dialog.exec():
            # Dialog kapandığında tüm listeleri güncelle
            self.tum_listeleri_guncelle()
            # Eğer rapor sekmesi aktifse raporu da güncelle
            if hasattr(self, 'rapor_table') and self.rapor_table.isVisible():
                self.rapor_olustur()
    
    def satiscilari_yukle(self):
        """Satışçıları combo box'a yükle"""
        self.satisci_combo.clear()
        satiscilar = self.db.satiscilari_getir()
        for satisci_id, ad_soyad in satiscilar:
            self.satisci_combo.addItem(ad_soyad, satisci_id)
    
    def baslangic_tarihi_degisti(self, tarih):
        """Başlangıç tarihi değiştiğinde bitiş tarihini otomatik ayarla"""
        # Bitiş tarihini 1 yıl sonraya ayarla
        self.bitis_tarihi.setDate(tarih.addYears(1))
    
    def kaydet(self):
        """Müşteri ve poliçe bilgilerini kaydet"""
        # Müşteri bilgilerini al
        ad_soyad = self.ad_soyad_input.text().strip()
        tc_no = self.tc_no_input.text().strip()
        telefon = self.telefon_input.text().strip()
        email = self.email_input.text().strip()
        adres = ""  # Adres kaldırıldı
        
        # Poliçe bilgilerini al
        police_no = self.police_no_input.text().strip()
        sigorta_turu = self.sigorta_turu_combo.currentText()
        sirket = self.sirket_combo.currentText()
        baslangic = self.baslangic_tarihi.date().toString("yyyy-MM-dd")
        bitis = self.bitis_tarihi.date().toString("yyyy-MM-dd")
        prim_tutari = self.prim_tutari_input.text().strip()
        aciklama = self.aciklama_input.toPlainText().strip()
        
        # Validasyon
        if not ad_soyad:
            QMessageBox.warning(self, "Uyarı", "Lütfen müşteri adı soyadı giriniz!")
            return
        
        if not tc_no or len(tc_no) != 11:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir TC No giriniz!")
            return
        
        if not police_no:
            QMessageBox.warning(self, "Uyarı", "Lütfen poliçe numarası giriniz!")
            return
        
        if sigorta_turu == "Seçiniz":
            QMessageBox.warning(self, "Uyarı", "Lütfen sigorta türünü seçiniz!")
            return
        
        if sirket == "Seçiniz":
            QMessageBox.warning(self, "Uyarı", "Lütfen sigorta şirketini seçiniz!")
            return
        
        # Önce müşteriyi ekle
        success, message = self.db.musteri_ekle(ad_soyad, tc_no, telefon, email, adres)
        
        if not success and "zaten kayıtlı" not in message:
            QMessageBox.critical(self, "Hata", message)
            return
        
        # Müşteri ID'sini al (Supabase ile)
        musteriler = self.db.musterileri_getir()
        musteri_id = None
        for m in musteriler:
            if m[2] == tc_no:  # tc_no index 2'de
                musteri_id = m[0]  # id index 0'da
                break
        
        if not musteri_id:
            QMessageBox.critical(self, "Hata", "Müşteri ID alınamadı!")
            return
        
        # Poliçeyi ekle
        try:
            prim = float(prim_tutari) if prim_tutari else 0.0
            # Komisyon otomatik hesaplama (prim tutarının %15'i)
            komisyon = prim * 0.15
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli tutar giriniz!")
            return
        
        # Satışçı ID'sini al
        satisci_id = self.satisci_combo.currentData()
        
        # Ödeme şeklini al
        odeme_sekli = self.odeme_sekli_combo.currentText()
        
        success, message = self.db.police_ekle(
            musteri_id, police_no, sigorta_turu, sirket,
            baslangic, bitis, prim, komisyon, aciklama, satisci_id, odeme_sekli
        )
        
        if success:
            QMessageBox.information(self, "Başarılı", "Müşteri ve poliçe başarıyla kaydedildi!")
            self.tum_listeleri_guncelle()  # Tüm listeleri güncelle
            self.formu_temizle()
        else:
            QMessageBox.critical(self, "Hata", message)
    
    def tum_listeleri_guncelle(self):
        """Tüm ekranlardaki listeleri güncelle (poliçe ekleme/silme/güncelleme sonrası)"""
        # Poliçe Giriş listesini güncelle
        self.police_listesini_guncelle()
        
        # Diğer tablardaki listeleri güncelle (eğer oluşturulduysa)
        if hasattr(self, 'yenileme_table'):
            self.yenilemeleri_yukle()
        
        if hasattr(self, 'finans_table'):
            self.finans_listesini_yukle()
        
        if hasattr(self, 'capraz_satis_table'):
            self.capraz_satis_listesini_yukle()
    
    def police_listesini_guncelle(self):
        """Poliçe listesini veritabanından çek ve tabloya yükle"""
        # Supabase'den poliçeleri çek
        self.tum_policeler = self.db.police_listesi_getir()
        self.tabloya_yukle(self.tum_policeler)

    
    def tabloya_yukle(self, policeler):
        """Poliçeleri tabloya yükle"""
        from datetime import datetime
        
        # Önce tabloyu temizle
        self.police_table.setRowCount(0)
        
        # Bugünün tarihi
        bugun = datetime.now().date()
        
        # Tabloya ekle
        for row_idx, police in enumerate(policeler):
            self.police_table.insertRow(row_idx)
            
            # Bitiş tarihini kontrol et (index 5)
            bitis_str = police[5]
            try:
                bitis_tarih = datetime.strptime(bitis_str, "%Y-%m-%d").date()
                kalan_gun = (bitis_tarih - bugun).days
                
                # Satır rengini kalan güne göre belirle - Daha canlı renkler
                if kalan_gun < 0:
                    satir_renk = "#ff8a80"  # Daha canlı kırmızı - Süresi geçmiş
                    yazi_renk = "#000000"  # Siyah yazı
                elif kalan_gun <= 30:
                    satir_renk = "#ffab91"  # Daha canlı turuncu - Acil
                    yazi_renk = "#000000"  # Siyah yazı
                elif kalan_gun <= 60:
                    satir_renk = "#fff59d"  # Daha canlı sarı - Yakın
                    yazi_renk = "#000000"  # Siyah yazı
                else:
                    satir_renk = "#ffffff"  # Beyaz - Normal
                    yazi_renk = "#000000"  # Siyah yazı
            except:
                satir_renk = "#ffffff"  # Hata durumunda beyaz
                yazi_renk = "#000000"
            
            for col_idx, value in enumerate(police):
                # Tarihleri formatla
                if col_idx in [4, 5] and value:  # Tarih kolonları
                    try:
                        tarih = datetime.strptime(value, "%Y-%m-%d")
                        value = tarih.strftime("%d.%m.%Y")
                    except:
                        pass
                
                # Tutarları formatla (Prim ve Komisyon)
                if col_idx in [6, 7] and value:  # Prim ve Komisyon tutarları
                    value = f"{float(value):,.2f}"
                
                item = QTableWidgetItem(str(value) if value else "-")
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(QColor(satir_renk))  # Arka plan rengini uygula
                item.setForeground(QColor(yazi_renk))  # Metin rengini uygula
                self.police_table.setItem(row_idx, col_idx, item)
        
        # Satır sayısını göster
        self.police_table.resizeRowsToContents()
    
    def police_filtrele(self):
        """Poliçeleri filtrele"""
        arama_metni = self.arama_input.text().lower()
        tur_filtre = self.filtre_tur_combo.currentText()
        sirket_filtre = self.filtre_sirket_combo.currentText()
        
        # Filtreleme yap
        filtrelenmis = []
        for police in self.tum_policeler:
            # Arama metni kontrolü (müşteri, poliçe no, şirket)
            arama_uygun = True
            if arama_metni:
                musteri = str(police[0]).lower()
                police_no = str(police[1]).lower()
                sirket = str(police[3]).lower()
                arama_uygun = (arama_metni in musteri or 
                              arama_metni in police_no or 
                              arama_metni in sirket)
            
            # Tür filtresi kontrolü
            tur_uygun = (tur_filtre == "Tümü" or police[2] == tur_filtre)
            
            # Şirket filtresi kontrolü
            sirket_uygun = (sirket_filtre == "Tümü" or police[3] == sirket_filtre)
            
            # Tüm koşullar sağlanıyorsa ekle
            if arama_uygun and tur_uygun and sirket_uygun:
                filtrelenmis.append(police)
        
        # Filtrelenmiş listeyi tabloya yükle
        self.tabloya_yukle(filtrelenmis)
    
    def filtreleri_temizle(self):
        """Tüm filtreleri temizle"""
        self.arama_input.clear()
        self.filtre_tur_combo.setCurrentIndex(0)
        self.filtre_sirket_combo.setCurrentIndex(0)
        self.tabloya_yukle(self.tum_policeler)
    
    def formu_temizle(self):
        """Form alanlarını temizle"""
        self.ad_soyad_input.clear()
        self.tc_no_input.clear()
        self.telefon_input.clear()
        self.email_input.clear()
        self.police_no_input.clear()
        self.sigorta_turu_combo.setCurrentIndex(0)
        self.sirket_combo.setCurrentIndex(0)
        self.baslangic_tarihi.setDate(QDate.currentDate())
        self.bitis_tarihi.setDate(QDate.currentDate().addYears(1))
        self.prim_tutari_input.clear()
        self.aciklama_input.clear()
        self.odeme_sekli_combo.setCurrentIndex(0)
        self.satisci_combo.setCurrentIndex(0)
        self.ad_soyad_input.setFocus()
    
    def police_detay_ac(self, item):
        """Poliçe detay penceresini aç"""
        try:
            # Tıklanan satırın poliçe numarasını al
            row = item.row()
            police_no_item = self.police_table.item(row, 1)
            
            if not police_no_item:
                QMessageBox.warning(self, "Hata", "Poliçe bilgisi bulunamadı!")
                return
            
            police_no = police_no_item.text()
            
            if not police_no:
                QMessageBox.warning(self, "Hata", "Poliçe numarası bulunamadı!")
                return
            
            # Detay penceresini aç
            dialog = PoliceDetayDialog(self, police_no, self.db)
            if dialog.exec():
                # Dialog kapandığında tüm listeleri güncelle
                self.tum_listeleri_guncelle()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Poliçe detayı açılırken hata oluştu:\n{str(e)}")
    
    def setup_finans_tab(self, tab):
        """Finans sekmesini oluştur - Nakit ödeme borç takibi"""
        # Ana layout
        main_layout = QVBoxLayout()
        tab.setLayout(main_layout)
        
        # Başlık
        baslik = QLabel("💰 FİNANS - NAKİT BORÇ TAKİBİ")
        baslik.setStyleSheet("""
            font-size: 16pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 15px;
            background-color: #bbdefb;
            border-radius: 5px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(baslik)
        
        # Bilgi etiketi
        info_label = QLabel("Ödeme şekli 'Nakit' olan poliçeler aşağıda listelenir. "
                           "Çift tıklayarak borç durumunu güncelleyebilirsiniz.")
        info_label.setStyleSheet("""
            font-size: 10pt;
            color: #37474f;
            padding: 10px;
            background-color: #fff9c4;
            border-radius: 5px;
            border-left: 4px solid #fbc02d;
        """)
        info_label.setWordWrap(True)
        main_layout.addWidget(info_label)
        
        # Tablo
        self.finans_table = QTableWidget()
        self.finans_table.setColumnCount(10)
        self.finans_table.setHorizontalHeaderLabels([
            "Poliçe No", "Müşteri", "Telefon", "Tür", "Şirket",
            "Prim (TL)", "Borç (TL)", "Ödenen (TL)", "Kalan (TL)", "Tarih"
        ])
        
        # Tablo ayarları
        self.finans_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.finans_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.finans_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.finans_table.setAlternatingRowColors(True)
        self.finans_table.itemDoubleClicked.connect(self.finans_detay_ac)
        
        self.finans_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #cfd8dc;
                border: 2px solid #78909c;
                border-radius: 5px;
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 8px;
                color: #000000;
            }
            QTableWidget::item:selected {
                background-color: #64b5f6;
                color: #000000;
                border: 2px solid #1976d2;
            }
            QTableWidget::item:hover {
                background-color: rgba(100, 181, 246, 0.3);
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1976d2, stop:1 #1565c0);
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 10pt;
            }
        """)
        
        main_layout.addWidget(self.finans_table)
        
        # Yenile butonu
        yenile_layout = QHBoxLayout()
        yenile_btn = QPushButton("🔄 Listeyi Yenile")
        yenile_btn.clicked.connect(self.finans_listesini_yukle)
        yenile_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1976d2, stop:1 #1565c0);
                color: white;
                font-size: 11pt;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1565c0, stop:1 #0d47a1);
            }
        """)
        yenile_layout.addStretch()
        yenile_layout.addWidget(yenile_btn)
        yenile_layout.addStretch()
        main_layout.addLayout(yenile_layout)
        
        # İlk yükleme
        self.finans_listesini_yukle()
    
    def finans_listesini_yukle(self):
        """Nakit ödeme yapılan poliçeleri yükle"""
        policeler = self.db.nakit_policeleri_getir()
        
        self.finans_table.setRowCount(0)
        
        for police in policeler:
            row_position = self.finans_table.rowCount()
            self.finans_table.insertRow(row_position)
            
            police_id, police_no, musteri_adi, telefon, tur, sirket, prim, borc, odenen, kalan, tarih = police
            
            # Borc tutarını kontrol et (None ise prim tutarına eşitle)
            if borc is None:
                borc = prim
            if odenen is None:
                odenen = 0
            if kalan is None:
                kalan = borc - odenen
            
            # Poliçe ID'sini sakla (gizli kolon olarak)
            id_item = QTableWidgetItem(str(police_id))
            id_item.setData(Qt.UserRole, police_id)
            
            # Tabloya ekle
            self.finans_table.setItem(row_position, 0, QTableWidgetItem(police_no))
            self.finans_table.setItem(row_position, 1, QTableWidgetItem(musteri_adi or ""))
            self.finans_table.setItem(row_position, 2, QTableWidgetItem(telefon or ""))
            self.finans_table.setItem(row_position, 3, QTableWidgetItem(tur))
            self.finans_table.setItem(row_position, 4, QTableWidgetItem(sirket))
            self.finans_table.setItem(row_position, 5, QTableWidgetItem(f"{prim:,.2f}"))
            self.finans_table.setItem(row_position, 6, QTableWidgetItem(f"{borc:,.2f}"))
            self.finans_table.setItem(row_position, 7, QTableWidgetItem(f"{odenen:,.2f}"))
            
            # Kalan borç
            kalan_item = QTableWidgetItem(f"{kalan:,.2f}")
            if kalan > 0:
                kalan_item.setBackground(QColor("#ffcdd2"))  # Açık kırmızı
                kalan_item.setForeground(QColor("#b71c1c"))  # Koyu kırmızı
            else:
                kalan_item.setBackground(QColor("#c8e6c9"))  # Açık yeşil
                kalan_item.setForeground(QColor("#2e7d32"))  # Koyu yeşil
            self.finans_table.setItem(row_position, 8, kalan_item)
            
            # Tarih
            try:
                tarih_obj = datetime.strptime(tarih, "%Y-%m-%d %H:%M:%S")
                tarih_str = tarih_obj.strftime("%d.%m.%Y")
            except:
                tarih_str = tarih
            self.finans_table.setItem(row_position, 9, QTableWidgetItem(tarih_str))
            
            # Police ID'yi ilk hücrede sakla
            self.finans_table.item(row_position, 0).setData(Qt.UserRole, police_id)
    
    def finans_detay_ac(self, item):
        """Finans detay penceresini aç"""
        row = item.row()
        police_id = self.finans_table.item(row, 0).data(Qt.UserRole)
        
        dialog = FinansDetayDialog(self, police_id, self.db)
        if dialog.exec():
            # Dialog kapandığında listeyi güncelle
            self.finans_listesini_yukle()
    
    def setup_capraz_satis_tab(self, tab):
        """Çapraz satış sekmesini oluştur"""
        # Ana layout - Splitter ile üst ve alt bölüm
        main_layout = QVBoxLayout()
        tab.setLayout(main_layout)
        
        # Başlık
        baslik = QLabel("🔄 ÇAPRAZ SATIŞ ÖNERİLERİ")
        baslik.setStyleSheet("""
            font-size: 16pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 15px;
            background-color: #bbdefb;
            border-radius: 5px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(baslik)
        
        # Bilgi etiketi
        info_label = QLabel("Aşağıdaki listeden bir poliçe seçin, alt kısımda çapraz satış önerileri görüntülenecektir.")
        info_label.setStyleSheet("""
            font-size: 10pt;
            color: #37474f;
            padding: 10px;
            background-color: #fff9c4;
            border-radius: 5px;
            border-left: 4px solid #fbc02d;
        """)
        info_label.setWordWrap(True)
        main_layout.addWidget(info_label)
        
        # Splitter ile üst ve alt bölüm
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)
        
        # ÜST BÖLÜM - Poliçe Listesi
        ust_widget = QWidget()
        ust_layout = QVBoxLayout()
        ust_widget.setLayout(ust_layout)
        
        ust_baslik = QLabel("📋 Tüm Poliçeler")
        ust_baslik.setStyleSheet("""
            font-size: 12pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 8px;
            background-color: #e3f2fd;
            border-radius: 5px;
        """)
        ust_layout.addWidget(ust_baslik)
        
        self.capraz_satis_table = QTableWidget()
        self.capraz_satis_table.setColumnCount(8)
        self.capraz_satis_table.setHorizontalHeaderLabels([
            "Poliçe No", "Müşteri", "Telefon", "Tür", "Şirket",
            "Başlangıç", "Bitiş", "Prim (TL)"
        ])
        
        # Tablo ayarları
        self.capraz_satis_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.capraz_satis_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.capraz_satis_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.capraz_satis_table.setAlternatingRowColors(True)
        self.capraz_satis_table.itemSelectionChanged.connect(self.capraz_satis_police_secildi)
        
        self.capraz_satis_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #cfd8dc;
                border: 2px solid #78909c;
                border-radius: 5px;
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 8px;
                color: #000000;
            }
            QTableWidget::item:selected {
                background-color: #64b5f6;
                color: #000000;
                border: 2px solid #1976d2;
            }
            QTableWidget::item:hover {
                background-color: rgba(100, 181, 246, 0.3);
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1976d2, stop:1 #1565c0);
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 10pt;
            }
        """)
        
        ust_layout.addWidget(self.capraz_satis_table)
        splitter.addWidget(ust_widget)
        
        # ALT BÖLÜM - Çapraz Satış Önerileri
        alt_widget = QWidget()
        alt_layout = QVBoxLayout()
        alt_widget.setLayout(alt_layout)
        
        alt_baslik = QLabel("💡 Çapraz Satış Önerileri")
        alt_baslik.setStyleSheet("""
            font-size: 12pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 8px;
            background-color: #e3f2fd;
            border-radius: 5px;
        """)
        alt_layout.addWidget(alt_baslik)
        
        # Scroll area for öneriler
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.oneriler_widget = QWidget()
        self.oneriler_layout = QVBoxLayout()
        self.oneriler_widget.setLayout(self.oneriler_layout)
        
        # İlk mesaj
        self.oneri_mesaj_label = QLabel("Lütfen yukarıdan bir poliçe seçin...")
        self.oneri_mesaj_label.setStyleSheet("""
            font-size: 11pt;
            color: #78909c;
            padding: 30px;
            text-align: center;
        """)
        self.oneri_mesaj_label.setAlignment(Qt.AlignCenter)
        self.oneriler_layout.addWidget(self.oneri_mesaj_label)
        self.oneriler_layout.addStretch()
        
        scroll_area.setWidget(self.oneriler_widget)
        alt_layout.addWidget(scroll_area)
        
        splitter.addWidget(alt_widget)
        
        # Splitter oranları (üst %60, alt %40)
        splitter.setSizes([600, 400])
        
        # Yenile butonu
        yenile_layout = QHBoxLayout()
        yenile_btn = QPushButton("🔄 Listeyi Yenile")
        yenile_btn.clicked.connect(self.capraz_satis_listesini_yukle)
        yenile_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1976d2, stop:1 #1565c0);
                color: white;
                font-size: 11pt;
                font-weight: bold;
                padding: 12px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1565c0, stop:1 #0d47a1);
            }
        """)
        yenile_layout.addStretch()
        yenile_layout.addWidget(yenile_btn)
        yenile_layout.addStretch()
        main_layout.addLayout(yenile_layout)
        
        # İlk yükleme
        self.capraz_satis_listesini_yukle()
    
    def capraz_satis_listesini_yukle(self):
        """Çapraz satış için poliçe listesini yükle"""
        policeler = self.db.capraz_satis_policeleri_getir()
        
        self.capraz_satis_table.setRowCount(0)
        
        for police in policeler:
            row_position = self.capraz_satis_table.rowCount()
            self.capraz_satis_table.insertRow(row_position)
            
            police_id, police_no, musteri_adi, telefon, tc_no, tur, sirket, baslangic, bitis, prim, tarih = police
            
            # Police ID'yi sakla
            id_item = QTableWidgetItem(police_no)
            id_item.setData(Qt.UserRole, police_id)
            
            # Tabloya ekle
            self.capraz_satis_table.setItem(row_position, 0, id_item)
            self.capraz_satis_table.setItem(row_position, 1, QTableWidgetItem(musteri_adi or ""))
            self.capraz_satis_table.setItem(row_position, 2, QTableWidgetItem(telefon or ""))
            self.capraz_satis_table.setItem(row_position, 3, QTableWidgetItem(tur))
            self.capraz_satis_table.setItem(row_position, 4, QTableWidgetItem(sirket))
            
            # Tarihler
            try:
                baslangic_obj = datetime.strptime(baslangic, "%Y-%m-%d")
                baslangic_str = baslangic_obj.strftime("%d.%m.%Y")
            except:
                baslangic_str = baslangic
            self.capraz_satis_table.setItem(row_position, 5, QTableWidgetItem(baslangic_str))
            
            try:
                bitis_obj = datetime.strptime(bitis, "%Y-%m-%d")
                bitis_str = bitis_obj.strftime("%d.%m.%Y")
            except:
                bitis_str = bitis
            self.capraz_satis_table.setItem(row_position, 6, QTableWidgetItem(bitis_str))
            
            self.capraz_satis_table.setItem(row_position, 7, QTableWidgetItem(f"{prim:,.2f}" if prim else "0.00"))
    
    def capraz_satis_police_secildi(self):
        """Poliçe seçildiğinde çapraz satış önerilerini göster"""
        selected_items = self.capraz_satis_table.selectedItems()
        if not selected_items:
            return
        
        row = selected_items[0].row()
        police_id_item = self.capraz_satis_table.item(row, 0)
        if not police_id_item:
            return
        
        police_id = police_id_item.data(Qt.UserRole)
        
        # Poliçe bilgilerini al
        police_no = self.capraz_satis_table.item(row, 0).text()
        musteri = self.capraz_satis_table.item(row, 1).text()
        tur = self.capraz_satis_table.item(row, 3).text()
        sirket = self.capraz_satis_table.item(row, 4).text()
        
        # Çapraz satış önerilerini al
        oneriler = self.db.capraz_satis_onerileri_getir(tur)
        
        # Öneriler widget'ını temizle
        while self.oneriler_layout.count():
            child = self.oneriler_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Seçili poliçe bilgisi
        secili_label = QLabel(f"📌 Seçili Poliçe: {police_no} - {musteri} ({tur})")
        secili_label.setStyleSheet("""
            font-size: 11pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 10px;
            background-color: #bbdefb;
            border-radius: 5px;
            margin-bottom: 10px;
        """)
        self.oneriler_layout.addWidget(secili_label)
        
        if not oneriler:
            no_oneri_label = QLabel("Bu poliçe türü için çapraz satış önerisi bulunmamaktadır.")
            no_oneri_label.setStyleSheet("""
                font-size: 10pt;
                color: #78909c;
                padding: 20px;
                text-align: center;
            """)
            no_oneri_label.setAlignment(Qt.AlignCenter)
            self.oneriler_layout.addWidget(no_oneri_label)
        else:
            for oneri_tur in oneriler:
                oneri_group = QGroupBox(f"💼 {oneri_tur}")
                oneri_group.setStyleSheet("""
                    QGroupBox {
                        font-weight: bold;
                        border: 2px solid #1976d2;
                        border-radius: 8px;
                        margin-top: 10px;
                        padding-top: 15px;
                        background-color: #ffffff;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 5px;
                        color: #0d47a1;
                        font-size: 11pt;
                    }
                """)
                oneri_layout = QHBoxLayout()
                oneri_group.setLayout(oneri_layout)
                
                # Açıklama
                aciklama_text = f"{tur} sigortası olan müşteriye {oneri_tur} sigortası önerilebilir."
                aciklama_label = QLabel(aciklama_text)
                aciklama_label.setWordWrap(True)
                aciklama_label.setStyleSheet("padding: 10px;")
                oneri_layout.addWidget(aciklama_label)
                
                # Poliçe Ekle butonu
                ekle_btn = QPushButton(f"➕ {oneri_tur} Poliçesi Ekle")
                ekle_btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 #2e7d32, stop:1 #1b5e20);
                        color: white;
                        font-size: 10pt;
                        font-weight: bold;
                        padding: 10px 20px;
                        border-radius: 5px;
                        min-width: 150px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                   stop:0 #388e3c, stop:1 #2e7d32);
                    }
                """)
                ekle_btn.clicked.connect(lambda checked, pid=police_id, ot=oneri_tur: self.capraz_satis_police_ekle(pid, ot))
                oneri_layout.addWidget(ekle_btn)
                
                self.oneriler_layout.addWidget(oneri_group)
        
        self.oneriler_layout.addStretch()
    
    def capraz_satis_police_ekle(self, mevcut_police_id, oneri_turu):
        """Çapraz satış önerisi için yeni poliçe ekleme penceresi aç"""
        # Mevcut poliçe bilgilerini al (Supabase ile)
        result = self.db.musteri_police_detay_getir(mevcut_police_id)
        
        if not result:
            QMessageBox.warning(self, "Hata", "Müşteri bilgileri bulunamadı!")
            return
        
        musteri_id, musteri_adi, tc_no, telefon = result
        
        # Çapraz satış poliçe ekleme dialogunu aç
        dialog = CaprazSatisPoliceEkleDialog(self, musteri_id, musteri_adi, oneri_turu, self.db)
        if dialog.exec():
            # Poliçe eklendi, tüm listeleri güncelle
            self.tum_listeleri_guncelle()
    
    def closeEvent(self, event):
        """Uygulama kapatılırken veritabanını kapat"""
        self.db.close()
        event.accept()


class PoliceDetayDialog(QDialog):
    """Poliçe detay ve düzenleme penceresi"""
    
    def __init__(self, parent, police_no, db):
        super().__init__(parent)
        self.db = db
        self.police_no = police_no
        self.police_data = None
        self.init_ui()
        self.bilgileri_yukle()
    
    def init_ui(self):
        """Pencereyi oluştur"""
        self.setWindowTitle("Poliçe Detayları")
        self.setGeometry(200, 200, 600, 700)
        self.setModal(True)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Başlık
        baslik = QLabel("📄 Poliçe Detayları ve Düzenleme")
        baslik_font = QFont("Arial", 14, QFont.Weight.Bold)
        baslik.setFont(baslik_font)
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("""
            color: white;
            padding: 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                       stop:0 #1976d2, stop:1 #1565c0);
            border-radius: 5px;
        """)
        layout.addWidget(baslik)
        
        # MÜŞTERİ BİLGİLERİ (Sadece görüntüleme)
        musteri_group = QGroupBox("Müşteri Bilgileri")
        musteri_layout = QFormLayout()
        musteri_group.setLayout(musteri_layout)
        
        self.musteri_ad_label = QLabel()
        self.musteri_ad_label.setStyleSheet("padding: 5px; background-color: #f5f5f5; border-radius: 3px;")
        musteri_layout.addRow("Ad Soyad:", self.musteri_ad_label)
        
        self.musteri_tc_label = QLabel()
        self.musteri_tc_label.setStyleSheet("padding: 5px; background-color: #f5f5f5; border-radius: 3px;")
        musteri_layout.addRow("TC No:", self.musteri_tc_label)
        
        self.musteri_telefon_label = QLabel()
        self.musteri_telefon_label.setStyleSheet("padding: 5px; background-color: #f5f5f5; border-radius: 3px;")
        musteri_layout.addRow("Telefon:", self.musteri_telefon_label)
        
        self.musteri_email_label = QLabel()
        self.musteri_email_label.setStyleSheet("padding: 5px; background-color: #f5f5f5; border-radius: 3px;")
        musteri_layout.addRow("E-mail:", self.musteri_email_label)
        
        layout.addWidget(musteri_group)
        
        # POLİÇE BİLGİLERİ (Düzenlenebilir)
        police_group = QGroupBox("Poliçe Bilgileri (Düzenlenebilir)")
        police_layout = QFormLayout()
        police_group.setLayout(police_layout)
        
        self.police_no_input = QLineEdit()
        police_layout.addRow("Poliçe No:", self.police_no_input)
        
        self.tur_combo = QComboBox()
        self.tur_combo.addItems([
            "Kasko", "Trafik", "Konut", "İşyeri", 
            "Sağlık", "Hayat", "Dask", "Seyahat", "Ferdi Kaza"
        ])
        police_layout.addRow("Poliçe Türü:", self.tur_combo)
        
        self.sirket_combo = QComboBox()
        self.sirket_combo.addItems([
            "Anadolu Sigorta", "Allianz", "AXA Sigorta",
            "HDI Sigorta", "Mapfre Sigorta", "Türk Nippon",
            "Aksigorta", "Groupama", "Ziraat Sigorta", "Halk Sigorta"
        ])
        police_layout.addRow("Şirket:", self.sirket_combo)
        
        self.baslangic_date = QDateEdit()
        self.baslangic_date.setCalendarPopup(True)
        self.baslangic_date.setDisplayFormat("dd.MM.yyyy")
        police_layout.addRow("Başlangıç Tarihi:", self.baslangic_date)
        
        self.bitis_date = QDateEdit()
        self.bitis_date.setCalendarPopup(True)
        self.bitis_date.setDisplayFormat("dd.MM.yyyy")
        police_layout.addRow("Bitiş Tarihi:", self.bitis_date)
        
        self.prim_input = QLineEdit()
        police_layout.addRow("Prim Tutarı (₺):", self.prim_input)
        
        self.komisyon_label = QLabel()
        self.komisyon_label.setStyleSheet("""
            padding: 8px; 
            background-color: #e8f5e9; 
            border-radius: 3px;
            font-weight: bold;
            color: #2e7d32;
        """)
        police_layout.addRow("Komisyon (₺):", self.komisyon_label)
        
        # Prim değişince komisyon güncelle
        self.prim_input.textChanged.connect(self.komisyon_hesapla)
        
        self.aciklama_input = QTextEdit()
        self.aciklama_input.setMaximumHeight(80)
        police_layout.addRow("Açıklama:", self.aciklama_input)
        
        # Satışçı
        self.satisci_combo_dialog = QComboBox()
        self.satisci_combo_dialog.addItem("Seçiniz", None)
        satiscilar = self.db.satiscilari_getir()
        for satisci_id, ad_soyad in satiscilar:
            self.satisci_combo_dialog.addItem(ad_soyad, satisci_id)
        police_layout.addRow("Satışçı:", self.satisci_combo_dialog)
        
        layout.addWidget(police_group)
        
        # BUTONLAR
        buton_layout = QHBoxLayout()
        
        # Güncelle butonu
        guncelle_btn = QPushButton("✅ GÜNCELLE")
        guncelle_btn.clicked.connect(self.guncelle)
        guncelle_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #66bb6a, stop:1 #43a047);
                color: white;
                padding: 12px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #81c784, stop:1 #66bb6a);
            }
        """)
        buton_layout.addWidget(guncelle_btn)
        
        # Sil butonu
        sil_btn = QPushButton("🗑️ SİL")
        sil_btn.clicked.connect(self.sil)
        sil_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #ef5350, stop:1 #e53935);
                color: white;
                padding: 12px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #e57373, stop:1 #ef5350);
            }
        """)
        buton_layout.addWidget(sil_btn)
        
        # İptal butonu
        iptal_btn = QPushButton("❌ İPTAL")
        iptal_btn.clicked.connect(self.reject)
        iptal_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #78909c, stop:1 #546e7a);
                color: white;
                padding: 12px;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #90a4ae, stop:1 #78909c);
            }
        """)
        buton_layout.addWidget(iptal_btn)
        
        layout.addLayout(buton_layout)
        
        # Stil
        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #78909c;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #37474f;
            }
            QLineEdit, QComboBox, QDateEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #90a4ae;
                border-radius: 4px;
                background-color: white;
                font-size: 11pt;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
                border: 2px solid #1976d2;
            }
            QLabel {
                font-size: 10pt;
            }
        """)
    
    def bilgileri_yukle(self):
        """Poliçe bilgilerini veritabanından yükle"""
        self.police_data = self.db.police_detay_getir(self.police_no)
        
        if not self.police_data:
            QMessageBox.warning(self, "Hata", "Poliçe bilgileri yüklenemedi!")
            self.reject()
            return
        
        # Müşteri bilgileri
        self.musteri_ad_label.setText(self.police_data[9])
        self.musteri_tc_label.setText(self.police_data[10])
        self.musteri_telefon_label.setText(self.police_data[11] or "-")
        self.musteri_email_label.setText(self.police_data[12] or "-")
        
        # Poliçe bilgileri
        self.police_no_input.setText(self.police_data[1])
        self.tur_combo.setCurrentText(self.police_data[2])
        self.sirket_combo.setCurrentText(self.police_data[3])
        
        # Tarihleri ayarla
        baslangic = datetime.strptime(self.police_data[4], "%Y-%m-%d")
        bitis = datetime.strptime(self.police_data[5], "%Y-%m-%d")
        self.baslangic_date.setDate(QDate(baslangic.year, baslangic.month, baslangic.day))
        self.bitis_date.setDate(QDate(bitis.year, bitis.month, bitis.day))
        
        # Tutarlar
        self.prim_input.setText(str(self.police_data[6]))
        self.komisyon_hesapla()
        
        # Açıklama
        self.aciklama_input.setText(self.police_data[8] or "")
        
        # Satışçı
        if self.police_data[13]:  # satisci_id
            for i in range(self.satisci_combo_dialog.count()):
                if self.satisci_combo_dialog.itemData(i) == self.police_data[13]:
                    self.satisci_combo_dialog.setCurrentIndex(i)
                    break
    
    def komisyon_hesapla(self):
        """Komisyon tutarını hesapla ve göster"""
        try:
            prim = float(self.prim_input.text()) if self.prim_input.text() else 0.0
            komisyon = prim * 0.15
            self.komisyon_label.setText(f"{komisyon:,.2f} ₺")
        except:
            self.komisyon_label.setText("0.00 ₺")
    
    def guncelle(self):
        """Poliçe bilgilerini güncelle"""
        # Değerleri al
        police_no = self.police_no_input.text().strip()
        tur = self.tur_combo.currentText()
        sirket = self.sirket_combo.currentText()
        baslangic = self.baslangic_date.date().toString("yyyy-MM-dd")
        bitis = self.bitis_date.date().toString("yyyy-MM-dd")
        
        try:
            prim = float(self.prim_input.text()) if self.prim_input.text() else 0.0
            komisyon = prim * 0.15
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir prim tutarı giriniz!")
            return
        
        aciklama = self.aciklama_input.toPlainText().strip()
        satisci_id = self.satisci_combo_dialog.currentData()
        
        # Validasyon
        if not police_no:
            QMessageBox.warning(self, "Uyarı", "Poliçe numarası boş olamaz!")
            return
        
        # Güncelleme yap
        success, message = self.db.police_guncelle(
            self.police_data[0],  # police_id
            police_no, tur, sirket, baslangic, bitis,
            prim, komisyon, aciklama, satisci_id
        )
        
        if success:
            QMessageBox.information(self, "Başarılı", message)
            self.accept()
        else:
            QMessageBox.critical(self, "Hata", message)
    
    def sil(self):
        """Poliçeyi sil"""
        # Onay iste
        reply = QMessageBox.question(
            self, 
            "Poliçe Sil",
            f"'{self.police_no}' numaralı poliçeyi silmek istediğinize emin misiniz?\n\nBu işlem geri alınamaz!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.db.police_sil(self.police_data[0])
            
            if success:
                QMessageBox.information(self, "Başarılı", message)
                self.accept()
            else:
                QMessageBox.critical(self, "Hata", message)

class TarihFiltreDialog(QDialog):
    """Tarih filtresi için küçük dialog"""
    
    def __init__(self, parent, kalan_gun, gecen_gun):
        super().__init__(parent)
        self.kalan_gun = kalan_gun
        self.gecen_gun = gecen_gun
        self.init_ui()
    
    def init_ui(self):
        """Dialog'u oluştur"""
        self.setWindowTitle("Tarih Filtresi")
        self.setModal(True)
        self.setFixedSize(400, 240)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Başlık
        baslik = QLabel("⚙️ Yenileme Filtresi")
        baslik.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 10px;
            background-color: #bbdefb;
            border-radius: 5px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        layout.addWidget(baslik)
        
        # Form
        form_layout = QFormLayout()
        
        # Kalan gün
        kalan_widget = QWidget()
        kalan_layout = QHBoxLayout()
        kalan_widget.setLayout(kalan_layout)
        
        self.kalan_input = QLineEdit()
        self.kalan_input.setText(str(self.kalan_gun))
        self.kalan_input.setMaximumWidth(120)
        self.kalan_input.setMinimumWidth(100)
        self.kalan_input.setAlignment(Qt.AlignCenter)
        self.kalan_input.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            padding: 12px;
            border: 3px solid #1976d2;
            border-radius: 5px;
        """)
        kalan_layout.addWidget(self.kalan_input)
        kalan_layout.addWidget(QLabel("gün kalan"))
        kalan_layout.addStretch()
        
        form_layout.addRow("⏰ Kalan Gün:", kalan_widget)
        
        # Geçen gün
        gecen_widget = QWidget()
        gecen_layout = QHBoxLayout()
        gecen_widget.setLayout(gecen_layout)
        
        self.gecen_input = QLineEdit()
        self.gecen_input.setText(str(self.gecen_gun))
        self.gecen_input.setMaximumWidth(120)
        self.gecen_input.setMinimumWidth(100)
        self.gecen_input.setAlignment(Qt.AlignCenter)
        self.gecen_input.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            padding: 12px;
            border: 3px solid #e53935;
            border-radius: 5px;
        """)
        gecen_layout.addWidget(self.gecen_input)
        gecen_layout.addWidget(QLabel("gün geçen"))
        gecen_layout.addStretch()
        
        form_layout.addRow("⚠️ Geçen Gün:", gecen_widget)
        
        layout.addLayout(form_layout)
        
        # Açıklama
        aciklama = QLabel("Bitiş tarihi bu aralıktaki poliçeleri gösterir")
        aciklama.setStyleSheet("color: #546e7a; font-size: 9pt; padding: 10px;")
        aciklama.setAlignment(Qt.AlignCenter)
        layout.addWidget(aciklama)
        
        # Butonlar
        buton_layout = QHBoxLayout()
        
        tamam_btn = QPushButton("✅ TAMAM")
        tamam_btn.clicked.connect(self.tamam)
        tamam_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #66bb6a, stop:1 #43a047);
                color: white;
                font-size: 11pt;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #81c784, stop:1 #66bb6a);
            }
        """)
        buton_layout.addWidget(tamam_btn)
        
        iptal_btn = QPushButton("❌ İPTAL")
        iptal_btn.clicked.connect(self.reject)
        iptal_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #78909c, stop:1 #546e7a);
                color: white;
                font-size: 11pt;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #90a4ae, stop:1 #78909c);
            }
        """)
        buton_layout.addWidget(iptal_btn)
        
        layout.addLayout(buton_layout)
        
        # Stil
        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
            }
            QLabel {
                font-size: 10pt;
            }
        """)
    
    def tamam(self):
        """Tamam butonuna basıldı"""
        try:
            self.kalan_gun = int(self.kalan_input.text())
            self.gecen_gun = int(self.gecen_input.text())
            
            if self.kalan_gun < 0 or self.gecen_gun < 0:
                QMessageBox.warning(self, "Uyarı", "Lütfen pozitif sayılar giriniz!")
                return
            
            self.accept()
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli sayılar giriniz!")


class CaprazSatisPoliceEkleDialog(QDialog):
    """Çapraz satış için hızlı poliçe ekleme dialogu"""
    def __init__(self, parent, musteri_id, musteri_adi, oneri_turu, db):
        super().__init__(parent)
        self.musteri_id = musteri_id
        self.musteri_adi = musteri_adi
        self.oneri_turu = oneri_turu
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        """Dialog'u oluştur"""
        self.setWindowTitle(f"➕ {self.oneri_turu} Poliçesi Ekle - Çapraz Satış")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Başlık
        baslik = QLabel(f"🔄 ÇAPRAZ SATIŞ: {self.oneri_turu}")
        baslik.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 15px;
            background-color: #bbdefb;
            border-radius: 5px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        layout.addWidget(baslik)
        
        # Müşteri bilgisi
        musteri_label = QLabel(f"👤 Müşteri: {self.musteri_adi}")
        musteri_label.setStyleSheet("""
            font-size: 11pt;
            font-weight: bold;
            color: #37474f;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 5px;
        """)
        layout.addWidget(musteri_label)
        
        # Form
        form = QFormLayout()
        
        # Poliçe türü (önceden seçili)
        tur_label = QLabel(self.oneri_turu)
        tur_label.setStyleSheet("""
            font-size: 11pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 8px;
            background-color: #e3f2fd;
            border-radius: 5px;
        """)
        form.addRow("Poliçe Türü:", tur_label)
        
        # Poliçe No
        self.police_no_input = QLineEdit()
        form.addRow("Poliçe No:", self.police_no_input)
        
        # Şirket
        self.sirket_combo = QComboBox()
        self.sirket_combo.addItems([
            "Seçiniz",
            "Anadolu Sigorta",
            "Allianz",
            "AXA Sigorta",
            "HDI Sigorta",
            "Mapfre Sigorta",
            "Türk Nippon",
            "Aksigorta",
            "Groupama",
            "Ziraat Sigorta",
            "Halk Sigorta"
        ])
        form.addRow("Sigorta Şirketi:", self.sirket_combo)
        
        # Başlangıç tarihi
        self.baslangic_tarihi = QDateEdit()
        self.baslangic_tarihi.setCalendarPopup(True)
        self.baslangic_tarihi.setDate(QDate.currentDate())
        self.baslangic_tarihi.setDisplayFormat("dd.MM.yyyy")
        self.baslangic_tarihi.dateChanged.connect(self.baslangic_tarihi_degisti)
        form.addRow("Başlangıç Tarihi:", self.baslangic_tarihi)
        
        # Bitiş tarihi
        self.bitis_tarihi = QDateEdit()
        self.bitis_tarihi.setCalendarPopup(True)
        self.bitis_tarihi.setDate(QDate.currentDate().addYears(1))
        self.bitis_tarihi.setDisplayFormat("dd.MM.yyyy")
        form.addRow("Bitiş Tarihi:", self.bitis_tarihi)
        
        # Prim tutarı
        self.prim_input = QLineEdit()
        form.addRow("Prim Tutarı (₺):", self.prim_input)
        
        # Açıklama
        self.aciklama_input = QTextEdit()
        self.aciklama_input.setMaximumHeight(80)
        self.aciklama_input.setPlaceholderText("Çapraz satış önerisi ile eklenen poliçe...")
        form.addRow("Açıklama:", self.aciklama_input)
        
        layout.addLayout(form)
        
        # Butonlar
        buton_layout = QHBoxLayout()
        
        kaydet_btn = QPushButton("💾 POLİÇEYİ EKLE")
        kaydet_btn.clicked.connect(self.kaydet)
        kaydet_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #2e7d32, stop:1 #1b5e20);
                color: white;
                font-size: 12pt;
                font-weight: bold;
                padding: 12px 25px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #388e3c, stop:1 #2e7d32);
            }
        """)
        buton_layout.addWidget(kaydet_btn)
        
        iptal_btn = QPushButton("❌ İPTAL")
        iptal_btn.clicked.connect(self.reject)
        iptal_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #78909c, stop:1 #546e7a);
                color: white;
                font-size: 12pt;
                font-weight: bold;
                padding: 12px 25px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #90a4ae, stop:1 #78909c);
            }
        """)
        buton_layout.addWidget(iptal_btn)
        
        layout.addLayout(buton_layout)
    
    def baslangic_tarihi_degisti(self, date):
        """Başlangıç tarihi değiştiğinde bitiş tarihini güncelle"""
        self.bitis_tarihi.setDate(date.addYears(1))
    
    def kaydet(self):
        """Poliçeyi kaydet"""
        # Validasyon
        if not self.police_no_input.text().strip():
            QMessageBox.warning(self, "Uyarı", "Lütfen poliçe numarası giriniz!")
            return
        
        if self.sirket_combo.currentIndex() == 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen sigorta şirketi seçiniz!")
            return
        
        try:
            prim_tutari = float(self.prim_input.text().replace(',', '.'))
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir prim tutarı giriniz!")
            return
        
        # Komisyon hesapla (%15)
        komisyon_tutari = prim_tutari * 0.15
        
        # Tarihleri formatla
        baslangic = self.baslangic_tarihi.date().toString("yyyy-MM-dd")
        bitis = self.bitis_tarihi.date().toString("yyyy-MM-dd")
        
        # Varsayılan satışçıyı al
        satiscilar = self.db.satiscilari_getir()
        satisci_id = satiscilar[0][0] if satiscilar else None
        
        # Poliçeyi ekle
        success, message = self.db.police_ekle(
            self.musteri_id,
            self.police_no_input.text().strip(),
            self.oneri_turu,
            self.sirket_combo.currentText(),
            baslangic,
            bitis,
            prim_tutari,
            komisyon_tutari,
            self.aciklama_input.toPlainText(),
            satisci_id,
            'Nakit'  # Varsayılan ödeme şekli
        )
        
        if success:
            QMessageBox.information(self, "Başarılı", f"{self.oneri_turu} poliçesi başarıyla eklendi!\n\n{message}")
            self.accept()
        else:
            QMessageBox.critical(self, "Hata", message)


class FinansDetayDialog(QDialog):
    """Finans detay ve güncelleme penceresi"""
    def __init__(self, parent, police_id, db):
        super().__init__(parent)
        self.police_id = police_id
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        """Finans detay penceresini oluştur"""
        self.setWindowTitle("💰 Finans Detayı")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Başlık
        baslik = QLabel("BORÇ DETAYI VE GÜNCELLEME")
        baslik.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #0d47a1;
            padding: 15px;
            background-color: #bbdefb;
            border-radius: 5px;
        """)
        baslik.setAlignment(Qt.AlignCenter)
        layout.addWidget(baslik)
        
        # Poliçe bilgilerini getir
        detay = self.db.finans_detay_getir(self.police_id)
        
        if not detay:
            QMessageBox.warning(self, "Hata", "Poliçe bilgileri bulunamadı!")
            self.reject()
            return
        
        police_no, musteri_adi, tur, sirket, prim, borc, odenen, kalan = detay
        
        # Eğer finans kaydı yoksa default değerler
        if borc is None:
            borc = prim
        if odenen is None:
            odenen = 0
        if kalan is None:
            kalan = borc - odenen
        
        # Bilgi grubu
        bilgi_group = QGroupBox("📋 Poliçe Bilgileri")
        bilgi_layout = QFormLayout()
        bilgi_group.setLayout(bilgi_layout)
        
        bilgi_layout.addRow("Poliçe No:", QLabel(f"<b>{police_no}</b>"))
        bilgi_layout.addRow("Müşteri:", QLabel(f"<b>{musteri_adi}</b>"))
        bilgi_layout.addRow("Tür:", QLabel(tur))
        bilgi_layout.addRow("Şirket:", QLabel(sirket))
        bilgi_layout.addRow("Prim Tutarı:", QLabel(f"<b style='color:#1976d2;'>{prim:,.2f} TL</b>"))
        
        layout.addWidget(bilgi_group)
        
        # Borç durumu
        borc_group = QGroupBox("💰 Borç Durumu")
        borc_layout = QFormLayout()
        borc_group.setLayout(borc_layout)
        
        borc_layout.addRow("Toplam Borç:", QLabel(f"<b style='font-size:12pt;'>{borc:,.2f} TL</b>"))
        borc_layout.addRow("Ödenen:", QLabel(f"<b style='color:#2e7d32; font-size:12pt;'>{odenen:,.2f} TL</b>"))
        
        kalan_renk = "#b71c1c" if kalan > 0 else "#2e7d32"
        borc_layout.addRow("Kalan Borç:", QLabel(f"<b style='color:{kalan_renk}; font-size:14pt;'>{kalan:,.2f} TL</b>"))
        
        layout.addWidget(borc_group)
        
        # Ödeme işlemi
        odeme_group = QGroupBox("💳 Ödeme İşlemi")
        odeme_layout = QVBoxLayout()
        odeme_group.setLayout(odeme_layout)
        
        # Ödeme tutarı
        odeme_form = QFormLayout()
        
        self.odeme_input = QLineEdit()
        self.odeme_input.setPlaceholderText("Ödeme tutarını giriniz...")
        self.odeme_input.textChanged.connect(self.odeme_hesapla)
        odeme_form.addRow("Ödeme Tutarı:", self.odeme_input)
        
        self.yeni_kalan_label = QLabel("-")
        self.yeni_kalan_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #1976d2;")
        odeme_form.addRow("Yeni Kalan:", self.yeni_kalan_label)
        
        odeme_layout.addLayout(odeme_form)
        
        # Hızlı ödeme butonları
        hizli_layout = QHBoxLayout()
        hizli_label = QLabel("Hızlı Ödeme:")
        hizli_layout.addWidget(hizli_label)
        
        tam_odemle_btn = QPushButton(f"Tamamını Öde ({kalan:,.2f} TL)")
        tam_odemle_btn.clicked.connect(lambda: self.odeme_input.setText(str(kalan)))
        tam_odemle_btn.setStyleSheet("""
            QPushButton {
                background-color: #2e7d32;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1b5e20;
            }
        """)
        hizli_layout.addWidget(tam_odemle_btn)
        
        yarim_btn = QPushButton(f"Yarısını Öde ({kalan/2:,.2f} TL)")
        yarim_btn.clicked.connect(lambda: self.odeme_input.setText(str(kalan/2)))
        yarim_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0d47a1;
            }
        """)
        hizli_layout.addWidget(yarim_btn)
        
        odeme_layout.addLayout(hizli_layout)
        
        layout.addWidget(odeme_group)
        
        # Butonlar
        buton_layout = QHBoxLayout()
        
        kaydet_btn = QPushButton("💾 KAYDET")
        kaydet_btn.clicked.connect(self.odeme_kaydet)
        kaydet_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #2e7d32, stop:1 #1b5e20);
                color: white;
                font-size: 12pt;
                font-weight: bold;
                padding: 12px 25px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #388e3c, stop:1 #2e7d32);
            }
        """)
        buton_layout.addWidget(kaydet_btn)
        
        iptal_btn = QPushButton("❌ İPTAL")
        iptal_btn.clicked.connect(self.reject)
        iptal_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #78909c, stop:1 #546e7a);
                color: white;
                font-size: 12pt;
                font-weight: bold;
                padding: 12px 25px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #90a4ae, stop:1 #78909c);
            }
        """)
        buton_layout.addWidget(iptal_btn)
        
        layout.addLayout(buton_layout)
        
        # Mevcut kalan borcu sakla
        self.mevcut_kalan = kalan
        
        # Stil
        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #78909c;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #37474f;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #90a4ae;
                border-radius: 4px;
                background-color: #fafafa;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border: 2px solid #1976d2;
                background-color: #ffffff;
            }
        """)
    
    def odeme_hesapla(self):
        """Ödeme tutarına göre yeni kalan borcu hesapla"""
        try:
            odeme = float(self.odeme_input.text().replace(',', '.'))
            yeni_kalan = self.mevcut_kalan - odeme
            
            if yeni_kalan < 0:
                self.yeni_kalan_label.setText(f"<span style='color:#b71c1c;'>{yeni_kalan:,.2f} TL (Fazla ödeme!)</span>")
            elif yeni_kalan == 0:
                self.yeni_kalan_label.setText(f"<span style='color:#2e7d32;'>0.00 TL (TAM ÖDEME ✓)</span>")
            else:
                self.yeni_kalan_label.setText(f"<span style='color:#1976d2;'>{yeni_kalan:,.2f} TL</span>")
        except ValueError:
            self.yeni_kalan_label.setText("-")
    
    def odeme_kaydet(self):
        """Ödeme işlemini kaydet"""
        try:
            odeme_tutari = float(self.odeme_input.text().replace(',', '.'))
            
            if odeme_tutari <= 0:
                QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir ödeme tutarı giriniz!")
                return
            
            if odeme_tutari > self.mevcut_kalan:
                cevap = QMessageBox.question(
                    self, 
                    "Fazla Ödeme", 
                    f"Ödeme tutarı kalan borçtan fazla!\n\nKalan: {self.mevcut_kalan:,.2f} TL\n"
                    f"Ödeme: {odeme_tutari:,.2f} TL\n\nDevam etmek istiyor musunuz?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if cevap == QMessageBox.No:
                    return
            
            # Veritabanını güncelle
            success, message = self.db.finans_guncelle(self.police_id, odeme_tutari)
            
            if success:
                QMessageBox.information(self, "Başarılı", "Ödeme kaydedildi!")
                self.accept()
            else:
                QMessageBox.critical(self, "Hata", message)
        
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Lütfen geçerli bir sayı giriniz!")

def main():
    app = QApplication(sys.argv)
    window = SigortaAcenteApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

