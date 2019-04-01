
from django import forms


class Question(forms.Form):
    text = forms.CharField(label='Question text', max_length=100)

    def clean_text(self):
        return self.cleaned_data.get('text')


class Survey(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(Survey, self).__init__(*args, **kwargs)

        for i, question in extra:
            self.fields['custom_%s' % i] = forms.CharField(label=question)

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (int(name[7:]), value)


class Key(forms.Form):
    key = forms.CharField()



