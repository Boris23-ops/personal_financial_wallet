class Record:
    '''Класс записи о доходах и расходах'''

    def __init__(
            self, date: str, category: str, amount: int, description: str
    ):
        '''Инициализирует объект записи по заданным параметрам.'''
        self.date: str = date
        self.category: str = category
        self.amount: int = amount
        self.description: str = description


class RecordManager:
    '''Класс записей'''

    def __init__(self):
        '''Инициализирует объект менеджера записей.'''
        self.records: list[Record] = []

    def load_records(self, filename: str) -> None:
        '''Загружает записи из файла и добавляет их в список записей.'''
        with open(filename, 'r', encoding='utf-8') as file:
            lines: list[str] = file.readlines()
            for i in range(0, len(lines), 4):
                date: str = lines[i].strip().split(': ')[1]
                category: str = lines[i+1].strip().split(': ')[1]
                amount: int = int(lines[i+2].strip().split(': ')[1])
                description: str = lines[i+3].strip().split(': ')[1]
                record: Record = Record(date, category, amount, description)
                self.records.append(record)

    def save_records(self, filename: str) -> None:
        '''Сохраняет текущие записи в файл.'''
        with open(filename, 'w', encoding='utf-8') as file:
            for record in self.records:
                file.write("Дата: " + record.date + "\n")
                file.write("Категория: " + record.category + "\n")
                file.write("Сумма: " + str(record.amount) + "\n")
                file.write("Описание: " + record.description + "\n")

    def display_balance(self) -> None:
        '''Отображает текущий баланс, доходы и расходы.'''
        total_income: int = sum(
            record.amount
            for record in self.records if record.category == "Доход"
        )
        total_expense: int = sum(
            record.amount
            for record in self.records if record.category == "Расход"
        )
        total_balance: int = total_income - total_expense
        print(
            f"Текущий баланс: {total_balance}\n"
            f"Доходы: {total_income}\n"
            f"Расходы: {total_expense}"
        )

    def add_record(self, new_record: Record) -> None:
        '''Добавляет новую запись.'''
        self.records.append(new_record)

    def edit_record(self, index: int, new_record: Record) -> None:
        '''Редактирует существующую запись по индексу.'''
        if 0 <= index < len(self.records):
            self.records[index] = new_record
            print("Запись успешно изменена.")
        else:
            print("Индекс записи некорректный.")

    def search_records(
            self, category: str, date: str, amount: int
    ) -> list[Record]:
        '''Ищет записи по заданным критериям.'''
        return [record for record in self.records if
                (not category or record.category == category) and
                (not date or record.date == date) and
                (amount is None or record.amount == amount)]


def display_menu() -> None:
    '''Меню ввода'''
    print("1. Вывод баланса")
    print("2. Добавление записи")
    print("3. Редактирование записи")
    print("4. Поиск по записям")


def process_choice(choice: str, record_manager: RecordManager) -> None:
    '''Выбор функции'''
    if choice == '1':
        record_manager.display_balance()
    elif choice == '2':
        add_record_menu(record_manager)
    elif choice == '3':
        edit_record_menu(record_manager)
    elif choice == '4':
        search_records_menu(record_manager)
    else:
        print("Некорректный выбор. Попробуйте снова.")


def add_record_menu(record_manager: RecordManager) -> None:
    '''Добавление данных'''
    date: str = input("Введите дату (гггг-мм-дд): ")
    category: str = input("Введите категорию (Доход/Расход): ").capitalize()
    amount: int = int(input("Введите сумму: "))
    description: str = input("Введите описание: ")
    new_record: Record = Record(date, category, amount, description)
    record_manager.add_record(new_record)
    record_manager.save_records("data.txt")


def edit_record_menu(record_manager: RecordManager) -> None:
    '''Редактирования данных'''
    index: int = int(input("Введите номер записи для редактирования: "))
    date: str = input("Введите новую дату (гггг-мм-дд): ")
    category: str = input(
        "Введите новую категорию (Доход/Расход): "
    ).capitalize()
    amount: int = int(input("Введите новую сумму: "))
    description: str = input("Введите новое описание: ")
    new_record: Record = Record(date, category, amount, description)
    record_manager.edit_record(index, new_record)
    record_manager.save_records("data.txt")


def search_records_menu(record_manager: RecordManager) -> None:
    '''Поиск'''
    category: str = input(
        "Введите категорию для поиска (Доход/Расход) или нажмите Enter: "
    ).capitalize()
    date: str = input("Введите дату для поиска или нажмите Enter: ")
    amount: str = input("Введите сумму для поиска или нажмите Enter: ")
    search_results = record_manager.search_records(
        category, date, int(amount) if amount else None
    )
    for result in search_results:
        print(result)


# Основной цикл программы
record_manager = RecordManager()
record_manager.load_records("data.txt")

while True:
    display_menu()
    choice: str = input("Выберите действие (1-4): ")
    process_choice(choice, record_manager)
