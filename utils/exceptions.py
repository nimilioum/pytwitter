from rest_framework.exceptions import APIException


class DomainException(APIException):
    status_code = 400
    default_detail = 'bad request'
    default_code = 'bad request'
