from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from main.forms import LoginRegisterForm, ShareVideoForm
from main.models import YoutubeVideo
from main.utils import get_youtube_metadata


@require_http_methods(['GET'])
def index(request):
    ctx = {'user': request.user}
    return render(request, 'index.html', ctx)

@require_http_methods(['POST'])
def login_register(request):
    form = LoginRegisterForm(request.POST)
    if not form.is_valid():
        err_data = {'message': 'Invalid data.'}
        return JsonResponse(err_data, status=400)
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    # If user login successfully, login the request
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'redirect_url': '/'})
    # If, email exists, return incorrect credentials
    if User.objects.filter(email=email).exists():
        err_data = {'message': 'Email or password is incorrect.'}
        return JsonResponse(err_data, status=400)
    user = User.objects.create_user(email, email, password)
    login(request, user)
    return JsonResponse({'redirect_url': '/'})

@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'redirect_url': '/'})

@require_http_methods(['GET'])
@login_required
def share(request):
    ctx = {'user': request.user}
    return render(request, 'share.html', ctx)

@require_http_methods(['POST'])
@login_required
def do_share(request):
    # Get the url & validate using form
    form = ShareVideoForm(request.POST)
    if not form.is_valid():
        err_data = {'message': 'Invalid data.'}
        return JsonResponse(err_data, status=400)
    video_url = form.cleaned_data['url']
    # Verify using youtube api
    is_valid, data = get_youtube_metadata(video_url)
    if not is_valid:
        return JsonResponse(data, status=400)
    # Create new object if url is valid
    data['shared_by_id'] = request.user.id
    video, created = YoutubeVideo.objects.get_or_create(**data)
    # Return error message if not valid
    if not created:
        err_data = {'message': 'The video has already shared.'}
        return JsonResponse(err_data, status=400)
    # Redirect to home if success
    return JsonResponse({'redirect_url': '/'})
