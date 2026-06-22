import sys
from game import generate_secret_number, play_round
from db import init_db, save_score, get_top_scores, clear_scores, get_player_best


RANGES = {
    "1": (1, 100),
    "2": (1, 50),
    "3": (1, 200),
    "4": (1, 1000),
}


def show_menu():
    print("\n=== Угадай число ===")
    print("1. Играть")
    print("2. Таблица рекордов")
    print("3. Мой лучший результат")
    print("4. Очистить таблицу рекордов")
    print("5. Выход")
    print("====================")


def run_game():
    player_name = input("Введите ваше имя: ").strip()
    if not player_name:
        print("Имя не может быть пустым.")
        return

    print("\nВыберите диапазон:")
    print("1. 1-100  (стандарт)")
    print("2. 1-50   (легко)")
    print("3. 1-200  (сложно)")
    print("4. 1-1000 (легенда)")

    choice = input("Ваш выбор [1]: ").strip()
    min_n, max_n = RANGES.get(choice, (1, 100))

    secret = generate_secret_number(min_n, max_n)
    print(f"\nЯ загадал число от {min_n} до {max_n}. Попробуйте угадать!")

    attempts = play_round(secret, min_n, max_n)
    save_score(player_name, attempts, min_n, max_n)
    print("Результат сохранён!")


def show_top_scores():
    scores = get_top_scores(10)
    if not scores:
        print("\nТаблица рекордов пуста.")
        return
    print("\n=== Таблица рекордов (топ 10) ===")
    print(f"{'#':<4} {'Игрок':<20} {'Попытки':<10} {'Диапазон':<15} Дата")
    print("-" * 65)
    for i, (name, att, min_n, max_n, created_at) in enumerate(scores, 1):
        date_str = created_at[:10] if created_at else "—"
        print(f"{i:<4} {name:<20} {att:<10} {min_n}-{max_n:<11} {date_str}")


def show_player_best():
    player_name = input("Введите имя игрока: ").strip()
    if not player_name:
        print("Имя не может быть пустым.")
        return
    row = get_player_best(player_name)
    if row:
        name, att, min_n, max_n, created_at = row
        date_str = created_at[:10] if created_at else "—"
        print(f"\nЛучший результат {name}: {att} попыток (диапазон {min_n}-{max_n}, {date_str})")
    else:
        print(f"\nИгрок '{player_name}' не найден.")


def main():
    init_db()
    while True:
        show_menu()
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            run_game()
        elif choice == "2":
            show_top_scores()
        elif choice == "3":
            show_player_best()
        elif choice == "4":
            confirm = input("Очистить таблицу рекордов? (да/нет): ").strip().lower()
            if confirm == "да":
                clear_scores()
                print("Таблица очищена.")
            else:
                print("Отмена.")
        elif choice == "5":
            print("До свидания!")
            sys.exit(0)
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()


