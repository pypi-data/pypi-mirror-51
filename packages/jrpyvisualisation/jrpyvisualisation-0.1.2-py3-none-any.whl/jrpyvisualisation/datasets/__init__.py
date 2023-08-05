import pandas as pd
import pkg_resources

def _load_from_resource(resource_path):
    return pd.read_csv(pkg_resources.resource_filename(__name__,resource_path))

def load_movies():
    resource_path = '/'.join(('data','movies.zip'))
    return _load_from_resource(resource_path) 

def load_bond():
    resource_path = '/'.join(('data','bond.zip'))
    return _load_from_resource(resource_path)
