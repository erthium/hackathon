# Notes

Takım İsmi
GitHub Kullanıcı İsimleri

Yarışma başladığında:
- Takım için Organizasyon içinde repo oluşturulacak
- 
- Takım üyeleri bu repo'ya erişim alacak, takım üyeleri diğer repoları görememeli
- Her repoya WebHook tanımlanacak, main'e her `release-` ile başlayan branch push edildiğinde WebHook çalışacak

Backend:
- Release webhook'u alacak, release'yi kontrol edecek, onaylayacak veya reddedecek

Engine:
- Release verildikten sonra, çalışıp çalışmayacağını kontrol edecek, çalışırsa sonucu dönecek
- Yarışma bittikten sonra, template'a göre bütün release'leri alacak, çalıştıracak, sonucu dönecek
- Websocket bağlantısı üzerine düşünülecek

Engine Structure:
- FastAPI backend, backend'den request alıp, sonucu dönecek vs
- Request geldiğinde docker'ı triggerlayacak
- 

2 farklı yarışma tipi
- agent based (başlangıçta buna odaklanıyoruz)
- model accuracy/evaluation based

Template sistemi:
- Öyle bir engine olacak ki, swords & sandals gibi de, satranç gibi de bir agent based yarışmayı supportlayacak, template'ı biz oluşturup verdiğimizde çalışacak
