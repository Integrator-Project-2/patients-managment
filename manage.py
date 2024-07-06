#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patients_managment.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Check if 'runserver' command is being executed
    if 'runserver' in sys.argv:
        from django.conf import settings
        # Get the PORT value from settings.py or default to 8000
        port = getattr(settings, 'PORT', 8000)
        # If 'runserver' is in sys.argv and there's at least one argument after it
        if 'runserver' in sys.argv and sys.argv.index('runserver') + 1 < len(sys.argv):
            # Replace the port value in sys.argv
            sys.argv[sys.argv.index('runserver') + 1] = str(port)
        else:
            # Append the port argument to sys.argv
            sys.argv.append(str(port))
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
