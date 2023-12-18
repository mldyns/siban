import django_filters
from django import forms
import datetime
from penerima.models import Ranking


def daterange(start, end, step=1):
        current_year = start
        while current_year <= end:
            yield current_year
            current_year += step

class TahunFilter(django_filters.FilterSet):
    t = []
            
    for year in daterange(2019, datetime.date.today().year):
        t.append((year,year))
    
    
    tahun = django_filters.ChoiceFilter(
        choices=t, label="Tahun", empty_label=None, 
        widget=forms.Select(attrs={'class': 'form-control', 'style':'border-color: #063970;border-radius: 10px;color: #063970'})
    )
    class Meta:
        
    
        model=Ranking
        fields={
        }