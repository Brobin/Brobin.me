from django.db import models
from urllib.parse import urljoin


class BaseMenuItem(models.Model):
    title = models.CharField(max_length=32)
    link = models.CharField(max_length=64)
    base_url = models.CharField(max_length=100, blank=True, null=True)
    new_tab = models.BooleanField(default=False)
    login_required = models.BooleanField(default=False)
    anonymous_only = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=10)

    class Meta:
        abstract = True

    @property
    def url(self):
        if self.base_url:
            return urljoin(self.base_url, self.link)
        return self.link


class MenuItem(BaseMenuItem):

    def __str__(self):
        return self.title

    @property
    def sub_menu_items(self):
        return self.submenuitem_set.all().order_by('order')

    @property
    def num_sub_menu_items(self):
        return len(self.sub_menu_items)

    @property
    def has_sub_items(self):
        return self.num_sub_menu_items > 0


class SubMenuItem(BaseMenuItem):
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} {1}'.format(self.menu.title, self.title)
