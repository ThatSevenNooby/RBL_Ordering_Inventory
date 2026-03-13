from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

# The @staff_member_required decorator ensures ONLY users with is_staff=True can enter.
@staff_member_required
def dashboard_home(request):
    return render(request, 'store_dashboard/dashboard_home.html')