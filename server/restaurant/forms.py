from django.core.files.base import ContentFile
from django import forms
import urllib

from .models import Restaurant, MenuItem, MenuSection
from server import schema

NOT_OWNER = 'NOT_OWNER'

@schema.register
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
        instance = super().save(commit)
        if self._photo_url:
            instance.photo.save(self._photo_url['name'], self._photo_url['file'])
            instance.save()
        instance.owners.add(self.request.user)
        return instance

    class Meta:
        model = Restaurant
        fields = ('name', 'description', 'photo_url')
        def user_can_access(instance, user):
            if instance:
                return user in instance.owners.all()
            return user.role == 'owner'


@schema.register
class OwnerMenuItemForm(forms.ModelForm):
    menusection = forms.IntegerField(widget=forms.HiddenInput)
    def clean_menusection(self):
        if self.instance.id:
            menusection = self.instance.menusection
        else:
            menusection = MenuSection.objects.filter(
                id=self.cleaned_data.get('menusection')
            ).first()
        if not (menusection and self.request.user in menusection.restaurant.owners.all()):
            raise ValidationError(f"You do not have permission to do this.")
        return menusection
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'menusection', 'price']
        def user_can_access(instance, user):
            if instance:
                return user in instance.menusection.restaurant.owners.all()
            return user.role == 'owner'


@schema.register
class OwnerMenuSectionForm(forms.ModelForm):
    restaurant = forms.IntegerField(widget=forms.HiddenInput)
    def clean_restaurant(self):
        if self.instance.id:
            restaurant = self.instance.restaurant
        else:
            restaurant = Restaurant.objects.filter(
                id=self.cleaned_data.get('restaurant')
            ).first()
        if not (restaurant and self.request.user in restaurant.owners.all()):
            raise ValidationError(f"You do not have permission to do this.")
        return restaurant
    class Meta:
        model = MenuSection
        fields = ['name', 'restaurant']
        def user_can_access(instance, user):
            if instance:
                return user in instance.restaurant.owners.all()
            return user.role == 'owner'
