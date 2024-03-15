#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoExe.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

'''
from treasurehunt import treasure
<<<<<<< HEAD
#treasure.Treasure.addActivity("TOM","12,12","Quiz","1",100)
print(".")
treasure.Treasure.getActivities()
'''
=======
a=treasure.Treasure.getTreasure(id=1)
print("AAAA"+a.getImage())
#treasure.Treasure.addStage(1,stage_no=2)
#print("AA")
'''
>>>>>>> aeaa74d99ce36db995297d3c93dc6463a24ec436
