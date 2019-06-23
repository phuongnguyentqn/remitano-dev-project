from mock import patch
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from main import utils
from main.models import YoutubeVideo


class LoginRegisterViewTest(TestCase):
    def setUp(self):
        self.url = reverse('main:login_register')

    def _do_post(self, data):
        return self.client.post(self.url, data)

    def test_register_success_if_email_not_exist(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        res = self._do_post(data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json(), {'redirect_url': '/'})

    def test_login_success_if_email_and_pwd_correct(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        self.user = User.objects.create_user(**data, username=data['email'])
        res = self._do_post(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {'redirect_url': '/'})

    def test_login_error_if_incorrect_pwd(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        self.user = User.objects.create_user(**data, username=data['email'])
        data['password'] = 'wrong_password'
        res = self._do_post(data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            res.json(), {'message': 'Email or password is incorrect.'})

class DoShareViewTest(TestCase):
    def setUp(self):
        user_data = {
            'username': 'username',
            'password': 'password'
        }
        self.user = User.objects.create_user(**user_data)
        self.url = reverse('main:do_share')
        self.client.login(**user_data)

    @patch('main.views.get_youtube_metadata')
    def test_share_success(self, mock_get):
        mock_data = {'vid': 't-x90HPhQUk', 'title': 'Title'}
        mock_get.return_value = True, mock_data
        video_url = 'https://youtu.be/t-x90HPhQUk'
        res = self.client.post(self.url, {'url': video_url})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {'redirect_url': '/'})
        self.assertTrue(mock_get.called)
        mock_get.assert_called_once_with(video_url)

    def test_share_error_if_invalid_url(self):
        video_url = 'https://youtube.com/asd'
        res = self.client.post(self.url, {'url': video_url})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), {'message': 'Invalid youtube url.'})

    @patch('main.views.get_youtube_metadata')
    def test_share_error_if_video_id_not_exist(self, mock_get):
        mock_data = {'message': 'Http 404'}
        mock_get.return_value = False, mock_data
        video_url = 'https://youtu.be/t-x90HPhQUk'
        res = self.client.post(self.url, {'url': video_url})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), mock_data)
        self.assertTrue(mock_get.called)
        mock_get.assert_called_once_with(video_url)

    @patch('main.views.get_youtube_metadata')
    def test_share_error_if_video_already_shared(self, mock_get):
        existing_vid = 't-x90HPhQUk'
        mock_data = {'vid': existing_vid, 'title': 'Title'}
        existing_video = YoutubeVideo.objects.create(
            shared_by_id=self.user.id, **mock_data)
        mock_get.return_value = True, mock_data
        video_url = 'https://youtu.be/t-x90HPhQUk'
        res = self.client.post(self.url, {'url': video_url})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), {'message': 'The video has already shared.'})
        self.assertTrue(mock_get.called)
        mock_get.assert_called_once_with(video_url)


class UtilsTest(TestCase):
    def test_get_youtube_id(self):
        video_urls = {
            'https://youtu.be/t-x90HPhQUk': 't-x90HPhQUk',
            'https://www.youtube.com/watch?v=t-x90HPhQUk': 't-x90HPhQUk',
        }
        for url, vid in video_urls.items():
            self.assertEqual(vid, utils.get_youtube_id(url))

    @patch('main.utils._get_as_json')
    def test_get_youtube_metadata(self, mock_get):
        mock_data = {
            'title': 'mock_title', 'author_name': 'author', 'author_url': 'url'
        }
        mock_get.return_value = mock_data
        video_url = 'https://youtu.be/t-x90HPhQUk'
        is_valid, data = utils.get_youtube_metadata(video_url)
        self.assertTrue(is_valid)
        mock_data.update({'vid': utils.get_youtube_id(video_url)})
        self.assertEqual(data, mock_data)
