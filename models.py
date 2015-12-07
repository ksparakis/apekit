from peewee import *

db = SqliteDatabase('apekit.db')

class App(Model):
    created = DateField()
    identifier = CharField(unique=True)
    title = CharField()
    version = CharField()
    developer_name = CharField()
    downloads = BigIntegerField()
    star_rating = FloatField()
    metadata_url = TextField()
    apk_url = TextField()
    apk_local = TextField()

    class Meta:
        database = db


class Permission(Model):
    name = TextField()
    count = IntegerField()

    class Meta:
        database = db


class AppPermission(Model):
    app = ForeignKeyField(App, related_name='app')
    permission = ForeignKeyField(Permission,
        related_name='permission')

    class Meta:
        database = db


class Vulnerability(Model):
    description = CharField()
    # How many apps have this vulnerability?
    count = IntegerField()

    class Meta:
        database = db


class AppVulnerability(Model):
    app = ForeignKeyField(App, related_name='app_vuln')
    vulnerability = ForeignKeyField(Vulnerability,
        related_name='vuln_vuln')
    filename = TextField()
    line_number = IntegerField()
    source_code = TextField()
