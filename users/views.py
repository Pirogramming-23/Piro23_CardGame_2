from django.shortcuts import render

# Create your views here.
def main_view(request):
    if request.user.is_authenticated:
        return render(request, 'users/main_after.html', {
            'user': request.user,
        })
    return render(request, 'users/main_before.html')