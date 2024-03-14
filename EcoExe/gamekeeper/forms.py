#Authored by George Piper and James Sadler

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class":"form-control"
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={
                "class":"form-control"
            }
        )
    )

class QuizCreationForm(forms.Form):
    quiz_name = forms.CharField()
    points_per_question = forms.IntegerField()
    extra_field_count = forms.CharField(widget = forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0) #get the extra argument passed in
        super(QuizCreationForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields #initialise the form with extra fields

        #add in the extra fields for added questions and answers
        for i in range(1,int(extra_fields)):
            self.fields['extra_field_{index}'.format(index=i)] = \
                forms.CharField()
            
class QRCreationForm(forms.Form):
    qr_name = forms.CharField()
    location = forms.CharField()
    extra = forms.CharField(required=False)

class TreasureHuntCreationForm(forms.Form):
    treasure_hunt_name = forms.CharField()
    bonus_points = forms.IntegerField()
    extra_field_count = forms.CharField(widget = forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0) #get the extra argument passed in
        super(TreasureHuntCreationForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields #initialise the form with extra fields

        #add in the extra fields for added questions and answers
        for i in range(1,int(extra_fields)+1):
            self.fields['extra_field_{index}'.format(index=i)] = \
                forms.CharField()

class SetDailyForm(forms.Form):
    quiz = forms.CharField()
    date = forms.CharField()