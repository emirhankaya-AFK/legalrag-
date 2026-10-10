# English
LegalRAG is an automated legal contract risk assessment and clause extraction system.

**Purpose**  
Provides batch processing of PDF agreements, risk scoring, clause comparison, question‑answering with citations, and exportable reports.

**Verified Features**  
- Batch PDF upload  
- Risk score indicator (0‑100 progress bar) based on predefined rule weights  
- Side‑by‑side contract comparison of clauses and risk weights  
- Citations‑enabled Q&A using semantic embeddings  
- Export of PDF report, CSV summary, and JSON data  

**Stack**  
- Backend: Python, FastAPI, Uvicorn  
- Frontend: Streamlit  
- Dependencies listed in `backend/requirements.txt`  

**Setup & Usage**  
1. Clone the repository and navigate to the project directory:  
   ```bash
   cd legalrag
   ```  
2. Create a virtual environment and install dependencies:  
   ```bash
   pip install -r backend/requirements.txt
   ```  
3. Set the Gemini API key (optional – without it the app runs in Mock Mode):  
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```  
4. Start the backend:  
   ```bash
   uvicorn backend.main:app --port 8001 --reload
   ```  
5. Start the frontend in a separate terminal:  
   ```bash
   streamlit run frontend/app.py --server.port 8501
   ```  

**Testing**  
Unit tests are located in the `tests/` directory (e.g., `test_extraction.py`, `test_rag.py`, `test_risk.py`). Run them with a test runner such as `pytest`.

**Limitations**  
- Requires a valid Gemini API key for real LLM‑powered analysis; otherwise operates in Mock Mode with simulated outputs.  
- Functionality is limited to the features implemented in the repository; no claims are made about performance, scalability, or production readiness.

---

# Türkçe
LegalRAG, otomatik yasal sözleşme risk değerlendirmesi ve maddeleri çıkarma sistemidir.

**Amaç**  
PDF sözleşmelerini toplu işleme, risk puanı gösterimi, yan‑yanı sözleşme karşılaştırması, alıntılı soru‑cevap ve dışa aktarılabilir raporlar sunar.

**Doğrulanmış Özellikler**  
- Toplu PDF yükleme  
- Önceden tanımlı kural ağırlıklarına dayalı risk puanı göstergesi (0‑100 ilerleme çubuğu)  
- İki sözleşmenin maddeleri ve risk ağırlıkları yan‑yanı karşılaştırma  
- Anlamsal gömme kullanarak alıntılı soru‑cevap  
- PDF raporu, CSV özeti ve JSON veri dışa aktarma  

**Yığın**  
- Arka uç: Python, FastAPI, Uvicorn  
- Ön uç: Streamlit  
- Bağımlılıklar `backend/requirements.txt` dosyasında belirtilmiştir  

**Kurulum & Kullanım**  
1. Depoyu klonlayıp proje dizinine gidin:  
   ```bash
   cd legalrag
   ```  
2. Sanal ortam oluşturup bağımlılıkları yükleyin:  
   ```bash
   pip install -r backend/requirements.txt
   ```  
3. Gemini API anahtarını ayarlayın (isteğe bağlı – anahtar yoksa uygulama Mock Modda çalışır):  
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```  
4. Arka ucu başlatın:  
   ```bash
   uvicorn backend.main:app --port 8001 --reload
   ```  
5. Başka bir terminalde ön ucu başlatın:  
   ```bash
   streamlit run frontend/app.py --server.port 8501
   ```  

**Test**  
Birim testleri `tests/` klasöründe bulunur (ör. `test_extraction.py`, `test_rag.py`, `test_risk.py`). `pytest` gibi bir test çalıştırıcıyla çalıştırılabilir.

**Sınırlamalar**  
- Gerçek LLM‑tabanlı analiz için geçerli bir Gemini API anahtarı gereklidir; aksi takdirde uygulama simüle edilmiş çıktılarla Mock Modda çalışır.  
- Depoda uygulanan özellikler dışında bir şey vaat edilmez; performans, ölçeklenebilirlik veya üretim hazırlığı hakkında iddia yoktur.

---

# Deutsch
LegalRAG ist ein automatisiertes System zur Risikobewertung von Rechtsverträgen und Extraktion von Klauseln.

**Zweck**  
Ermöglicht die Stapelverarbeitung von PDF‑Verträgen, Risikobewertung, Seiten‑an‑Seiten‑Vergleich von Klauseln, Frage‑und‑Antwort‑Interaktion mit Quellenangaben sowie den Export von Berichten.

**Verifizierte Funktionen**  
- Stapel‑PDF‑Upload  
- Risikoanzeige (0‑100 Fortschrittsbalken) basierend auf vordefinierten Regelgewichtungen  
- Seiten‑an‑Seiten‑Vergleich von Klauseln und Risikogewichtungen zweier Verträge  
- Quellenbasierte Frage‑und‑Antwort mittels semantischer Einbettungen  
- Export von PDF‑Bericht, CSV‑Zusammenfassung und JSON‑Daten  

**Technologie‑Stack**  
- Backend: Python, FastAPI, Uvicorn  
- Frontend: Streamlit  
- Abhängigkeiten siehe `backend/requirements.txt`  

**Installation & Verwendung**  
1. Repository klonen und ins Projektverzeichnis wechseln:  
   ```bash
   cd legalrag
   ```  
2. Virtuelle Umgebung anlegen und Abhängigkeiten installieren:  
   ```bash
   pip install -r backend/requirements.txt
   ```  
3. Gemini API‑Schlüssel setzen (optional – ohne Schlüssel läuft die Anwendung im Mock‑Modus):  
   ```bash
   export GEMINI_API_KEY="your-gemini-api-key"
   ```  
4. Backend starten:  
   ```bash
   uvicorn backend.main:app --port 8001 --reload
   ```  
5. Frontend in einem weiteren Terminal starten:  
   ```bash
   streamlit run frontend/app.py --server.port 8501
   ```  

**Tests**  
Unit‑tests befinden sich im `tests/`‑Ordner (z. B. `test_extraction.py`, `test_rag.py`, `test_risk.py`). Sie können mit einem Test‑Runner wie `pytest` ausgeführt werden.

**Einschränkungen**  
- Für echte LLM‑gestützte Analyse wird ein gültiger Gemini API‑Schlüssel benötigt; ohne Schlüssel arbeitet die Anwendung im Mock‑Modus mit simulierten Ausgaben.  
- Es werden nur die im Repository implementierten Funktionen angeboten; keine Aussagen über Leistung, Skalierbarkeit oder Produktionsreife werden getroffen.
