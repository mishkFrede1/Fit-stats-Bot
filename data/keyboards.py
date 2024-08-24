from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Reply keyboards:
gender_choice = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Женский"), KeyboardButton(text="Мужской")]
    ], resize_keyboard=True, one_time_keyboard=True, is_persistent=False
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="О боте ℹ️"), KeyboardButton(text="Расписание тренировок 🗓")],
        [KeyboardButton(text="Друзья 👥"), KeyboardButton(text="Запись наблюдений ✏️")],
        [KeyboardButton(text="Личный кабинет 👤"), KeyboardButton(text="Прогресс и Статистика 📈")]
    ], resize_keyboard=True
)

account_settings = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мои данные 📋"), KeyboardButton(text="Изменить персональные данные ⚙️")],
        [KeyboardButton(text="Назад ⬅️"), KeyboardButton(text="Удалить аккаунт ❌")]
    ], resize_keyboard=True
)

schedule_settings = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Тренировки 🏋️"), KeyboardButton(text="Добавить тренировку ➕")],
        [KeyboardButton(text="Назад ⬅️"), KeyboardButton(text="Настройки оповещений 🔔")]
    ], resize_keyboard=True
)

stats = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Качество сна 🛌"), KeyboardButton(text="Калории 🥪")],
        [KeyboardButton(text="Назад ⬅️"), KeyboardButton(text="Измерения 📏")]
    ], resize_keyboard=True
)

goal_set = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Снижение веса"), KeyboardButton(text="Набор веса")],
        [KeyboardButton(text="Удержание веса")]
    ], resize_keyboard=True, one_time_keyboard=True, is_persistent=False
)

new_training = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Настройки тренировки ⚙️"), KeyboardButton(text="Добавить день ➕")],
        [KeyboardButton(text="Отмена ❌"), KeyboardButton(text="Добавить упражнение ➕")],
        [KeyboardButton(text="Подтвердить ✔️")]
    ], resize_keyboard=True
)

training_types = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Силовая тренировка 🏋️"), KeyboardButton(text="Кардио тренировка 🏃")],
        [KeyboardButton(text="Гибкость и растяжка 🤸")]
    ], resize_keyboard=True
)

exercise_types = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Силовое упражнение 🏋️"), KeyboardButton(text="Кардио упражнение 🏃")],
        [KeyboardButton(text="Для растяжки 🤸")]
    ], resize_keyboard=True
)

records_settings = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Новая запись ➕"), KeyboardButton(text="Все записи 📝")],
        [KeyboardButton(text="Назад ⬅️")]
    ], resize_keyboard=True
)

new_record_params = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Тренировка 🏋️")],
        [KeyboardButton(text="Затраченное время ⌛️"), KeyboardButton(text="Замеры 📏")],
        [KeyboardButton(text="Сон 🛌"), KeyboardButton(text="Самочувствие ❤️")],
        [KeyboardButton(text="Калории 🍽"), KeyboardButton(text="Комментарий/Заметка ✍️")],
        [KeyboardButton(text="Удалить запись ❌"), KeyboardButton(text="Добавить запись ✔️")]
    ], resize_keyboard=True
)

months = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Январь"), KeyboardButton(text="Февраль"), KeyboardButton(text="Март")],
        [KeyboardButton(text="Апрель"), KeyboardButton(text="Май"), KeyboardButton(text="Июнь")],
        [KeyboardButton(text="Июль"), KeyboardButton(text="Август"), KeyboardButton(text="Сентябрь")],
        [KeyboardButton(text="Октябрь"), KeyboardButton(text="Ноябрь"), KeyboardButton(text="Декабрь")]
    ], resize_keyboard=True
)

friends = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить друга ➕"), KeyboardButton(text="Список друзей 👥")],
        [KeyboardButton(text="Назад ⬅️"), KeyboardButton(text="Настройки приватности 🔐")]
    ], resize_keyboard=True
)








# Inline keyboards:
delete_account = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да ✔️", callback_data="YesDeleteAcc"), InlineKeyboardButton(text="Нет ❌", callback_data="NoDeleteAcc")]
    ]
)

change_account = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пол", callback_data="genderChange"), InlineKeyboardButton(text="Возраст", callback_data="ageChange")],
        [InlineKeyboardButton(text="Вес", callback_data="weightChange"), InlineKeyboardButton(text="Рост", callback_data="heightChange")],
        [InlineKeyboardButton(text="Направление", callback_data="goalChange")],
        [InlineKeyboardButton(text="Изменить все", callback_data="allChange")]
    ]
)

registration_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Зарегистрироваться", callback_data="reg")]
    ]
)

training_days = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Понедельник", callback_data="monday"), InlineKeyboardButton(text="Вторник", callback_data="tuesday")],
        [InlineKeyboardButton(text="Среда", callback_data="wednesday"), InlineKeyboardButton(text="Четверг", callback_data="thursday")],
        [InlineKeyboardButton(text="Пятница", callback_data="friday"), InlineKeyboardButton(text="Суббота", callback_data="saturday")],
        [InlineKeyboardButton(text="Воскресенье", callback_data="sunday"), InlineKeyboardButton(text="Все дни", callback_data="alldays")]
    ]
)

training_params = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Время тренировки 🕘", callback_data="training_time"), InlineKeyboardButton(text="Тип тренировки 🏋️", callback_data="training_type")],
        [InlineKeyboardButton(text="Название тренировки 📄", callback_data="training_name")]
    ]
)

notifications_params_enabled = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Время ⏰", callback_data="notice_time"), InlineKeyboardButton(text="Отключить ❌", callback_data="notice_off")]
    ]
)

notifications_params_disabled = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Время ⏰", callback_data="notice_time"), InlineKeyboardButton(text="Включить ✔️", callback_data="notice_on")]
    ]
)

calories_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Набранные калории 🍟", callback_data="cal_gained"), InlineKeyboardButton(text="Соженные калории 🏃‍♀️", callback_data="cal_burned")]
    ]
)

record_find_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="По дню", callback_data="find_type_day_"), InlineKeyboardButton(text="По месяцу", callback_data="find_type_month"), InlineKeyboardButton(text="По году", callback_data="find_type_year")],
        [InlineKeyboardButton(text="Поиск по дате", callback_data="find_type_date")]
    ]
)

measurement_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вес", callback_data="measure_type_weight"), InlineKeyboardButton(text="Рост", callback_data="measure_type_height")],
        [InlineKeyboardButton(text="Шея", callback_data="measure_type_neck"), InlineKeyboardButton(text="Грудь", callback_data="measure_type_chest")],
        [InlineKeyboardButton(text="Талия", callback_data="measure_type_weist"), InlineKeyboardButton(text="Бедра", callback_data="measure_type_hips")],
        [InlineKeyboardButton(text="Бицепс", callback_data="measure_type_biceps"), InlineKeyboardButton(text="Икры", callback_data="measure_type_calf")],
    ]
)

friend_find_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="По ID", callback_data="friend_find_id"), InlineKeyboardButton(text="По никнейму", callback_data="friend_find_nick")]
    ]
)

calories_stats_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Набранные 📈", callback_data="stats_gained"), InlineKeyboardButton(text="Сожженные 📉", callback_data="stats_burned")]
    ]
)

measurement_stats_types = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вес", callback_data="measure_stat_weight"), InlineKeyboardButton(text="Рост", callback_data="measure_stat_height")],
        [InlineKeyboardButton(text="Шея", callback_data="measure_stat_neck"), InlineKeyboardButton(text="Грудь", callback_data="measure_stat_chest")],
        [InlineKeyboardButton(text="Талия", callback_data="measure_stat_weist"), InlineKeyboardButton(text="Бедра", callback_data="measure_stat_hips")],
        [InlineKeyboardButton(text="Бицепс", callback_data="measure_stat_biceps"), InlineKeyboardButton(text="Икры", callback_data="measure_stat_calf")],
    ]
)