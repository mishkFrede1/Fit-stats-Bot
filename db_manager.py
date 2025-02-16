from psycopg2.pool import SimpleConnectionPool
from datetime import time
from datetime import date

class Manager():
    connection_pool = SimpleConnectionPool(
        1, 20, 
        user='postgres',
        password='1707',
        host='127.0.0.1',
        database='accounts'
    )

    def get_connection_from_pool(self) -> any:
        """
        Return connection from the pool of DB.

        :return:
        """
        try:
            conn = self.connection_pool.getconn()
            return conn
        
        except Exception as _ex:
            print("[ERROR]", _ex)
            return None
        
    def put_connection_in_pool(self, conn):
        """
        Return connection back in the pool of DB.
        """
        try:
            self.connection_pool.putconn(conn)

        except Exception as _ex:
            print("[ERROR]", _ex)

    def release_db_connection(self, conn):
        try:
            self.connection_pool.putconn(conn)

        except Exception as _ex:
            print("[ERROR]:", _ex)

    def user_exists(self, user_id: int) -> bool:
        """
        Checks if the user is in the Database by his Telegram ID.

        :param user_id: User's Telegram ID.
        :return:
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s);
                    """, 
                    (user_id,)
                )
                exists = cursor.fetchone()[0]
                return(exists)
            
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def upload_registration_data(
            self, 
            user_id: int, 
            registered_at, 
            first_name: str, 
            username: str, 
            gender_female: bool, 
            age: int, 
            weight: int, 
            height: int, 
            goal: str
    ):
        """
        Insert user's data in DB.

        :param user_id: User's Telegram ID.
        :param registered_at: Date of registration.
        :param first_name: User's Telegram first name.
        :param username: Unique Telegram username.
        :param gender_female: Is the User a woman.
        :param age: User's full age.
        :param weight: User's weight in kg.
        :param height: User's height in cm.
        :param goal: User's goal.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (user_id, registered_at, first_name, username, gender_female, age, weight, height, goal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, 
                    (user_id, registered_at, first_name, username, gender_female, age, weight, height, goal,)
                )
                print("[INFO] Успешная запись данных:", user_id, username, gender_female, age, weight, height, goal)

        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def delete_record(self, record_id: int):
        """
        Delete User record from DB by record ID.

        :param record_id: Record unique ID.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM records WHERE record_id = %s;
                    """, 
                    (record_id,)
                )
            print(f"[INFO] Успешное удаление: {record_id}")
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def delete_training(self, training_id: int):
        """
        Delete User's training from DB by training's ID.

        :param training_id: Training unique ID.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM schedules WHERE training_id = %s;
                    """, 
                    (training_id,)
                )
            print(f"[INFO] Успешное удаление: {training_id}")
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)
    
    def delete_user(self, user_id: int):
        """
        Delete User from DB by Telegram ID.

        :param user_id: User's Telegram ID.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute("""DELETE FROM users WHERE user_id = %s;""", (user_id,))
                cursor.execute("""DELETE FROM schedules WHERE user_id = %s;""", (user_id,))
                cursor.execute("""DELETE FROM records WHERE user_id = %s;""", (user_id,))
                print(f"[INFO] Успешное удаление: {user_id}")
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def upload_exercise(self, exercise: list, user_id: int):
        """
        Upload new exercise in DB.

        :param exercise: List of exercise params.
        :param user_id: User's Telegram ID.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO schedules exercises = %s WHERE user_id = %s;
                    """, 
                    (exercise, user_id,)
                )
                print("[INFO] Успешная запись данных")
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def upload_training(
            self, 
            user_id: int, 
            first_name: str, 
            username: str, 
            days: list, 
            training_time: time, 
            training_type: str, 
            exercises: list,
            training_name: str):
        """
        Upload new training in DB.

        :param user_id: User's Telegram ID.
        :param first_name: User's Telegram first name.
        :param username: Unique Telegram username.
        :param days: List of training's days.
        :param training_time: Time of training starts.
        :param training_type: Type of training.
        :param exercises: List of exercises.
        :param training_name: Name of training.

        :return:
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO schedules (user_id, first_name, username, days, training_time, training_type, exercises, training_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, 
                    (user_id, first_name, username, days, training_time, training_type, exercises, training_name,)
                )
                cursor.execute(
                    """
                    SELECT * FROM schedules WHERE user_id = %s
                    """, 
                    (user_id,)
                )
                data = cursor.fetchall()

                print("[INFO] Успешная запись данных")
                return data[len(data) - 1][6]
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def upload_record(
            self, 
            user_id: int, 
            first_name: str, 
            username: str, 
            date: date, 
            training_type: str, 
            exercises: list,
            time_spent: int,
            state_of_health: str,
            note: str,
            burned_cal: int,
            gained_cal: int,
            measurements: list,
            sleep: int
        ):
        """
        Upload new record in DB.

        :param user_id: User's Telegram ID.
        :param first_name: User's Telegram first name.
        :param username: Unique Telegram username.
        :param date: Date of day. `date` type object.
        :param training_type: Type of training.
        :param exercises: List of exercises.
        :param time_spent: Time spent on training in minutes.
        :param state_of_health: A note on the state of health.
        :param note: Note about the day.
        :param burned_cal: Number of calories burned
        :param gained_cal: Number of calories gained
        :param measurments: List of measurments.
        :param sleep: Hours of night sleep.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO records (user_id, first_name, username, date, training_type, exercises, time_spent, state_of_health, note, burned_cal, gained_cal, measurements, sleep) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, 
                    (user_id, first_name, username, date, training_type, exercises, time_spent, state_of_health, note, burned_cal, gained_cal, measurements, sleep,)
                )

                print("[INFO] Успешная запись данных:", user_id, first_name, username, date, training_type, exercises, time_spent, state_of_health, note, burned_cal, gained_cal, measurements, sleep)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def upload_friend_list(self, user_id: int, friends: list):
        """
        Upload new user friend in DB.

        :param user_id: User Telegram ID.
        :param friends: List of friends Telegram ID.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users SET friends = %s WHERE user_id = %s;
                    """, 
                    (friends, user_id,)
                )
                print("[INFO] Успешная запись данных", friends, user_id)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_all_user_id(self) -> list:
        """
        Return all Telegram ID's from DB in `list`. 

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT user_id FROM users;
                    """
                )
                data = cursor.fetchall()
                return(data)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)
    
    def get_user_data(self, user_id: int) -> tuple:
        """
        Return User's data by Telegram ID from DB. 
        
        :param user_id: User's Telegram ID.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM users WHERE user_id = %s;
                    """, 
                    (user_id,)
                )
                data = cursor.fetchone()
                return(data)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_user_data_by_username(self, username: str) -> tuple:
        """
        Return User's data by username. 
        
        :param username: Telegram username.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM users WHERE username = %s;
                    """, 
                    (username,)
                )
                data = cursor.fetchone()
                return(data)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_notice_time(self, user_id: int) -> int:
        """
        Return User's notice time in minutes by Telegram ID. 

        :param user_id: User's Telegram ID.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT notifications_time FROM users WHERE user_id = %s;
                    """, 
                    (user_id,)
                    )
                data = cursor.fetchone()
                return(data[0])
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_records(self, user_id: int, date_type="none", date_val=None) -> tuple | list:
        """
        Return user records data. 

        :param user_id: User's Telegram ID.
        :param date_type: Type of date filter.
        :param date_val: Filter value of date.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM records WHERE user_id = %s;
                    """,
                    (user_id,)
                )
                data = cursor.fetchall()

                if date_type == "none":
                    return(data)
                elif date_type == "day":
                    result = []
                    for record in data:
                        date = record[4]
                        if date.day == date_val: result.append(record)
                elif date_type == "month":
                    result = []
                    for record in data:
                        date = record[4]
                        if date.month == date_val: result.append(record)
                elif date_type == "year":
                    result = []
                    for record in data:
                        date = record[4]
                        if date.year == date_val: result.append(record)
                else:
                    result = []
                    for record in data:
                        date = record[4]
                        if date == date_val: result.append(record)

                return result

        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_record(self, record_id: int) -> tuple:
        """
        Return record's data in `tuple` by record ID. 

        :param record_id: Record unique ID.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM records WHERE record_id = %s;
                    """, 
                    (record_id,)
                )
                data = cursor.fetchone()
                return(data) #Tuple
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_training(self, training_id: int) -> tuple:
        """
        Return training's data in `tuple` by training ID. 

        :param training_id: Training unique ID.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM schedules WHERE training_id = %s;
                    """, 
                    (training_id,)
                )
                data = cursor.fetchone()
                return(data) #Tuple
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_training_time(self, training_id: int) -> tuple:
        """
        Return training's time in `tuple` by training ID. 

        :param training_id: Training unique ID.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT training_time FROM schedules WHERE training_id = %s;
                    """, 
                    (training_id,)
                )
                data = cursor.fetchone()
                return(data)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_user_notice(self, user_id: int) -> bool:
        """
        Return `bool` value of the user's on/off notifications in DB.

        :param user_id: User's Telegram ID.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT notifications FROM users WHERE user_id = %s;
                    """, 
                    (user_id,)
                )
                data = cursor.fetchone()
                return(data[0])
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_user_data(self, user_id: int) -> tuple:
        """
        Return User's data from DB.

        :param user_id: User's Telegram ID.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM users WHERE user_id = %s;
                    """, 
                    (user_id,)
                )
                data = cursor.fetchone()
                return(data)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_trainings(self, user_id: int) -> tuple:
        """
        Return list of User's trainings from DB.

        :param user_id: User's Telegram ID.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM schedules WHERE user_id = %s;
                    """, 
                    (user_id,)
                )
                data = cursor.fetchall()
                return(data)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def get_filter_data(self, user_id: int) -> tuple:
        """
        Return list of User's filter records from DB.

        :param user_id: User's Telegram ID.

        :return: 
        """
        conn = self.get_connection_from_pool()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT records_filter_data FROM users WHERE user_id = %s;
                    """, 
                    (user_id,)
                )
                data = cursor.fetchone()
                return(data)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def update_filter_data(self, user_id: int, records: list):
        """
        Update user records filter data in DB.

        :param user_id: User's Telegram ID.
        :param records: List of user filtered records.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users SET records_filter_data = %s WHERE user_id = %s;
                    """, 
                    (records, user_id,)
                )
                print("[INFO] Успешное обновление: records_filter_data", user_id)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def update_privacy_param(self, user_id: int, option: str, value: bool):
        """
        Update one of few User's privacy params in DB.

        :param user_id: User's Telegram ID.
        :param option: Param name.
        :param value: New param value.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE users SET {option} = %s WHERE user_id = %s;
                    """, 
                    (value, user_id,)
                )
                print("[INFO] Успешное обновление:", user_id, option, value)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def update_option(self, user_id: int, option: str, value):
        """
        Update one of few User's options in DB.

        :param user_id: User's Telegram ID.
        :param option: Option name.
        :param value: New option value
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE users SET {option} = %s WHERE user_id = %s;
                    """, 
                    (value, user_id,)
                )
                print("[INFO] Успешное обновление:", user_id, option, value)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def update_all(
            self, 
            user_id: int, 
            gender: bool, 
            age: int, 
            weight: int, 
            height: int, 
            goal: str
        ):
        """
        Update all User's options in DB.

        :param user_id: User's Telegram ID.
        :param gender_female: Is the User a woman.
        :param age: User's full age.
        :param weight: User's weight in kg.
        :param height: User's height in cm.
        :param goal: User's goal.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE users
                    SET gender_female = %s,
                        age = %s,
                        weight = %s,
                        height = %s,
                        goal = %s
                    WHERE user_id = %s;
                    """, 
                    (gender, age, weight, height, goal, user_id,)
                )
                print(f"[INFO] Успешное обновление данных:", user_id, gender, age, weight, height, goal)
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def update_notice_on_off(self, user_id: int, notice_value: bool):
        """
        Update notices condition for one User.

        :param user_id: User's Telegram ID.
        :param notice_value: On/Off notifications.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE users SET notifications = %s WHERE user_id = %s;
                    """, 
                    (notice_value, user_id,)
                )
                print("[INFO] Успешное обновление ")
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)

    def update_notice_time(self, user_id: int, new_notice_time: int):
        """
        Update notification time for User.

        :param user_id: User's Telegram ID.
        :param new_notice_time: New notifications time.
        """
        conn = self.get_connection_from_pool()
        conn.autocommit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"""
                    UPDATE users SET notifications_time = %s WHERE user_id = %s;
                    """, 
                    (new_notice_time, user_id,)
                )
                print("[INFO] Успешное обновление ")
        
        except Exception as _ex:
            print("[ERROR]", _ex)
        finally:
            cursor.close()
            self.release_db_connection(conn)