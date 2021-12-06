import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from djoser.serializers import UserCreateSerializer

from .models import Company, Employee

User = get_user_model()


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'position',
            'personal_phone',
            'office_phone',
            'fax',
            'company'
        )
        extra_kwargs = {
            'company': {'required': True},
            'office_phone': {'required': False},
            'fax': {'required': False},
            'middle_name': {'required': False},
            'personal_phone': {
                'required': False,
                'validators': [UniqueValidator(
                    queryset=Employee.objects.all(),
                    message='Personal phone must be unique'
                )]
            }
        }

    def validate(self, data):
        phone_list = [
            data.get('personal_phone'),
            data.get('office_phone'),
            data.get('fax')
        ]
        if not any(phone_list):
            raise serializers.ValidationError(
                'Must be provided at least one phone number'
            )
        for number in phone_list:
            if number and not re.match(Employee.PHONE_REGEX, str(number)):
                raise serializers.ValidationError(
                    f'{number} is wrong number. '
                    'Enter correct number start with +'
                )
        return data


class CompanySerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'address',
            'description',
            'owner',
            'employees'
        )
        extra_kwargs = {
            'name': {'validators': [UniqueValidator(
                queryset=Company.objects.all(),
                message='Name of company must be unique'
            )]}
        }


class ShortCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ('name', 'id')


class UserSerializer(UserCreateSerializer):
    own_companies = serializers.SerializerMethodField(read_only=True)
    rights_to_edit_companies = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'username',
            'rights_to_edit_companies',
            'own_companies'
        )

        extra_kwargs = {'username': {'required': False}}

    def get_own_companies(self, obj):
        own_companies = Company.objects.filter(owner=obj)
        serializer = ShortCompanySerializer(own_companies, many=True)
        return serializer.data


class UserSetRightsSeriazlizer(serializers.Serializer):

    email = serializers.EmailField()
