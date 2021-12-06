from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action


from .mixins import CreateListRetrieveViewSet
from .models import Company, Employee
from .serializers import (EmployeeSerializer, CompanySerializer,
                          UserSerializer, UserSetRightsSeriazlizer)
from .permissions import (SignUpOrIsAuthentificatedOrSelf,
                          IsCompanyOwnerOrReadOnly, HasRigthsToEditOrReadOnly)

User = get_user_model()


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [HasRigthsToEditOrReadOnly, ]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [IsCompanyOwnerOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name',
        'employees__last_name',
        'employees__first_name',
        'employees__middle_name',
        'employees__personal_phone'
    ]

    def get_serializer_class(self):
        if self.action == 'grant_rigths_to_edit':
            return UserSetRightsSeriazlizer
        return CompanySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsCompanyOwnerOrReadOnly]
    )
    def grant_rigths_to_edit(self, request, pk):
        company = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = get_object_or_404(User, email=email)
        if user == request.user:
            return Response(
                data=['Error! You can`t grant yourself'],
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'POST':
            if company not in user.rights_to_edit_companies.all():
                user.rights_to_edit_companies.add(company)
                return Response(
                    data=['The rights have been successfully granted'],
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                    data=['Error! User already has the rigths'],
                    status=status.HTTP_400_BAD_REQUEST
                )
        if request.method == 'DELETE':
            if company in user.rights_to_edit_companies.all():
                user.rights_to_edit_companies.remove(company)
                return Response(
                    data=['The rights have been successfully revoked'],
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                data=['Error! User does not have rights yet'],
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def editable_by_me(self, request):
        user = request.user
        companies = user.rights_to_edit_companies.all()

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(companies, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.get_serializer(companies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [SignUpOrIsAuthentificatedOrSelf, ]

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )
    def editing_my_companies(self, request):
        users_with_rights = User.objects.filter(
            rights_to_edit_companies__owner=request.user).distinct()
        serializer = self.get_serializer(users_with_rights, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
