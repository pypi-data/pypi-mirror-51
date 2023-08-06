# django-drf-autoview
Expose CRUD DRF compatible api's for any django model with one line. 
This patten can be used to quickly bootstrap an api server app based on django DRF. 


Example 

    # Add below snippet in api.py of the django app
    from drf_autoview.api import get_api_views_with_all_fields_readonly
    api_views = get_api_views_with_all_fields_readonly([
        models.DemoModel,
    ])
    
    # Add below snippet in site/api.py
    from drf_autoview.api import register_with_router
    def get_router():
        _router = routers.DefaultRouter()
        _apps = filter(lambda x: '<appName>' in x[1].name, apps.app_configs.items())
        for _app_name, _app_obj in _apps:
            if module_has_submodule(_app_obj.module, 'api'):
                api = import_module('{0}.api'.format(_app_obj.module.__name__))
                register_with_router(_router, api.api_views)
        return _router
    router = get_router()
    