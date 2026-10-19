# Almanya Elektrik Fiyatı Tahmini ile Soğutma Planlaması

## Problem

Almanya'da faaliyet gösteren bir depomuz olduğunu hayal edelim. Depo, ürünleri saklamak için her gün 6 saat boyunca yoğun soğutma yapıyor ve bu 6 saatlik soğutma bloğunu günün istediği saatine kaydırabiliyor. Elektriği sabit fiyattan değil, borsadaki saatlik fiyata bağlı bir tarifeyle alıyor; dolayısıyla bloğu hangi saatte çalıştırdığı, ürün maliyetini doğrudan etkiliyor.

Almanya'da elektrik fiyatları sabit değil. Rüzgârlı dönemlerde ve öğlen güneşin bol olduğu saatlerde fazla üretim nedeniyle fiyatlar düşüyor; akşam ise güneş üretimi azalırken herkes evine döndüğü için talep artıyor ve fiyatlar yükseliyor.

Bir sonraki günün fiyatları bir gün önceden belirleniyor, ancak yarından sonraki günlerin fiyatları bilinmiyor. Depomuzda vardiya ve bakım planı haftalık yapıldığı için, her hafta başında önümüzdeki 7 günün soğutma saatlerini belirlememiz gerekiyor.

Bu projede verideki örüntüleri keşfederek önümüzdeki 7 gün için saatlik elektrik fiyatı tahmini üreten bir model geliştireceğiz ve bu tahminlere göre soğutma bloğunu her gün en ucuz saatlere yerleştireceğiz.

## Başarı Ölçütü

Modelin başarısını üç senaryoyu karşılaştırarak ölçeceğiz:

- **Sabit plan:** Soğutma bloğu her gün, ortalamada en ucuz saatler olan 10:00–16:00 arasında çalıştırılıyor. Modelin, bu akıllı ama sabit kuralı geçmesi gerekiyor. Diyelim ki maliyeti 100 €.
- **Kusursuz bilgi:** Geleceği bilseydik en ucuz saatlerle ödeyeceğimiz tutar. Diyelim ki 60 €; daha ucuzu mümkün değil.
- **Model:** Tahminlere göre seçtiğimiz saatlerle ödediğimiz tutar. Diyelim ki 70 €.

Buradan iki oran çıkıyor:

- **Tasarruf oranı:** (100 − 70) ÷ 100 = **%30**
- **Yakalama oranı:** Modelin sağladığı tasarrufun, mümkün olan en büyük tasarrufa oranı: (100 − 70) ÷ (100 − 60) = 30 ÷ 40 = **%75**

Yakalama oranı asıl metriğimiz; "mükemmel bir tahminin sağlayacağı faydanın ne kadarını yakalayabildik?" sorusunu cevaplıyor.

## Veri

Veriler, Fraunhofer ISE'nin [Energy-Charts API](https://api.energy-charts.info/)'sinden Almanya-Lüksemburg (DE-LU) teklif bölgesi için day-ahead elektrik fiyatları olarak çekiliyor (EUR/MWh). Veri Ocak 2024'ten başlıyor; Eylül 2025'e kadar saatlik, Ekim 2025'ten itibaren Avrupa piyasasının geçişiyle birlikte 15 dakikalık çözünürlükte. Tutarlılık için tüm seri dbt'de saatlik ortalamaya dönüştürülüyor.