
from users.models import Citizen, Workers, DepartmentAdmin

def get_account_type(user):
    if Citizen.objects.filter(user=user).exists():
        return 'Citizen'
    elif Workers.objects.filter(user=user).exists():
        return 'Worker'
    elif DepartmentAdmin.objects.filter(user=user).exists():
        return 'DepartmentAdmin'
    elif user.is_staff:
        return 'SuperAdmin'
    return 'Unknown'