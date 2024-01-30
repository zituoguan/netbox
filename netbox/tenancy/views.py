from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from netbox.views import generic
from utilities.utils import count_related, get_related_models
from utilities.views import register_model_view, ViewTab
from . import filtersets, forms, tables
from .models import *


class ObjectContactsView(generic.ObjectChildrenView):
    child_model = ContactAssignment
    table = tables.ContactAssignmentTable
    filterset = filtersets.ContactAssignmentFilterSet
    template_name = 'tenancy/object_contacts.html'
    tab = ViewTab(
        label=_('Contacts'),
        badge=lambda obj: obj.contacts.count(),
        permission='tenancy.view_contactassignment',
        weight=5000
    )

    def get_children(self, request, parent):
        return ContactAssignment.objects.restrict(request.user, 'view').filter(
            content_type=ContentType.objects.get_for_model(parent),
            object_id=parent.pk
        ).order_by('priority', 'contact', 'role')

    def get_table(self, *args, **kwargs):
        table = super().get_table(*args, **kwargs)

        # Hide object columns
        table.columns.hide('content_type')
        table.columns.hide('object')

        return table

#
# Tenant groups
#


class TenantGroupListView(generic.ObjectListView):
    queryset = TenantGroup.objects.add_related_count(
        TenantGroup.objects.all(),
        Tenant,
        'group',
        'tenant_count',
        cumulative=True
    )
    filterset = filtersets.TenantGroupFilterSet
    filterset_form = forms.TenantGroupFilterForm
    table = tables.TenantGroupTable


@register_model_view(TenantGroup)
class TenantGroupView(generic.ObjectView):
    queryset = TenantGroup.objects.all()

    def get_extra_context(self, request, instance):
        groups = instance.get_descendants(include_self=True)
        related_models = (
            (Tenant.objects.restrict(request.user, 'view').filter(group__in=groups), 'group_id'),
        )

        return {
            'related_models': related_models,
        }


@register_model_view(TenantGroup, 'edit')
class TenantGroupEditView(generic.ObjectEditView):
    queryset = TenantGroup.objects.all()
    form = forms.TenantGroupForm


@register_model_view(TenantGroup, 'delete')
class TenantGroupDeleteView(generic.ObjectDeleteView):
    queryset = TenantGroup.objects.all()


class TenantGroupBulkImportView(generic.BulkImportView):
    queryset = TenantGroup.objects.all()
    model_form = forms.TenantGroupImportForm


class TenantGroupBulkEditView(generic.BulkEditView):
    queryset = TenantGroup.objects.add_related_count(
        TenantGroup.objects.all(),
        Tenant,
        'group',
        'tenant_count',
        cumulative=True
    )
    filterset = filtersets.TenantGroupFilterSet
    table = tables.TenantGroupTable
    form = forms.TenantGroupBulkEditForm


class TenantGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = TenantGroup.objects.add_related_count(
        TenantGroup.objects.all(),
        Tenant,
        'group',
        'tenant_count',
        cumulative=True
    )
    filterset = filtersets.TenantGroupFilterSet
    table = tables.TenantGroupTable


#
#  Tenants
#

class TenantListView(generic.ObjectListView):
    queryset = Tenant.objects.all()
    filterset = filtersets.TenantFilterSet
    filterset_form = forms.TenantFilterForm
    table = tables.TenantTable


@register_model_view(Tenant)
class TenantView(generic.ObjectView):
    queryset = Tenant.objects.all()

    def get_extra_context(self, request, instance):
        related_models = [
            (model.objects.restrict(request.user, 'view').filter(tenant=instance), f'{field}_id')
            for model, field in get_related_models(Tenant)
        ]

        return {
            'related_models': related_models,
        }


@register_model_view(Tenant, 'edit')
class TenantEditView(generic.ObjectEditView):
    queryset = Tenant.objects.all()
    form = forms.TenantForm


@register_model_view(Tenant, 'delete')
class TenantDeleteView(generic.ObjectDeleteView):
    queryset = Tenant.objects.all()


class TenantBulkImportView(generic.BulkImportView):
    queryset = Tenant.objects.all()
    model_form = forms.TenantImportForm


class TenantBulkEditView(generic.BulkEditView):
    queryset = Tenant.objects.all()
    filterset = filtersets.TenantFilterSet
    table = tables.TenantTable
    form = forms.TenantBulkEditForm


class TenantBulkDeleteView(generic.BulkDeleteView):
    queryset = Tenant.objects.all()
    filterset = filtersets.TenantFilterSet
    table = tables.TenantTable


@register_model_view(Tenant, 'contacts')
class TenantContactsView(ObjectContactsView):
    queryset = Tenant.objects.all()


#
# Contact groups
#

class ContactGroupListView(generic.ObjectListView):
    queryset = ContactGroup.objects.add_related_count(
        ContactGroup.objects.all(),
        Contact,
        'group',
        'contact_count',
        cumulative=True
    )
    filterset = filtersets.ContactGroupFilterSet
    filterset_form = forms.ContactGroupFilterForm
    table = tables.ContactGroupTable


@register_model_view(ContactGroup)
class ContactGroupView(generic.ObjectView):
    queryset = ContactGroup.objects.all()

    def get_extra_context(self, request, instance):
        groups = instance.get_descendants(include_self=True)
        related_models = (
            (Contact.objects.restrict(request.user, 'view').filter(group__in=groups), 'group_id'),
        )

        return {
            'related_models': related_models,
        }


@register_model_view(ContactGroup, 'edit')
class ContactGroupEditView(generic.ObjectEditView):
    queryset = ContactGroup.objects.all()
    form = forms.ContactGroupForm


@register_model_view(ContactGroup, 'delete')
class ContactGroupDeleteView(generic.ObjectDeleteView):
    queryset = ContactGroup.objects.all()


class ContactGroupBulkImportView(generic.BulkImportView):
    queryset = ContactGroup.objects.all()
    model_form = forms.ContactGroupImportForm


class ContactGroupBulkEditView(generic.BulkEditView):
    queryset = ContactGroup.objects.add_related_count(
        ContactGroup.objects.all(),
        Contact,
        'group',
        'contact_count',
        cumulative=True
    )
    filterset = filtersets.ContactGroupFilterSet
    table = tables.ContactGroupTable
    form = forms.ContactGroupBulkEditForm


class ContactGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = ContactGroup.objects.add_related_count(
        ContactGroup.objects.all(),
        Contact,
        'group',
        'contact_count',
        cumulative=True
    )
    filterset = filtersets.ContactGroupFilterSet
    table = tables.ContactGroupTable


#
# Contact roles
#

class ContactRoleListView(generic.ObjectListView):
    queryset = ContactRole.objects.all()
    filterset = filtersets.ContactRoleFilterSet
    filterset_form = forms.ContactRoleFilterForm
    table = tables.ContactRoleTable


@register_model_view(ContactRole)
class ContactRoleView(generic.ObjectView):
    queryset = ContactRole.objects.all()

    def get_extra_context(self, request, instance):
        related_models = (
            (ContactAssignment.objects.restrict(request.user, 'view').filter(role=instance), 'role_id'),
        )

        return {
            'related_models': related_models,
        }


@register_model_view(ContactRole, 'edit')
class ContactRoleEditView(generic.ObjectEditView):
    queryset = ContactRole.objects.all()
    form = forms.ContactRoleForm


@register_model_view(ContactRole, 'delete')
class ContactRoleDeleteView(generic.ObjectDeleteView):
    queryset = ContactRole.objects.all()


class ContactRoleBulkImportView(generic.BulkImportView):
    queryset = ContactRole.objects.all()
    model_form = forms.ContactRoleImportForm


class ContactRoleBulkEditView(generic.BulkEditView):
    queryset = ContactRole.objects.all()
    filterset = filtersets.ContactRoleFilterSet
    table = tables.ContactRoleTable
    form = forms.ContactRoleBulkEditForm


class ContactRoleBulkDeleteView(generic.BulkDeleteView):
    queryset = ContactRole.objects.all()
    filterset = filtersets.ContactRoleFilterSet
    table = tables.ContactRoleTable


#
# Contacts
#

class ContactListView(generic.ObjectListView):
    queryset = Contact.objects.annotate(
        assignment_count=count_related(ContactAssignment, 'contact')
    )
    filterset = filtersets.ContactFilterSet
    filterset_form = forms.ContactFilterForm
    table = tables.ContactTable


@register_model_view(Contact)
class ContactView(generic.ObjectView):
    queryset = Contact.objects.all()


@register_model_view(Contact, 'edit')
class ContactEditView(generic.ObjectEditView):
    queryset = Contact.objects.all()
    form = forms.ContactForm


@register_model_view(Contact, 'delete')
class ContactDeleteView(generic.ObjectDeleteView):
    queryset = Contact.objects.all()


class ContactBulkImportView(generic.BulkImportView):
    queryset = Contact.objects.all()
    model_form = forms.ContactImportForm


class ContactBulkEditView(generic.BulkEditView):
    queryset = Contact.objects.annotate(
        assignment_count=count_related(ContactAssignment, 'contact')
    )
    filterset = filtersets.ContactFilterSet
    table = tables.ContactTable
    form = forms.ContactBulkEditForm


class ContactBulkDeleteView(generic.BulkDeleteView):
    queryset = Contact.objects.annotate(
        assignment_count=count_related(ContactAssignment, 'contact')
    )
    filterset = filtersets.ContactFilterSet
    table = tables.ContactTable

#
# Contact assignments
#


class ContactAssignmentListView(generic.ObjectListView):
    queryset = ContactAssignment.objects.all()
    filterset = filtersets.ContactAssignmentFilterSet
    filterset_form = forms.ContactAssignmentFilterForm
    table = tables.ContactAssignmentTable
    actions = {
        'import': {'add'},
        'export': {'view'},
        'bulk_edit': {'change'},
        'bulk_delete': {'delete'},
    }


@register_model_view(ContactAssignment, 'edit')
class ContactAssignmentEditView(generic.ObjectEditView):
    queryset = ContactAssignment.objects.all()
    form = forms.ContactAssignmentForm
    template_name = 'tenancy/contactassignment_edit.html'

    def alter_object(self, instance, request, args, kwargs):
        if not instance.pk:
            # Assign the object based on URL kwargs
            content_type = get_object_or_404(ContentType, pk=request.GET.get('content_type'))
            instance.object = get_object_or_404(content_type.model_class(), pk=request.GET.get('object_id'))
        return instance

    def get_extra_addanother_params(self, request):
        return {
            'content_type': request.GET.get('content_type'),
            'object_id': request.GET.get('object_id'),
        }


class ContactAssignmentBulkEditView(generic.BulkEditView):
    queryset = ContactAssignment.objects.all()
    filterset = filtersets.ContactAssignmentFilterSet
    table = tables.ContactAssignmentTable
    form = forms.ContactAssignmentBulkEditForm


class ContactAssignmentBulkImportView(generic.BulkImportView):
    queryset = ContactAssignment.objects.all()
    model_form = forms.ContactAssignmentImportForm


class ContactAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = ContactAssignment.objects.all()
    filterset = filtersets.ContactAssignmentFilterSet
    table = tables.ContactAssignmentTable


@register_model_view(ContactAssignment, 'delete')
class ContactAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = ContactAssignment.objects.all()
