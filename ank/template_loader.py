"""
Template loader for generating new ANK apps.
Centralizes template loading and rendering with consistent placeholders.
"""

__author__ = 'sunary'

import os

from ank.constants import BASE_APP, API_APP, SCHEDULE_APP

# Template directory relative to this module
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

# App types and their template file mappings
APP_TEMPLATES = {
    BASE_APP: {
        'processor': 'baseapp_processor.tpy',
        'services': 'baseapp_services.tpy',
        'settings': 'baseapp_settings.tpy',
        'extra_files': [],
    },
    API_APP: {
        'processor': 'apiapp_processor.tpy',
        'services': 'apiapp_services.tpy',
        'settings': 'apiapp_settings.tpy',
        'extra_files': [
            ('endpoint', 'apiapp_endpoint.tpy'),
        ],
    },
    SCHEDULE_APP: {
        'processor': 'scheduleapp_processor.tpy',
        'services': 'scheduleapp_services.tpy',
        'settings': 'scheduleapp_settings.tpy',
        'extra_files': [],
    },
}

# Shared templates (same for all app types)
SHARED_TEMPLATES = {
    'docker': 'docker.tpy',
    'unittest': 'unittest.tpy',
    'readme': 'readme.tpy',
}


def _load_template(filename):
    """Load template file content."""
    path = os.path.join(TEMPLATES_DIR, filename)
    with open(path, 'r') as f:
        return f.read()


def get_template(app_type, template_key):
    """Get template content for app type and template key."""
    if app_type not in APP_TEMPLATES:
        raise ValueError(f"Unknown app type: {app_type}")
    config = APP_TEMPLATES[app_type]
    filename = config.get(template_key)
    if not filename:
        raise ValueError(f"No template '{template_key}' for {app_type}")
    return _load_template(filename)


def render_app(app_type, project_name, api_port='5372', version='1.6.0'):
    """
    Render all files for a new app. Returns dict of filename -> content.
    Templates use {0}=project_name, {1}=api_port.
    """
    config = APP_TEMPLATES[app_type]
    files = {}

    # Processor
    content = get_template(app_type, 'processor')
    if app_type == API_APP:
        files['processor.py'] = content.format(project_name, api_port)
    else:
        files['processor.py'] = content.format(project_name)

    # Extra files (e.g. endpoint.py for APIApp)
    for file_key, template_file in config.get('extra_files', []):
        content = _load_template(template_file)
        files[f'{file_key}.py'] = content.format(project_name, api_port)

    # Services
    content = get_template(app_type, 'services')
    files['services.yml'] = content.format(project_name)

    # Settings
    content = get_template(app_type, 'settings')
    if app_type == API_APP:
        files['settings.yml'] = content.format(api_port)
    else:
        files['settings.yml'] = content

    # Shared
    files['__init__.py'] = ''
    files['requirements.txt'] = f'ank>={version}\n'
    content = _load_template(SHARED_TEMPLATES['docker'])
    files['Dockerfile'] = content.format(project_name)
    content = _load_template(SHARED_TEMPLATES['unittest'])
    files['test_service.py'] = content.format(project_name)
    content = _load_template(SHARED_TEMPLATES['readme'])
    files['README.md'] = content.format(project_name)

    return files
