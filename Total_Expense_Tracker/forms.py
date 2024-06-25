from django import forms # type: ignore

class ShiftForm(forms.Form):
    shift_start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Shift Start"
    )
    shift_end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Shift End"
    )
    IS_CASH_CHOICES  = [
        (True, 'Cash'),
        (False, 'Online'),
    ]
    is_cash = forms.ChoiceField(
        choices=IS_CASH_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Transaction Mode"
    )
    tip = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="Tip Amount", 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    ride = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="Ride Amount", 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class TransactionForm(forms.Form):
    IS_CREDIT_CHOICES  = [
        (True, 'Credit'),
        (False, 'Debit'),
    ]
    is_credit = forms.ChoiceField(
        choices=IS_CREDIT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Transaction Type"
    )
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        label="Amount", 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    IS_CASH_CHOICES  = [
        (True, 'Cash'),
        (False, 'Online'),
    ]
    is_cash = forms.ChoiceField(
        choices=IS_CASH_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Transaction Mode"
    )
    TYPE_CHOICES = [
        ('Walmart', 'Walmart'),
        ('India_Bazaar', 'India Bazaar'),
        ('Ride', 'Ride'),
        ('Rent','Rent'),
        ('Other', 'Other')
    ]
    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_type'})
    )
    other_type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class TransactionResultForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="End Date"
    )

class ShiftResultForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Start Date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="End Date"
    )
    shift_type_choices = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Both','Both')
    ]
    shift_type = forms.ChoiceField(
        choices=shift_type_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Shift Type"
    )
    # noofrows = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'class': 'form-control'}),
    #     label="Number of Rows"
    # )