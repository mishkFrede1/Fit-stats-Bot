from aiogram import Router
from handlers import (
    menu_buttons,
    back_button,
    training_delete,
    training_exercises_info,
    trainings_schedule,
    add_training_button,
    cancel_button,
    accept_button,
    training_options_button,
    training_info,
    notifications_button,
    notifications_on_off,
    new_record_button,
    cancel_note_button,
    add_record_button,
    records_info,
    base_commands,
    account_settings_buttons,
    friend_info,
    stats_graphs
)

handlersRouter = Router()

handlersRouter.include_routers(
    base_commands.router,
    back_button.router,
    account_settings_buttons.router,
    add_training_button.router,
    cancel_button.router,
    accept_button.router,
    training_options_button.router,
    trainings_schedule.router,
    training_delete.router,
    training_info.router,
    notifications_button.router,
    notifications_on_off.router,
    training_exercises_info.router,
    new_record_button.router,
    cancel_note_button.router,
    add_record_button.router,
    records_info.router,
    menu_buttons.router,
    friend_info.router,
    stats_graphs.router
)