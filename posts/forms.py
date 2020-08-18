from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model=Post
        fields=('text', 'group')
        labels = {
            'text': 'Текст',
            'group': 'Группа'
        }
        help_texts = {
            'text': 'Введите текст вашего поста',
            'group': 'Выберите группу для публикации'
        }


