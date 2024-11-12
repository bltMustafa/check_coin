# Coin List Comparison Tool

Bu Python programı, Binance, Bybit, Gate.io ve CoinGecko gibi kripto para borsalarının sunduğu coin listelerini
karşılaştırarak, belirli borsalarda bulunan veya bulunmayan coinleri tespit etmeye yardımcı olur.

## İçindekiler

- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Çalışma Mantığı](#çalışma-mantığı)

---

## Kurulum

### Gereksinimler

- Python 3.x
- `venv`
- `requests`, `colorama`, `tabulate` kütüphaneleri (HTTP istekleri, renkli çıktı ve tablo formatında gösterim için)

```bash
pip install -r requirements.txt
```

# Kullanım

Bu araç, Bybit API ile iletişim kurmak için API anahtarı ve gizli anahtar gerektirir. API anahtarlarınızı BYBIT_API_KEY
ve BYBIT_API_SECRET değişkenlerine ekleyin.

# Çalışma Mantığı

```

=== Binance'de olup Bybit'te olmayan coinler ===
+-----------------------------+
| Binance-Only Coins (Not in Bybit) |
+-----------------------------+
| BTCUSDT                      |
| ETHUSDT                      |
| ...                          |
+-----------------------------+

=== Bybit'te olup Binance'de olmayan coinler ===
+-----------------------------+
| Bybit-Only Coins (Not in Binance) |
+-----------------------------+
| XYZUSDT                      |
| ABCUSDT                      |
| ...                          |
+-----------------------------+

```