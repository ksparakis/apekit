from peewee import *
from models import *
import datetime

class ModelInterface(object):

    def __init__(self):
        self.db = db
        self.db.connect()

        try:
            self.db.create_tables([
                    App,
                    Permission,
                    AppPermission,
                    Vulnerability,
                    AppVulnerability,
                ])
        except:
            pass



    @staticmethod
    def get_instance():
        return model_interface


    def add_apps_to_db(self, app_list):
        """
        Add apps to the db.
        """
        for app_dict in app_list:
            del app_dict["category"]
            del app_dict["free"]
            del app_dict["version_code"]
            del app_dict["installation_size"]
            del app_dict["snapshot_date"]
            app_dict["created"] = datetime.datetime.now()
        with db.atomic():
            App.insert_many(app_list).execute()


    def add_permissions_for_app(self, app_id, permissions_list):
        """
        Add the permissions for an app.
        """
        with db.atomic():
            try:
                app = App.get(App.app_id == app_id)
            except:
                return False
            for name in permissions_list:
                try:    
                    permission = Permission.get(Permission.name == name)
                except:
                    permission = Permission.create(name=name)
                # Update the counts for these permissions.
                Permission.update(count=Permission.count + 1).where(
                    Permission.name == name)
                # Add the relation to the table.
                AppPermission.create(app=app, permission=permission)


    def add_vulnerability_for_app(self, app, vuln_id, filename,
        line_number, source_code):
        try:
            vulnerability = Vulnerability.get(
                Vulnerability.id == vuln_id)
        except:
            return False
        if AppVulnerability.select().where(
            app=app, vulnerability=vulnerability).count() == 0:
                Vulnerability.update(count=Vulnerability.count + 1).where(
                    Vulnerability.id == vuln_id)
        AppVulnerability.create(app=app, vulnerability=vulnerability,
            filename=filename, line_number=line_number,
            source_code=source_code)


model_interface = ModelInterface()