from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class TestMethods(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="test"
        )

    # Тест на создание профиля пользователя при регистрации
    def testProfile(self):
        response = self.client.get('/test/')
        self.assertEqual(response.status_code, 200)

    # Тест на добавление записи авторизованным пользователем
    def testNewPostAuth(self):
        self.client.force_login(self.user)
        response = self.client.post('/new/', data={'text': 'text'}, follow=True)
        self.assertRedirects(response, '/')
        self.assertEqual(Post.objects.filter(author=self.user).count(), 1)

    # Тест на невозможность создать запись неавторизованным пользователем
    def testNewPostNotAuth(self):
        response = self.client.post('/new/', data={'text': 'text'}, follow=True)
        self.assertRedirects(response, '/auth/login/?next=/new/')

    # Вспомогательная функция для проверки наличия определенного поста на главной странице, странице пользователя и
    # страницы с самим постом
    def help_test(self, text):
        response = self.client.get('/')
        posts_index = list(map(lambda x: x.text, response.context['page']))  # Получаем текст всех постов на главной
        # странице
        response = self.client.get(f'/{self.user.username}/')
        posts_profile = list(map(lambda x: x.text, response.context['page']))  # Получаем текст всех постов на
        # странице пользователя
        response = self.client.get(f'/{self.user.username}/1/')
        self.assertEqual(response.status_code, 200)  # Проверяем, что страница с постом существует
        self.assertEqual(response.context['post'].text, text)  # Проверяем, что текст поста на странице соответствует
        # тексту, который был создан
        self.assertTrue(text in posts_index)  # Проверяем, что текст созданного поста есть среди текстов на главной
        # странице
        self.assertTrue(text in posts_profile)  # Проверяем, что текст созданного поста есть на странице пользователя

    # Тест на создание нового поста на главной странице, странице пользователя и странице этого поста
    def testNewPostExist(self):
        self.client.force_login(self.user)
        text = 'text123'
        self.client.post('/new/', data={'text': text}, follow=True)
        self.help_test(text)

    # Тест на редактирование поста
    def testEditingPost(self):
        self.client.force_login(self.user)
        text = 'text123'
        self.client.post('/new/', data={'text': text}, follow=True)
        new_text = 'text123_edit'
        self.client.post(f'/{self.user.username}/1/edit/', data={'text': new_text}, follow=True)
        self.help_test(new_text)
