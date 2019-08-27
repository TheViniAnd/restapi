from django.conf.urls import url
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from api_v1 import views
from api_v1.views import *
from api_v1.views import UserViews


urlpatterns = [
    #Готово
    path('user/get', UserViews.as_view()),
    path('owner/object/all', ObjectsPropertyOwnerViews.as_view()),
    path('owner/object/get', OneObjectPropertyOwnerViews.as_view()),
    path('owner/object/areas/now', EmploymentNowViews.as_view()),
    path('owner/object/tenantry', ListTenantresViews.as_view()),

    path('manager/user/all', AllUsersViews.as_view()),
    path('manager/user/delete', DeleteUserViews.as_view()),
    path('auth/user/add', AddUserViews.as_view()),
    
    path('manager/realty/all', AllRealtyViews.as_view()),
    path('manager/realty/add', AddRealtyViews.as_view()),
    path('manager/realty/remove', RemoveRealtyViews.as_view()),
    path('manager/realty/update', UpdateRealtyViews.as_view()),

    path('manager/contract/all', AllContractViews.as_view()),
    path('manager/contract/add', AddContractViews.as_view()),
    path('manager/contract/close', CloseContractViews.as_view()),

    path('manager/realty/gallery/get', GetImgRealtyViews.as_view()),
    path('manager/realty/gallery/add_img', AddImgRealtyViews.as_view()),
    path('manager/realty/gallery/remove_img', RemoveImgRealtyViews.as_view()),

    #Сделано, но не прроверено
    path('owner/object/areas/over_period', EmploymentOverPeriodViews.as_view()),
    path('owner/object/files', ListFilesViews.as_view()),
    path('owner/notification/new', NewNatification.as_view()),

    path('tenant/object/all', ObjectsPropertyTenantViews.as_view()),
    path('tenant/object/get', OneObjectPropertyTenantViews.as_view()),

    path('message/count', CountMessageViews.as_view()),
    path('message/push', PushMessageViews.as_view()),
    path('message/get/new', NewMessageViews.as_view()),
    path('message/range', RangeMessageViews.as_view()),
    path('message/read', ReadMessageViews.as_view()),

    path('change_password', ChangePasswordViews.as_view()),
    path('rental_flow/now', TotalRentalFlowNowViews.as_view()),
    path('owner/object/cost/now', CostNowViews.as_view()),
    path('cost/now', TotalCostNowViews.as_view()),
    path('areas/now', TotalEmploymentNowViews.as_view()),

    #Нужно сделать
    path('owner/object/cost/over_period', CostOverPeriodViews.as_view()),
    path('rental_flow/over_period', TotalRentalFlowOverPeriodViews.as_view()),
    path('areas/over_period', TotalEmploymentOverPeriodViews.as_view()),
    path('cost/over_period',TotalCostOverPeriodViews.as_view()),
]
