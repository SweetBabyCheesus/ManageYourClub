import json

from django.db import models
from django.utils.translation import ugettext_lazy as _

from . dynamic_fields import get_fields_types
from . forms import BaseDynamicForm
from . utils import get_as_dict


class DynamicFieldMap(models.Model):
    """
    """
    name = models.CharField(max_length=150,verbose_name=_('Feldbezeichnung'))
    field_type = models.CharField(max_length=100,
                                  choices = get_fields_types(),verbose_name=_('Typ des Feldes'))
    value = models.TextField(max_length=20000,
                              blank=True,
                              default='',
                              verbose_name=_('Liste von Werten'),
                              help_text=_("Inhalte für Dropdown Listen. "
                                          "Beispiel zur Formatierung: "
                                          "wert 1;wert 2;wert 3"))
    is_required = models.BooleanField(default=True,verbose_name=_('Pflichtfeld (Ja/ Nein)'))
    help_text = models.CharField(max_length=254, blank=True, default='',verbose_name=_('Hilfstext / Erklärung'))
    pre_text = models.TextField(blank=True, default='')
    ordering = models.PositiveIntegerField(verbose_name=_('Sortierung (Stelle des Feldes im Formular)'),
                                              blank=True,
                                              default=0)

    class Meta:
        abstract = True
        ordering = ('ordering',)


class SavedFormContent(models.Model):
    """
    """
    # libreria esterna oppure cambio client per JsonField
    # non serve gestirlo come JsonField perchè non vi facciamo ricerche al suo interno ;)
    json = models.TextField()

    @staticmethod
    def compiled_form(data_source=None,
                      constructor_dict={},
                      files=None,
                      remove_filefields=True,
                      remove_datafields=False,
                      form_source=None,
                      # fields_order=[],
                      extra_datas={},
                      **kwargs):
        """
        Returns form compiled by data (json_dict = json.loads(data_source))
        """
        json_dict = json.loads(data_source)
        data = get_as_dict(json_dict, allegati=False)
        if extra_datas:
            for k,v in extra_datas.items():
                data[k]=v
        if not form_source:
            form_source = BaseDynamicForm
        form = form_source.get_form(constructor_dict=constructor_dict,
                                    data=data,
                                    files=files,
                                    remove_filefields=remove_filefields,
                                    remove_datafields=remove_datafields,
                                    **kwargs)
        # Già invocato nel "form_source", ma è bene tenerlo come riferimento
        # if fields_order:
            # form.order_fields(fields_order)
        return form

    @staticmethod
    def compiled_form_readonly(form, attr='disabled', fields_to_remove=[]):
        """
        Returns a more clean version of the compiled_form.
        - Not compiled fields aren't shown (remove_not_compiled_fields());
        - Title attribute by default isn't shown;
        - Form fields are readonly.
        Note: SelectBox aren't affected by readonly attribute!

        This method is useful to produce not editable compiled form.
        """
        form.remove_not_compiled_fields()
        for field_to_remove in fields_to_remove:
            del form.fields[field_to_remove]
        for generic_field in form:
            field = form.fields[generic_field.name]
            widget = field.widget
            widget.attrs[attr] = True
            # If field is a Formset, the widget will make it readonly
            if field.is_formset:
                widget.make_readonly(attr)
                continue
            # Es: TextArea non ha attributo 'input_type'
            # Senza questo controllo il codice genera un'eccezione
            if not hasattr(widget, 'input_type'):
                # widget.attrs[attr] = True
                continue
            tipo = widget.input_type
            if tipo in ['select', 'checkbox', 'radiobox']:
                widget.attrs['disabled'] = True
            # else:
                # widget.attrs[attr] = True
        return form

    class Meta:
        abstract = True
