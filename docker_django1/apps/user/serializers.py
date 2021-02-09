from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from docker_django1.apps.user.models import User

# class StudentRegistrationSerializer(serializers.ModelSerializer):
#     """
#     Serializer that checks data when creating new student record.
#     phone_number is formatted on deserialization and saved as strings of digits
#     """
#     email = serializers.EmailField(label='Email')
#
#     first_name = serializers.CharField(label='Имя', trim_whitespace=True, max_length=64)
#     last_name = serializers.CharField(label='Фамилия', trim_whitespace=True, max_length=64)
#     middle_name = serializers.CharField(label='Отчество', trim_whitespace=True, max_length=64,
#                                         allow_blank=True, allow_null=False, required=False)
#
#     snils = NumbersOnlyField(label='СНИЛС', max_length=11)
#
#     phone_number = MobilePhoneField(label='Номер мобильного телефона', max_length=16)
#
#     @staticmethod
#     def check_snils(snils) -> bool:
#         snils = str(snils)
#         if len(snils) < 11:
#             return False
#         csum = sum([int(snils[9 - i]) * i for i in range(9, 0, -1)])
#         while csum > 101:
#             csum %= 101
#         if csum in (100, 101):
#             csum = 0
#         return csum == int(snils[-2:])
#
#     def to_internal_value(self, data):
#         return super().to_internal_value({
#             **data,
#             'email': data.get('email', '').strip().lower(),
#             'first_name': name_processing(data.get('first_name')),
#             'last_name': name_processing(data.get('last_name')),
#             'middle_name': name_processing(data.get('middle_name')),
#         })
#
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         if Student.objects.filter(email__iexact=data['email']).exists():
#             raise ValidationError(
#                 code='student_already_registered',
#                 detail='Пользователь c таким Email уже существует'
#             )
#
#         # If snils equal to snils allowed for registration
#         # Do not check for user existence
#         if settings.SNILS_EXCEPTION != data.get('snils', ''):
#             snils = data.get('snils', '')
#             if not self.check_snils(snils):
#                 raise ValidationError(
#                     code='incorrect_snils',
#                     detail=(
#                         'Введен некорректный номер СНИЛС. Пожалуйста, проверьте правильность указанных данных. '
#                         'Если вы уверены в корректности заполненного поля СНИЛС, '
#                         'обратитесь в службу технической поддержки по адресу express@worldskills.ru'
#                     )
#                 )
#             student = Student.objects.filter(snils=snils).first()
#             if not student:
#                 return data
#             if student.applications.exclude(status__in=[StatusApplication.expel.name, StatusApplication.cancel.name]):
#                 raise ValidationError(
#                     code='student_already_registered',
#                     detail=(
#                         'В программе уже существует заявка от пользователя c указанным СНИЛС. '
#                         'Если ранее вы не подавали заявку по данной программе на сайте express.worldskills.ru или '
#                         'trudvsem.ru, обратитесь в службу технической поддержки по адресу express@worldskills.ru'
#                     )
#                 )
#             else:
#                 if not all([
#                     str(getattr(student, field)) == str(data.get(field))
#                     for field in ("first_name", "last_name", "middle_name", "birthday", "sex")
#                 ]):
#                     raise ValidationError(
#                         code='student_already_registered',
#                         detail='Пользователь с таким номером СНИЛС уже зарегистрирован'
#                     )
#
#         return data
#
#     def create(self, validated_data):
#         student: Student = Student.objects.filter(snils=validated_data['snils']).first()
#
#         if settings.SNILS_EXCEPTION == validated_data.get('snils', ''):
#             student: Student = Student.objects.create_user(**{k: v for k, v in validated_data.items()})
#
#         if student:
#             student.category = validated_data['category']
#             student.region = validated_data['region']
#             student.study_permission = None
#         else:
#             student: Student = Student.objects.create_user(**{k: v for k, v in validated_data.items()})
#
#         if student.email.lower() != validated_data['email'].lower():
#             student.email = validated_data['email'].lower()
#             student.email_verified = False
#
#         if not student.email_verified:
#             # send email to confirm user
#             token = ConfirmEmailTokenGenerator().make_token(student.user_ptr)
#             confirm_link = f'{settings.SITE_URL}/api/v1/confirm-email/?email={quote(student.email)}&token={token}'
#             send_confirm_email.delay(student.email, student.email_name, confirm_link)
#
#         student.save()
#
#         return student
#
#     class Meta:
#         model = Student
#         fields = ('id', 'email', 'first_name', 'last_name', 'middle_name',
#                   'phone_number', 'birthday', 'sex', 'snils', 'city', 'category',
#                   'region', 'email_verified',)


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    email = serializers.EmailField(max_length=255, required=True, label='Email')
    first_name = serializers.CharField(max_length=255, required=True, label='Имя')
    last_name = serializers.CharField(max_length=255, required=True, label='Отчество')
    middle_name = serializers.CharField(max_length=255, required=False, label='Фамилия')
    email_verified = serializers.BooleanField()
    password = serializers.CharField(
        min_length=4,
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Пароль',
    )

    class Meta:
        fields = '__all__'
        # fields = ('email', 'first_name')
        model = User

    def create(self, validated_data):
        user = self.Meta.model.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

    def validate(self, attrs):
        """todo добавить валидацию по ФИО (отчество опционально,
        сделать trim whitespaces (можно в самом сериализаторе))"""
        data = super(UserSerializer, self).validate(attrs)
        if User.objects.filter(email__iexact=data['email']).exists():
            raise ValidationError(
                code=f'user_already_registered',
                detail=f'Пользователь c таким email "{data["email"]}" уже существует',
            )
        return data
