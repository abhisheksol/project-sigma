from core_utils.utils.generics.serializers.mixins import CoreGenericBaseHandler
from user_config.user_auth.models import FoAttendanceModel, FoStatusenum, UserModel
from core_utils.utils.enums import list_enum_values
from django.db import transaction
from datetime import datetime, date, time, timedelta


class FoAttendanceUpdateHandler(CoreGenericBaseHandler):
    attendance_instance: FoAttendanceModel = None

    def validate(self):
        attendance_id = self.request.query_params.get('fo_user')
        if not attendance_id:
            return self.set_error_message("Attendance ID is required", key="id")

        fo_status = self.data.get("fo_status")
        if fo_status is None:
            return self.set_error_message("fo_status is required", key="fo_status")

        if fo_status not in list_enum_values(enum_cls=FoStatusenum):
            return self.set_error_message("Invalid fo_status", key="fo_status")

        # ------------------------------------------------------
        # Step 1: Auto-close all previous open ON_DUTY records
        # ------------------------------------------------------
        open_attendances = self.queryset.filter(
            fo_user__id=attendance_id,
            date__lt=date.today(),
            fo_status=FoStatusenum.ON_DUTY.value
        )

        for attendance in open_attendances:
            attendance.fo_status = FoStatusenum.OFF_DUTY.value
            # Auto-close at 23:59:59 of that day
            attendance.duty_off = datetime.combine(attendance.date, time(23, 59, 59))

            if attendance.duty_on:
                duty_on_dt = (
                    datetime.combine(attendance.date, attendance.duty_on)
                    if isinstance(attendance.duty_on, time)
                    else attendance.duty_on
                )
                delta = attendance.duty_off - duty_on_dt
                attendance.hours_worked = round(delta.total_seconds() / 3600, 2)

            attendance.save()
            self.logger.info(
                f"Auto-closed previous ON_DUTY record for user_id={attendance_id} on {attendance.date}"
            )

        # ------------------------------------------------------
        # Step 2: Get today's attendance record or create it
        # ------------------------------------------------------
        try:
            self.attendance_instance = self.queryset.get(
                fo_user__id=attendance_id, date=date.today()
            )
        except FoAttendanceModel.DoesNotExist:
            try:
                user = UserModel.objects.get(id=attendance_id)
            except UserModel.DoesNotExist:
                return self.set_error_message("User not found", key="fo_user")

            self.attendance_instance = FoAttendanceModel.objects.create(
                fo_user=user,
                date=date.today(),
                fo_status=FoStatusenum.OFF_DUTY.value
            )
            self.logger.info(
                f"New attendance record created for user_id={attendance_id} on {date.today()}"
            )

    # ------------------------------------------------------
    # Step 3: Update the attendance record based on status
    # ------------------------------------------------------
    def create(self):
        with transaction.atomic():
            fo_status = self.data.get("fo_status")
            attendance = self.attendance_instance
            now = datetime.now()

            attendance.fo_status = fo_status

            if not attendance.date:
                attendance.date = date.today()

            # -------------------
            # ON_DUTY case
            # -------------------
            if fo_status == FoStatusenum.ON_DUTY.value:
                if not attendance.duty_on:
                    attendance.duty_on = now

            # -------------------
            # OFF_DUTY case
            # -------------------
            elif fo_status == FoStatusenum.OFF_DUTY.value:
                attendance.duty_off = now
                if attendance.duty_on:
                    duty_on_dt = (
                        datetime.combine(attendance.date, attendance.duty_on)
                        if isinstance(attendance.duty_on, time)
                        else attendance.duty_on
                    )
                    delta = attendance.duty_off - duty_on_dt
                    attendance.hours_worked = round(delta.total_seconds() / 3600, 2)

            attendance.save()
            self.logger.info(
                f"Attendance updated successfully for user_id={attendance.fo_user.id}, "
                f"status={attendance.fo_status}, hours_worked={attendance.hours_worked}"
            )
