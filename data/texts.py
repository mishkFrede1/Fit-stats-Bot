#Bot texts
registration_text = (
    "👋 Привет, {username}!\n\n"

    "Добро пожаловать в нашего бота. Он поможет вам в достижении ваших целей в сфере фитнеса. "
    "С его помощью вы сможете:\n"
    "🔸 Следить за своим прогрессом\n"
    "🔸 Разные рекомендации по каждой категории\n"
    "🔸 Делиться своим прогрессом с другими\n"
    "🔸 Набирать, удерживать или сбрасывать вес\n\n"

    "Для начала работы вас нужно зарегистрировать, для этого нажмите на кнопку и заполните необходимые данные.\n\n"
)

welcome_text = (
    "👋 Рады видеть вас снова, {username}!\n\n"
    
    "Для начала работы выберите нужный раздел ниже. \n"
    "Если у вас возникнут вопросы, то воспользуйтесь командой /help\n\n"
)

user_info_text = (
    "👤 <b>Данные аккаунта</b>:\n\n"

    "<b>ID</b>: {id}\n"
    "<b>Дата регистрации</b> - {date}\n"
    "<b>Пол</b> - {gender}\n"
    "<b>Возраст</b> - {age}\n"
    "<b>Вес</b> - {weight} кг.\n"
    "<b>Рост</b> - {height} см.\n"
    "<b>Цель</b> - {goal}\n"
)

friend_info_text = (
    "👤 <b>Данные о {username}</b>:\n\n"

    "<b>ID</b>: {id}\n"
    "<b>Дата регистрации</b>: {date}\n\n"
    "<b>Пол</b> - {gender}\n"
    "<b>Возраст</b> - {age} {age_ending}\n"
    "<b>Вес</b> - {weight} кг.\n"
    "<b>Рост</b> - {height} см.\n"
    "<b>Цель</b> - {goal}\n\n"
    " "
)

help_text = (
    "⚙️ <b>Все доступные команды для взаимодействия с ботом</b>:\n\n"

    "/start - Начать работу с ботом\n"
    "/reg - Регистрация в боте для начала работы\n"
    "/help - Показать сообщение с перечнем доступных команд\n"
    "/menu - Главное меню со всеми категориями\n"
    "/acc - Настройки вашего аккаунта\n"
    "/sched - Расписание тренировок\n"
    "/stats - Статистика и прогресс\n"
    "/rec - Запись результатов\n"
    "/del - Удаление аккаунта\n"
    "/change - Изменение параметров аккаунта\n"
    "/info - Данные об аккаунте\n"
    "/friends - Меню друзей\n"
    "/about - Информация о боте\n\n"

    "<b>По всем вопросам и ошибкам</b> - t.me/whitePower1"
)

record_info_text = (
    "📋 <b>Запись</b> {day}.{month}.{year}:\n\n"
)

training_info_text = (
    "📋 <b>Данные о тренировке</b>:\n\n"

    "<b>Время тренировки</b>: {t_time}\n"
    "<b>Тип тренировки</b>: {t_type}\n"
    "<b>Дни</b>: {t_days}\n"
)

power_exercise_info_text = (
    "📄 <b>Упражнение {id}</b>:\n\n"

    "<b>Название</b>: {name}\n"
    "<b>Количество подходов</b>: {counts}\n"
    "<b>Тип</b>: {type}\n"
)

stretch_cardio_exercise_info_text = (
    "📄 <b>Упражнение {id}</b>:\n\n"

    "<b>Название</b>: {name}\n"
    "<b>Длительность</b>: {time} {measure}\n"
    "<b>Тип</b>: {type}\n"
)

notice_text = (
    "📢 <b>Не забудьте про тренировку</b>!\n\n"

    "<b>Сегодня у вас</b>: {t_type}\n"
    "<b>Она начнется через</b>: {notice_time} {time_ending}, в {hour}:{minute}\n\n"
    "🤍 <b>Удачи вам</b>!"
)

notice_text_zero = (
    "📢 <b>Не забудьте про тренировку</b>!\n\n"

    "<b>Сегодня у вас</b>: {t_type}\n"
    "<b>Время тренировки</b>: {hour}:{minute}\n\n"
    "🤍 <b>Удачи вам</b>!"
)

bot_info_text = (
    "📃 <b>Данные о боте</b>:\n\n"
    
    "<b>Адрес</b>: @fitsStatsBot\n"
    "<b>Версия бота</b>: {bot_version}\n"
    "<b>Github</b>: <a href='{github}'>Fit Stats Bot</a>\n\n"

    "<b>Телеграм автора</b>: {telegram}\n"
    "<b>ВК автора</b>: {vk}\n\n"
)

updated_data_text = "✔️ <b>Данные обновлены</b>."

day_add_text = "✔️ <b>День успешно добавлен</b>"

days_add_text = "✔️ <b>Все дни успешно добавлены</b>"

#Errors texts:
registration_error_text = "❌ <b>Ошибка</b>: Неправильный формат ввода данных, повторите попытку - /reg"

repeated_registration_error_text = "❌ <b>Вы уже зарегистрированны.</b> Используйте команду /start или /help для помощи в навигации."

unregistered_access_text = "❌ <b>Вы не зарегистрированны в системе.</b> Используйте /reg для регистрации."

delete_error_text = "❌ <b>Ошибка удаления</b>."

incorrect_format_error_text = "❌ <b>Ошибка</b>: Неправильный формат ввода данных."

incorrect_training_params = "❌ <b>Ошибка</b>: Настройки тренировки не были заданы."

all_params_none_error_text = "❌ <b>Ошибка</b>: Все поля записи не могут быть пустыми."

self_add_friend_list = "❌ <b>Ошибка</b>: Вы не можете добавить себя в друзья."

user_is_not_exist = "❌ <b>Ошибка</b>: Такого пользователя не существует."