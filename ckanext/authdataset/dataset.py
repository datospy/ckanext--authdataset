import ckan.plugins.toolkit as toolkit
import ckan.plugins as plugins
from logging import getLogger

log = getLogger(__name__)



class PruebaDatasetFormPlugin(plugins.SingletonPlugin,
                             toolkit.DefaultDatasetForm):
    """
    Custom dataset form plugin.
    """

    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'templates')


    _custom_fields = ['valid_from', 'valid_until', 'valid_spatial', 'update_frequency']

    def get_helpers(self):
        return {
            'dpy_get_custom_fields': self._get_custom_fields,
            'dpy_get_custom_fields': self._get_custom_fields,
            'dpy_user_is_admin': self._user_is_admin
        }

    def _get_custom_fields(self):
        return self._custom_text_fields

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def _modify_package_schema_for_edit(self, schema):
        for field_name in self._custom_fields:
            schema[field_name] = [toolkit.get_validator('ignore_missing'),
                    toolkit.get_converter('convert_to_extras')]

    def _modify_package_schema_for_read(self, schema):
        for field_name in self._custom_fields:
            schema[field_name] = [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]

    def create_package_schema(self):
        schema = super(PruebaDatasetFormPlugin, self).create_package_schema()
        self._modify_package_schema_for_edit(schema)
        return schema

    def update_package_schema(self):
        schema = super(PruebaDatasetFormPlugin, self).update_package_schema()
        self._modify_package_schema_for_edit(schema)
        return schema

    def show_package_schema(self):
        schema = super(PruebaDatasetFormPlugin, self).show_package_schema()
        self._modify_package_schema_for_read(schema)
        return schema


#######Para publicar en Privado######

    def before_index(self, pkg_dict):
        data_dict = json.loads(pkg_dict['data_dict'])
        extras_name = set()
        extras_description = set()
        extras_attributes = set()
        extras_values = set()

        for resource in data_dict['resources']:
            log.debug(resource)
            if 'schema' in resource:
                try:
                    schema = json.loads(resource['schema'])
                    for field in schema['fields']:
                        extras_name.add(field['name'])
                        extras_description.add(field['description'])
                except ValueError:
                    log.info("Entry 'schema' is not valid JSON. This should not happen.")
                except KeyError:
                    log.info("JSON Table Schema syntax problem.")

            if 'dynamic' in resource:
                try:
                    for attr in json.loads(resource['dynamic']):
                        extras_attributes.add(attr['key'])
                        extras_values.add(attr['value'])
                except ValueError:
                    log.info("Entry 'dynamic' is not valid JSON. This should not happen.")
                except KeyError:
                    log.info("Syntax problem. 'key' and 'value' are mandatory for each attribute.")

        pkg_dict['extras_name'] = ' '.join(extras_name)
        pkg_dict['extras_description'] = ' '.join(extras_description)
        pkg_dict['extras_attributes'] = ' '.join(extras_attributes)
        pkg_dict['extras_values'] = ' '.join(extras_values)

        return pkg_dict

    def before_view(self, pkg_dict):
        return  pkg_dict

    def _user_is_admin(self, group_id):
        user_id = toolkit.c.userobj.id
        group_admins = toolkit.get_action('member_list')(
            data_dict={'id': group_id, 'object_type': 'user', 'capacity': 'admin'})
        user_is_group_admin = user_id in [user[0] for user in group_admins]
        return user_is_group_admin or self._user_is_sysadmin()


    def _user_is_sysadmin(self):
        user = toolkit.c.user
        user_is_sysadmin = True
        try:
            toolkit.check_access('sysadmin', {'user': user}, {})
        except toolkit.NotAuthorized:
            user_is_sysadmin = False
        return user_is_sysadmin

    	
    def create(self, entity):
        if not self._user_is_sysadmin():
            entity.private = True


    def edit(self, entity):
        if not self._user_is_admin(entity.owner_org):
            entity.private = True