from peewee import *
import os
from pathlib import Path

default_folder = Path(__file__).resolve().parent.parent.parent / 'report' / 'data'
database = SqliteDatabase(os.path.join(default_folder, 'database.db'))


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Racers(BaseModel):
    key = TextField(null=True)
    name = TextField(null=True)
    team = TextField(null=True)

    class Meta:
        table_name = 'racers'
        primary_key = False


class Time(BaseModel):
    key = TextField(null=True)
    time_diff = IntegerField(null=True)
    time_end = IntegerField(null=True)
    time_start = IntegerField(null=True)
    valid = TextField(null=True)

    class Meta:
        table_name = 'time'
        primary_key = False


def get_list() -> list[tuple]:
    query = (Time
             .select(Time.key, Racers.name)
             .join(Racers, on=(Time.key == Racers.key)))
    result = [(row.get('key'), row.get('name')) for row in query.dicts()]
    return result


def get_report(order: str = 'asc') -> list[tuple]:
    order_by = Time.time_diff.asc() if order == 'asc' else Time.time_diff.desc()
    query = (Time
             .select(Time.key, Time.time_diff, Racers.name, Racers.team)
             .where(Time.valid == 'Time entry is valid')
             .join(Racers, on=(Time.key == Racers.key))
             .order_by(order_by))
    result = [(row.get('key'), row.get('time_diff'), row.get('name'), row.get('team')) for row in query.dicts()]
    return result


def get_racer(key: str) -> list[tuple]:
    query = (Time
             .select(Time.key, Racers.name, Racers.team, Time.time_start, Time.time_end, Time.time_diff, Time.valid)
             .where(Time.key == key)
             .join(Racers, on=(Time.key == Racers.key)))
    result = [(row.get('key'), row.get('name'), row.get('team'), row.get('time_start'), row.get('time_end'),
               row.get('time_diff'), row.get('valid')) for row in query.dicts()]
    return result


if __name__ == "__main__":
    print(get_report('asc'))

