class NmpspeciesRouter(object):
    """
    A router to control all database operations on models in the
    nmpspecies application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read nmpspecies models go to nmpspecies_db.
        """
        if model._meta.app_label == 'nmpspecies':
            return 'nmpspecies_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write nmpspecies models go to nmpspecies_db.
        """
        if model._meta.app_label == 'nmpspecies':
            return 'nmpspecies_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the nmpspecies app is involved.
        """
        if obj1._meta.app_label == 'nmpspecies' or obj2._meta.app_label == 'nmpspecies':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the nmpspecies app only appears in the 'nmpspecies' database.
        """
        if app_label == 'nmpspecies':
            return db == 'nmpspecies_db'
        return None
