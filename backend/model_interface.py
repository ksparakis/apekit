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
        except Exception as e:
            print e

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
            query = Permission.update(count=Permission.count + 1).where(
                Permission.name == name)
            query.execute()
            # Add the relation to the table.
            AppPermission.create(app=app, permission=permission)


    def add_vulnerability_for_app(self, app, vuln_id, filename,
        line_number, source_code):
        try:
            vulnerability = Vulnerability.get(
                Vulnerability.id == vuln_id)
        except:
            return False
        count = AppVulnerability.select().where(AppVulnerability.app ==
            app, AppVulnerability.vulnerability == vulnerability).count()
        if count == 0:
            query = Vulnerability.update(count=Vulnerability.count + 1).where(
                Vulnerability.id == vuln_id)
            query.execute()
        AppVulnerability.create(app=app, vulnerability=vulnerability,
            filename=filename, line_number=line_number,
            source_code=source_code)


    def get_num_apps(self):
        return App.select().count()


    def get_app_for_id(self, a_id):
        try:
            app = App.get(App.id == a_id)
        except:
            return False
        return app


    def get_vulnerabilities_and_descriptions(self):
        vulns = []
        for v in Vulnerability.select().order_by(Vulnerability.count.desc()):
            vulns.append([v.description, v.count])
        return vulns


model_interface = ModelInterface()