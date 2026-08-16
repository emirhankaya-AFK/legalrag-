# LegalRAG — Yapay Zekâ Destekli Hukuki Belge Analizi

[English](README.md) | [Türkçe](README_TR.md)

LegalRAG, sözleşmelerdeki maddeleri çıkaran, riskleri puanlayan, belgeleri karşılaştıran ve kaynak göstererek soru-cevap yapabilen otomatik bir hukuki belge analiz sistemidir.

## Özellikler

- Birden fazla PDF sözleşmesini toplu yükleme
- Önceden tanımlanmış kurallarla 0–100 risk puanı
- İki sözleşmenin maddelerini ve risklerini yan yana karşılaştırma
- Anlamsal arama ve kaynaklı soru-cevap
- PDF raporu, CSV özeti ve JSON verisi dışa aktarma

## Kurulum ve çalıştırma

```bash
pip install -r backend/requirements.txt
export GEMINI_API_KEY="gemini-api-anahtariniz"
uvicorn backend.main:app --port 8001 --reload
```

Başka bir terminalde:

```bash
streamlit run frontend/app.py --server.port 8501
```

API anahtarı verilmezse geliştirme ve test için örnek yanıt modu kullanılır.

> Bu yazılım hukuki danışmanlık vermez. Önemli kararlar için yetkili bir hukuk uzmanına başvurun.

