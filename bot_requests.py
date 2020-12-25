import Classes.DB_class as DataTool

def add_worker(params): # Передается 6 параметров
    name, is_conf, contact, edu, post_id, workplace_id = (item for item in params)
    if not(is_conf == "0" or is_conf == "1"):
        return "Параметр(2) `Нал. Конф. Инф.` должен быть 0 или 1."
    if not post_id.isdigit:
        return "Параметр(5) `ID зарплаты` должен быть числом."
    if not workplace_id.isdigit:
        return "Параметр(6) `ID место работы` должено быть числом."
    # Выполняется, если все данные впорядке
    db = DataTool.DataBase()

    post_id = int(post_id)
    workplace_id = int(workplace_id)
    current_post_id = db.get_id("post")
    current_workplace_id = db.get_id("workplace")
    error = ""
    try:
        current_post_id.index(post_id)
    except ValueError:
         error = "Должности с `id {}` не существует\n".format(post_id)
    try:
        current_workplace_id.index(workplace_id)
    except ValueError:
        return error + "Работы с `id {}` не существует".format(workplace_id)

    table_params = ["name", "is_confidential", "contacts", "education", "post_id", "workplace_id"]
    db.add_item("workers", params, table_params)

def add_workplace(params): # Передается 3 параметра
    monitor, level, address = (item for item in params)
    if not(monitor == "0" or monitor == "1"):
        return "Параметр(1) `монитор` должен быть 0 или 1."
    if not level.isdigit:
        return "Параметр(2) `этаж` должен быть числом."
    # Выполняется, если все данные впорядке
    db = DataTool.DataBase()
    table_params = ["monitor", "level", "address"]
    db.add_item("workplace", params, table_params)

def add_post(params): # Передается 3 параметра
    name, salary, vacancy_rate = (item for item in params)
    if not(vacancy_rate == "0" or vacancy_rate == "1"):
        return "Параметр(2) `вакантность` должен быть 0 или 1."
    if not salary.isdigit:
        return "Параметр(3) `оклад` должен быть числом."
    # Выполняется, если все данные впорядке
    db = DataTool.DataBase()
    table_params = ["name", "salary", "vacancy_rate"]
    db.add_item("post", params, table_params)

def select_worker(id = None):
    if id is not None:
        if not id.isdigit:
            return "ID должен быть числом"
    # Выполняется, если все данные впорядке
    db = DataTool.DataBase()

    current_post_id = db.get_id("workers")
    if id is not None:
        try:
            current_post_id.index(int(id))
        except ValueError:
            return "Сотрудника с `id {}` не существует\n".format(id)
    text = "**Все сотрудники**\n"
    if id is None:
        result = db.select_item("workers")
        for worker in result:
            post = db.select_item("post", worker[5])[0]
            post_name = post[1]
            post_salary = post[2]
            is_conf = "Нету"
            if worker[2] == 1:
                is_conf = "Есть"
            text += "ID: {}\nСотрудник: {}\nНаличие конфидициальных данных: {}\nКонтакты: {}\nОбразование: {}\n\n".format(
                worker[0], worker[1], is_conf, worker[3], worker[4]
            )
            text += "Работает на должности {} с зарплатой {} рублей.\n------------------------\n".format(post_name, post_salary)
        return text

    result = db.select_item("workers", id)[0]
    post = db.select_item("post", result[5])[0]
    post_name = post[1]
    post_salary = post[2]
    is_conf = "Нету"
    if result[2] == 1:
        is_conf = "Есть"
    text = "ID: {}\nСотрудник: {}\nНаличие конфидициальных данных: {}\nКонтакты: {}\nОбразование: {}\n\n".format(
        result[0], result[1], is_conf, result[3], result[4]
    )
    text += "Работает на должности {} с зарплатой {} рублей.".format(post_name, post_salary)
    return text

def select_posts(id = None):
    db = DataTool.DataBase()
    text = "**Все должности**\n"
    result = db.select_item("post")
    for item in result:
        is_conf = "Нет"
        if item[3]== 1:
            is_conf = "Требуются"
        text += "ID: {}\nНазвание должности: {}\nОклад: {}\nВакантность: {}\n------------------------------\n\n".format(
            item[0], item[1], item[2], is_conf
        )
    return text

def select_workplace(id = None):
    db = DataTool.DataBase()
    text = "**Места работы**\n"
    result = db.select_item("workplace")
    for item in result:
        is_conf = "Нет"
        if item[1]== 1:
            is_conf = "Есть монитор"
        text += "ID: {}\nНаличие монитора : {}\nАдрес: {}\nЭтаж: {}\n------------------------------\n\n".format(
            item[0], is_conf, item[3], item[2]
        )
    return text
