# Basit yapılacaklar listesi uygulaması: kullanıcı yeni görev ekleyebilsin, görevl

Bu proje **CM6453 Agent Platform** tarafından üretildi: Master Agent gereksinimi görevlere böldü, her görevi farklı bir yerel LLM ile çalışan bir ajan yaptı.

## Gereksinim

Basit yapılacaklar listesi uygulaması: kullanıcı yeni görev ekleyebilsin, görevleri listede görebilsin, bir görevi tamamlandı olarak işaretleyebilsin ve silebilsin.

## Adımlar

| Adım | Ajan | Model | Durum | Deneme | Özet |
| --- | --- | --- | --- | --- | --- |
| Database | agent_esra | qwen2.5-coder:7b | tamamlandı | 1 | 1 tablo: tasks |
| Backend | agent_merve | gemma3:4b | tamamlandı | 1 | 5 endpoint, tablolar: tasks |
| Frontend | agent_melisa | qwen2.5-coder:7b | tamamlandı | 1 | index.html (89 satır), kullanılan endpoint'ler: GET /api/tasks, POST /api/tasks, GET /api/tasks/<int:task_id>, PUT /api/tasks/<int:task_id>, DELETE /api/tasks/<int:task_id> |
| Testing | agent_okan | gemma3:4b | tamamlandı | 1 | 5 test metodu |

## Dosyalar

- `backend/app.py`
- `database/schema.sql`
- `frontend/index.html`
- `testing/test_app.py`

## Çalıştırma

Python 3.10+ yeterli; ek paket gerekmez.

```bash
python3 run.py
```

Backend `http://localhost:9000` adresinde açılır, arayüz tarayıcıda açılır.

Testler:

```bash
cd backend && python3 -m unittest discover -s ../testing -t ..
```
