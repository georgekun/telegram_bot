import random

import aiosqlite

class DatabaseManager:
    async def create_tables(self):
        with open('database.db', "a") as file:
            pass
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS "users" (
                        "username" TEXT,
                        "userid" INT,
                        "country" TEXT,
                        "age" INT,
                        PRIMARY KEY("userid")
                    );""")
            await db.execute("""CREATE TABLE IF NOT EXISTS "services" (
                        "link" TEXT,
                        "country" TEXT,
                        "bottom_sum" INT,
                        "upper_sum" INT,
                        "bottom_term" INT,
                        "upper_term" INT,
                        "procent" INT,
                        "free_procent_if" TEXT,
                        "picture" TEXT,
                        "is_badki" INT,
                        "is_card" INT,
                        "is_yandex" INT,
                        "is_qiwi" INT,
                        "is_contact" INT,
                        "callback" TEXT,
                        PRIMARY KEY("callback")
                        );""")
            await db.commit()

    async def user_exists(self, userid):
        async with aiosqlite.connect('database.db') as db:
            return bool(await (await db.execute("""SELECT userid FROM users WHERE userid == ?""", (int(userid),))).fetchall())

    async def add_user(self, username, userid):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""INSERT INTO users(username, userid, country, age) 
                            VALUES (?, ?, ?, ?)""", (userid, username, None, 0))
            await db.commit()

    async def update_user_settings(self, userid, country, age):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""UPDATE users SET country == ?, age == ? WHERE userid == ?""", (country, age, userid))
            await db.commit()

    async def get_user_settigns(self, userid):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT country, age FROM users WHERE userid == ?""", (userid, ))
            return await ex.fetchone()

    async def get_services(self, country):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT * FROM services WHERE country == ?""", (country,))
            return await ex.fetchall()

    async def get_country_by_link(self, callback):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT country FROM services WHERE callback == ?""", (callback, ))
            return (await ex.fetchone())[0]

    async def get_user_country(self, userid):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT country FROM users WHERE userid == ?""", (userid, ))
            return (await ex.fetchone())[0]

    async def add_service(self, link, country, bottom_sum, upper_sum, bottom_term, upper_term, procent, picture, is_badki,
                          is_card, is_yandex, is_qiwi, is_contact, free_procent_if=None):
        async with aiosqlite.connect('database.db') as db:
            random_chars_part = list("1234567890abcdefGHIGKLMNOPQRSTUVYXWZ")
            random.shuffle(random_chars_part)
            password_chars_part = "".join(
                [random.choice(random_chars_part) for x in range(6)])
            password_number_part = str(random.randint(100000, 999999))
            callback = password_number_part + password_chars_part
            await db.execute("""INSERT INTO services(link, country, bottom_sum, upper_sum, bottom_term, upper_term, procent, free_procent_if, picture, is_badki,
                             is_card, is_yandex, is_qiwi, is_contact, callback) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                             (link, country, bottom_sum, upper_sum, bottom_term, upper_term, procent, free_procent_if, picture, is_badki,
                              is_card, is_yandex, is_qiwi, is_contact, callback))
            await db.commit()

    async def get_service_info(self, callback):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT * FROM services WHERE callback == ?""", (callback, ))
            return await ex.fetchone()

    async def delete_service(self, callback):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""DELETE FROM services WHERE callback == ?""", (callback,))
            await db.commit()

    async def get_popular_services_by_param(self, param, country):
        async with aiosqlite.connect('database.db') as db:
            if param == '0':
                ex = await db.execute("""SELECT * FROM services WHERE (procent == ? or free_procent_if != ?) and country == ?""", (0, None, country))
            elif param == 'badki':
                ex = await db.execute("""SELECT * FROM services WHERE is_badki != ? and country == ?""", (0, country))
            elif param == 'qiwi':
                ex = await db.execute("""SELECT * FROM services WHERE is_qiwi != ? and country == ?""", (0, country))
            elif param == 'yandex':
                ex = await db.execute("""SELECT * FROM services WHERE is_yandex != ? and country == ?""", (0, country))
            elif param == 'contact':
                ex = await db.execute("""SELECT * FROM services WHERE is_contact != ? and country == ?""", (0, country))
            elif param == 'card':
                ex = await db.execute("""SELECT * FROM services WHERE is_card != ? and country == ?""", (0, country))
            elif param == 'all':
                ex = await db.execute("""SELECT * FROM services WHERE country == ?""", (country,))
            res = await ex.fetchall()
            return res

    async def get_services_callbacks_by_param(self, param, country):
        async with aiosqlite.connect('database.db') as db:
            if param == '0':
                ex = await db.execute("""SELECT callback FROM services WHERE (procent == ? or free_procent_if != ?) and country == ?""", (0, None, country))
            elif param == 'badki':
                ex = await db.execute("""SELECT callback FROM services WHERE is_badki != ? and country == ?""", (0, country))
            elif param == 'qiwi':
                ex = await db.execute("""SELECT callback FROM services WHERE is_qiwi != ? and country == ?""", (0, country))
            elif param == 'yandex':
                ex = await db.execute("""SELECT callback FROM services WHERE is_yandex != ? and country == ?""", (0, country))
            elif param == 'contact':
                ex = await db.execute("""SELECT callback FROM services WHERE is_contact != ? and country == ?""", (0, country))
            elif param == 'card':
                ex = await db.execute("""SELECT * FROM services WHERE is_card != ? and country == ?""", (0, country))
            elif param == 'all':
                ex = await db.execute("""SELECT callback FROM services WHERE country == ?""", (0, country))
            res = await ex.fetchall()
            return res

    async def get_link_by_callback(self, callback):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT link FROM services WHERE callback == ?""", (callback, ))
            return (await ex.fetchone())[0]

    async def get_popular_prev_and_next(self, callback, param, country):
        async with aiosqlite.connect('database.db') as db:
            country = await self.get_country_by_link(callback)
            cur_services = list(await self.get_popular_services_by_param(param, country))
            cur_service_info = await self.get_service_info(callback)
            i = cur_services.index(cur_service_info)
            prev_link = (await self.get_service_info(cur_services[(i - 1) % len(cur_services)][-1]))[-1]
            next_link = (await self.get_service_info(cur_services[(i + 1) % len(cur_services)][-1]))[-1]
            return [prev_link, next_link]

    async def get_index_by_callback(self, callback, param, country):
        async with aiosqlite.connect('database.db') as db:
            services = list(await self.get_services_callbacks_by_param(param, country))
            ind = services.index((callback,))
            return ind

    async def get_services_by_param(self, procent, payment):
        async with aiosqlite.connect('database.db') as db:
            payment_condition = f"is_{payment}"
            if procent == '0':
                ex = await db.execute("""SELECT * FROM services WHERE (procent == ? or free_procent_if != ?) and ? == ?""", (0, None, payment_condition, 1))
            else:
                ex = await db.execute("""SELECT * FROM services WHERE ? == ?""", (payment_condition, 1))
            res = await ex.fetchall()
            return res

    async def get_detail_prev_and_next(self, callback, procent, payment):
        async with aiosqlite.connect('database.db') as db:
            country = await self.get_country_by_link(callback)
            cur_services = list(await self.get_services_by_param(procent, payment))
            cur_service_info = await self.get_service_info(callback)
            i = cur_services.index(cur_service_info)
            prev_link = (await self.get_service_info(cur_services[(i - 1) % len(cur_services)][-1]))[-1]
            next_link = (await self.get_service_info(cur_services[(i + 1) % len(cur_services)][-1]))[-1]
            return [prev_link, next_link]

    async def get_users_by_country(self, country):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT userid FROM users WHERE country == ?""", (country,))
            return await ex.fetchall()
