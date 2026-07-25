from import_export import resources, fields
from .models import Doctors

class DoctorResource(resources.ModelResource):
    full_name = fields.Field()

    class Meta:
        model = Doctors
        fields = (
            'full_name',
            'user__username',
            'user__first_name',
            'user__last_name',
            'user__email',
            'user__gender',
            'user__birthday',
            'user__id_address__city',
            'user__id_address__address_line',
            'user__profile_avatar',
            'specialty__name',
            'bio',
        )
        export_order = (
            'user__username',
            'full_name',
            'user__email',
            'user__gender',
            'user__birthday',
            'user__id_address__city',
            'user__id_address__address_line',
            'specialty__name',
            'bio',
            'user__profile_avatar',
        )

    def dehydrate_full_name(self, doctor):
        return f"{doctor.user.first_name} {doctor.user.last_name}"
