from django import forms


class FilterForm(forms.Form):
    form_id = None
    form_title = None
    filters = {}

    def get_params(self):
        return {
            field: value
            for field, value in self.cleaned_data.items()
            if value
        }

    def get_filters(self):
        return {
            expr: self.cleaned_data[field]
            for field, expr in self.filters.items()
            if self.cleaned_data.get(field)
        }

    def get_ordering(self):
        return []
