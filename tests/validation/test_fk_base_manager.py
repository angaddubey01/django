from django import forms
from django.test import TestCase

from .models import ArchivedArticle, FavoriteArchivedArticle


class FavoriteArchivedArticleForm(forms.ModelForm):
    class Meta:
        model = FavoriteArchivedArticle
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["article"].queryset = ArchivedArticle._base_manager.all()


class ForeignKeyBaseManagerTests(TestCase):
    def test_foreign_key_validation_uses_base_manager(self):
        article = ArchivedArticle.objects.create(title="Test", archived=True)
        form = FavoriteArchivedArticleForm({"article": article.pk})
        self.assertTrue(form.is_valid())
