from django.forms import ModelForm
from . models import PresentIllnessImage

class PresentIllnessImageForm(ModelForm):
  class Meta:
    model = PresentIllnessImage
    fields = '__all__'