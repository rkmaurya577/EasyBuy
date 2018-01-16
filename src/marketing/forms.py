from django import forms


class EmailForm(forms.Form):
	email = forms.EmailField(max_length=200)

	def __unicode__(self):
		return self.email;
