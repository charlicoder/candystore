from django.urls import path

from .views import *

app_name = 'bond'

urlpatterns = [
    path('', BondListView.as_view(), name='bond_list'),
    path('pendings-approval/', BondListPendingApprovalView.as_view(), name='bond_list_pendings_approval'),
    path('my-bonds-for-sale/', BondListApprovedForSellView.as_view(), name='bond_list_for_sale'),
    path('my-bonds-soled/', BondListSoldView.as_view(), name='bond_list_sold'),
    path('<int:pk>/details/', BondDetailView.as_view(), name='bond_detail'),
    path('create/', BondCreateView.as_view(), name='bond_create'),
    path('<int:pk>/request-for-sell-approvale/', BondRequestForSellView.as_view(), name='bond_sell_request'),
    path('<int:pk>/approve-for-sell/', BondApproveForSellView.as_view(), name='bond_sell_approve'),
    path('<int:pk>/request-for-sell/', BondUpdateSoldView.as_view(), name='bond_sell'),

]