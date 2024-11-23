import app
from app.utils import is_valid_url

if __name__ == "__main__":
    print("Добро пожаловать в MatchMiner!")
    print("Введите ссылки формата https://www.flashscorekz.com/match/<ID>/#/match-summary.")
    print("Введите ссылки по одной. Напишите 'break', чтобы завершить.")

    links = []

    while True:
        try:
            link = input("Введите ссылку: ").strip()
            if link == "break":
                break

            if is_valid_url(link):
                links.append(link)
                print("Ссылка добавлена!")
            else:
                print("Неверный формат ссылки. Попробуйте снова.")
        except Exception as e:
            print(f"Ошибка ввода: {e}. Попробуйте снова.")


    if links:
        print("Программа начинает парсинг страниц, в консоли могут быть ошибки, не пугайтесь!")

        app.run(links)

        print("MatchMiner завершил свою работу. Данные сохранены в файл!")
    else:
        print("Вы не ввели ни одной ссылки")

    input("Нажмите Enter чтобы закрыть программу")