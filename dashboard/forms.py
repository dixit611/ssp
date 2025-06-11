from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class NotesForm(forms.ModelForm):
  class Meta:
    model = Notes
    fields = ['title','description']


class DateInput(forms.DateInput):
  input_type = 'date'

class HomeworkForm(forms.ModelForm):
  class Meta:
    model = Homework
    widgets = {'due':DateInput()}
    fields = ['subject','title','description','due','is_finished']


class DashboardFom(forms.Form):
  text = forms.CharField(max_length=100,label="Enter you Search :")


class TodoForm(forms.ModelForm):
  class Meta:
    model = Todo
    fields = ['title', 'is_finished']

from django import forms

from django import forms

# Overall form to choose the type of conversion
class ConversionForm(forms.Form):
    measurement = forms.ChoiceField(choices=[
        ('length', 'Length'),
        ('mass', 'Mass'),
        ('temperature', 'Temperature'),
        ('time', 'Time'),
        ('area', 'Area'),
        ('volume', 'Volume'),
        ('weight', 'Weight')
    ], label='Choose Conversion Type')

# Form for Length Conversion (already implemented)
class ConversionLengthForm(forms.Form):
    measure1 = forms.ChoiceField(choices=[
        ('meters', 'Meters'),
        ('kilometers', 'Kilometers'),
        ('centimeters', 'Centimeters'),
        ('millimeters', 'Millimeters'),
        ('inches', 'Inches'),
        ('feet', 'Feet'),
        ('yards', 'Yards'),
        ('miles', 'Miles')
    ], label='From')
    measure2 = forms.ChoiceField(choices=[
        ('meters', 'Meters'),
        ('kilometers', 'Kilometers'),
        ('centimeters', 'Centimeters'),
        ('millimeters', 'Millimeters'),
        ('inches', 'Inches'),
        ('feet', 'Feet'),
        ('yards', 'Yards'),
        ('miles', 'Miles')
    ], label='To')
    input = forms.FloatField(label='Input Value')

# Form for Mass Conversion (already implemented)
class ConversionMassForm(forms.Form):
    measure1 = forms.ChoiceField(choices=[
        ('kilograms', 'Kilograms'),
        ('grams', 'Grams'),
        ('pounds', 'Pounds'),
        ('ounces', 'Ounces')
    ], label='From')
    measure2 = forms.ChoiceField(choices=[
        ('kilograms', 'Kilograms'),
        ('grams', 'Grams'),
        ('pounds', 'Pounds'),
        ('ounces', 'Ounces')
    ], label='To')
    input = forms.FloatField(label='Input Value')

# Form for Temperature Conversion
class ConversionTemperatureForm(forms.Form):
    measure1 = forms.ChoiceField(choices=[
        ('Celsius', 'Celsius'),
        ('Fahrenheit', 'Fahrenheit'),
        ('Kelvin', 'Kelvin')
    ], label='From')
    measure2 = forms.ChoiceField(choices=[
        ('Celsius', 'Celsius'),
        ('Fahrenheit', 'Fahrenheit'),
        ('Kelvin', 'Kelvin')
    ], label='To')
    input = forms.FloatField(label='Input Value')

# Form for Time Conversion
class ConversionTimeForm(forms.Form):
    measure1 = forms.ChoiceField(choices=[
        ('seconds', 'Seconds'),
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days')
    ], label='From')
    measure2 = forms.ChoiceField(choices=[
        ('seconds', 'Seconds'),
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days')
    ], label='To')
    input = forms.FloatField(label='Input Value')

# Form for Area Conversion
class ConversionAreaForm(forms.Form):
    measure1 = forms.ChoiceField(choices=[
        ('square_meters', 'Square Meters'),
        ('square_kilometers', 'Square Kilometers'),
        ('hectares', 'Hectares'),
        ('acres', 'Acres')
    ], label='From')
    measure2 = forms.ChoiceField(choices=[
        ('square_meters', 'Square Meters'),
        ('square_kilometers', 'Square Kilometers'),
        ('hectares', 'Hectares'),
        ('acres', 'Acres')
    ], label='To')
    input = forms.FloatField(label='Input Value')

# Form for Volume Conversion
class ConversionVolumeForm(forms.Form):
    measure1 = forms.ChoiceField(choices=[
        ('liters', 'Liters'),
        ('milliliters', 'Milliliters'),
        ('cubic_meters', 'Cubic Meters'),
        ('gallons', 'Gallons')
    ], label='From')
    measure2 = forms.ChoiceField(choices=[
        ('liters', 'Liters'),
        ('milliliters', 'Milliliters'),
        ('cubic_meters', 'Cubic Meters'),
        ('gallons', 'Gallons')
    ], label='To')
    input = forms.FloatField(label='Input Value')

# Form for Weight Conversion (same as Mass)
class ConversionWeightForm(forms.Form):
    measure1 = forms.ChoiceField(choices=[
        ('kilograms', 'Kilograms'),
        ('grams', 'Grams'),
        ('pounds', 'Pounds'),
        ('ounces', 'Ounces')
    ], label='From')
    measure2 = forms.ChoiceField(choices=[
        ('kilograms', 'Kilograms'),
        ('grams', 'Grams'),
        ('pounds', 'Pounds'),
        ('ounces', 'Ounces')
    ], label='To')
    input = forms.FloatField(label='Input Value')





class UserRegistrationForm(UserCreationForm):
   class Meta:
      model = User
      fields = ['username', 'password1', 'password2']


class CodeForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea(attrs={'id': 'code-editor', 'class': 'form-control', 'rows': 10}), required=True)


from django import forms

class CodeForm(forms.Form):
    email = forms.EmailField()
    code = forms.CharField(widget=forms.Textarea)
    language = forms.ChoiceField(choices=[('c', 'C'), ('cpp', 'C++'), ('python', 'Python'), ('js', 'JavaScript')])

