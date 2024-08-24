from aiogram import Router
from fsm import (
    record_spent_time_fsm,
    registration_fsm, 
    add_day_fsm,
    notifications_time_fsm,
    add_exercise_fsm,
    new_training_fsm,
    record_training_fsm,
    record_health_fsm,
    record_comment_fsm,
    record_calories_fsm,
    records_find_fsm,
    change_acc_options,
    record_measurements_fsm,
    add_friend_fsm,
    record_sleep_fsm
)

fsmRouter = Router()

fsmRouter.include_routers(
    registration_fsm.router,
    add_day_fsm.router,
    notifications_time_fsm.router,
    add_exercise_fsm.router,
    new_training_fsm.router,
    record_spent_time_fsm.router,
    record_training_fsm.router,
    record_health_fsm.router,
    record_comment_fsm.router,
    record_calories_fsm.router,
    records_find_fsm.router,
    change_acc_options.router,
    record_measurements_fsm.router,
    add_friend_fsm.router,
    record_sleep_fsm.router
)
