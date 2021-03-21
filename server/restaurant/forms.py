from django.core.files.base import ContentFile
from django import forms
import urllib

from .models import Restaurant, MenuItem, MenuSection
from server import schema

NOT_OWNER = 'NOT_OWNER'

@schema.register('restaurant')
class OwnerRestaurantForm(forms.ModelForm):
    _photo_url = None
    photo_url = forms.CharField(required=False)

    # TODO there's redundancy between self.photo_url and UserSettingsForm.avatar
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data.get('photo_url') == self.instance.photo_url:
            self._photo_url = self.data.get('photo_url')

    def clean_photo_url(self, *args, **kwargs):
        if self._photo_url:
            response = urllib.request.urlopen(self._photo_url['dataURL'])
            self._photo_url['file'] = ContentFile(response.read())

    def save(self, commit=True):
        if not self.instance.id:
            self.instance.owner = self.request.user
        instance = super().save(commit)
        if self._photo_url:
            instance.photo.save(self._photo_url['name'], self._photo_url['file'])
            instance.save()
        return instance

    user_can_GET = 'ANY'
    @staticmethod
    def user_can_POST(instance, user):
        if instance:
            return instance.user_can_edit(user)
        return user.role == 'owner'
    class Meta:
        model = Restaurant
        fields = ('name', 'description', 'photo_url')


@schema.register('menuitem')
class OwnerMenuItemForm(forms.ModelForm):
    menusection = forms.IntegerField(widget=forms.HiddenInput)
    def clean_menusection(self):
        if self.instance.id:
            menusection = self.instance.menusection
        else:
            menusection = MenuSection.objects.filter(
                id=self.cleaned_data.get('menusection')
            ).first()
        if not (menusection and menusection.restaurant.user_can_edit(self.request.user)):
            raise ValidationError(f"You do not have permission to do this.")
        return menusection

    @staticmethod
    def user_can_POST(instance, user):
        if instance:
            return instance.menusection.restaurant.user_can_edit(user)
        return user.role == 'owner'
    user_can_GET = user_can_POST
    user_can_DELETE = user_can_POST

    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'menusection', 'price']


@schema.register('menusection')
class OwnerMenuSectionForm(forms.ModelForm):
    restaurant = forms.IntegerField(widget=forms.HiddenInput)
    def clean_restaurant(self):
        if self.instance.id:
            restaurant = self.instance.restaurant
        else:
            restaurant = Restaurant.objects.filter(
                id=self.cleaned_data.get('restaurant')
            ).first()
        if not (restaurant and restaurant.user_can_edit(self.request.user)):
            raise ValidationError(f"You do not have permission to do this.")
        return restaurant

    @staticmethod
    def user_can_POST(instance, user):
        if instance:
            return instance.restaurant.user_can_edit(user)
        return user.role == 'owner'
    user_can_GET = user_can_POST
    user_can_DELETE = user_can_POST

    class Meta:
        model = MenuSection
        fields = ['name', 'restaurant']
