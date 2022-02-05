import requests
from bs4 import BeautifulSoup
import os
speed_boof = 44100

def music_search():
    r = requests.get("https://ru.hitmotop.com/search?q="+ input("Укажите название песни: "))
    soup = BeautifulSoup(r.content, 'lxml')
    tracks_info = soup.findAll('div', class_='track__info')
    musics = []

    for track in tracks_info:
        musics.append({
            'title': track.find('div', class_='track__title').get_text(strip=True,),
            'downloads_link': track.find('a', class_='track__download-btn').get("href")
        })
    for num, music in enumerate(musics, 1):
        print(num, music['title'])
    try:
        downloads_music = int(input("Укажите номер песни: "))
        print("Начинаю загружать песню",musics[downloads_music -1]['title'])
        myCmd = os.popen('wget -O temp.mp3 {0}'.format(musics[downloads_music -1]['downloads_link'])).read()
        print(myCmd)
        print("Начинаю преобразование трека в wav формат.")
        myCmd = os.popen('mpg123 -w temp.wav temp.mp3').read()
        print(myCmd)
    except Exception as exc:
        print("Ошибка:", exc)
def music_translate():
    frequency = input("Укажите необходимую частоту: ")
    print(f"Запустил трек на частоту{frequency}")
    myCmd = os.popen(f'sudo /home/pi/python/radio/PiFm/./pifm temp.wav {frequency} {speed_boof} stereo').read()
    input()
def menu():
    while True:
        print('1.Выбрать песню\n2-Начать вещать песню\n0-Выход')
        try:
            type = int(input('Ответ: '))
            if type == 1:
                music_search()
            elif type == 2:
                music_translate()
            elif type == 0:
                break
        except:
            pass

menu()
