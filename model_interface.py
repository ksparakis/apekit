from peewee import *
from datetime import date

class ModelInterface(object):

    def __init__(self):
        self.db = db
        self.db.connect()
        try:
            self.db.createtables([
                    App,
                    Permission,
                    AppPermission,
                    Vulnerability,
                    AppVulnerability
                ])
        except:
            pass


    @staticmethod
    def get_instance():
        return model_interface


    def add_apps_to_db(app_list):
        """
        Add apps to the db.
        """
        with db.atomic():
            App.insert_many(app_list).execute()


    def add_permissions_for_app(identifier, permissions_list):
        """
        Add the permissions for an app.
        """
        with db.atomic():
            try:
                app = App.get(App.identifier == identifier)
            except AppDoesNotExist:
                return False
            for name in permissions_list
                try:    
                    permission = Permission.get(Permission.name == name)
                except PermissionDoesNotExist:
                    permission = Permission.create(Permission.name == name)
                # Update the counts for these permissions.
                Permission.update(count=Permission.count + 1).where(
                    Permission.name == name)
                # Add the relation to the table.
                AppPermission.create(app=app, permission=permission)


    def add_vulnerability_for_app(app, vuln_id, filename,
        line_number, source_code):
        try:
            vulnerability = Vulnerability.get(
                Vulnerability.id == vuln_id)
        except VulnerabilityDoesNotExist:
            return False
        Vulnerability.update(count=Vulnerability.count + 1).where(
            Vulnerability.id == vuln_id)
        AppVulnerability.create(app=app, vulnerability=vulnerability,
            filename=filename, line_number=line_number,
            source_code=source_code)


model_interface = ModelInterface()