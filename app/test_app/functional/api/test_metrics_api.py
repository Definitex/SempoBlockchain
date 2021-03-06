import pytest
from server.models.transfer_usage import TransferUsage
from server.models.custom_attribute import CustomAttribute, MetricsVisibility
from server.utils.transfer_filter import Filters
from server.utils.credit_transfer import make_payment_transfer
from server.utils.user import create_transfer_account_user, set_custom_attributes
from server import db
import json
import os
from datetime import datetime, timedelta
from dateutil.parser import isoparse

@pytest.fixture(scope='module')
def generate_timeseries_metrics(create_organisation):
    attribute_dict = {'custom_attributes': {}}
    attribute_dict['custom_attributes']['colour'] = 'red'

    # Generates metrics over timeline
    # User1 and User2 made today
    user1 = create_transfer_account_user(first_name='Ricky',
                                    phone="+19025551234",
                                    organisation=create_organisation,
                                    roles=[('BENEFICIARY', 'beneficiary')])
    user1.default_transfer_account.is_approved = True
    user1.default_transfer_account._make_initial_disbursement(100, True)
    user1._location = 'Sunnyvale'
    attribute_dict['custom_attributes']['colour'] = 'red'
    set_custom_attributes(attribute_dict, user1)

    user2 = create_transfer_account_user(first_name='Bubbles',
                                    phone="+19025551235",
                                    organisation=create_organisation)
    user2.default_transfer_account.is_approved = True
    user2.default_transfer_account._make_initial_disbursement(200, True)
    user2._location = 'Sunnyvale'
    attribute_dict['custom_attributes']['colour'] = 'red'

    set_custom_attributes(attribute_dict, user2)

    # user3 made yesterday
    user3 = create_transfer_account_user(first_name='Julian',
                                    phone="+19025531230",
                                    organisation=create_organisation)
    user3.default_transfer_account.is_approved = True
    disburse = user3.default_transfer_account._make_initial_disbursement(210, True)
    user3.created = user3.created - timedelta(days=1)
    disburse.created = user3.created - timedelta(days=1)
    user3._location = 'Dartmouth'
    attribute_dict['custom_attributes']['colour'] = 'blue'
    set_custom_attributes(attribute_dict, user3)

    # user4 made 4 days ago
    user4 = create_transfer_account_user(first_name='Randy',
                                    phone="+19025511230",
                                    organisation=create_organisation)
    user4.default_transfer_account.is_approved = True
    disburse = user4.default_transfer_account._make_initial_disbursement(201, True)
    user4.created = user4.created - timedelta(days=4)
    disburse.created = user4.created - timedelta(days=4)
    user4._location = 'Lower Sackville'
    attribute_dict['custom_attributes']['colour'] = 'blue'
    set_custom_attributes(attribute_dict, user4)

    # user5/user6 made 10 days ago
    user5 = create_transfer_account_user(first_name='Cory',
                                    phone="+19011531230",
                                    organisation=create_organisation)
    user5.default_transfer_account.is_approved = True
    disburse = user5.default_transfer_account._make_initial_disbursement(202, True)
    user5.created = user5.created - timedelta(days=10)
    disburse.created = user5.created - timedelta(days=10)
    user5._location = 'Truro'
    attribute_dict['custom_attributes']['colour'] = 'green'
    set_custom_attributes(attribute_dict, user5)

    user6 = create_transfer_account_user(first_name='Trevor',
                                    phone="+19025111230",
                                    organisation=create_organisation)
    user6.default_transfer_account.is_approved = True
    disburse = user6.default_transfer_account._make_initial_disbursement(204, True)
    user6.created = user6.created - timedelta(days=10)
    disburse.created = user6.created - timedelta(days=10)
    attribute_dict['custom_attributes']['colour'] = 'red'
    set_custom_attributes(attribute_dict, user6)
    db.session.commit()
    tu1 = TransferUsage.find_or_create("Pepperoni")
    tu2 = TransferUsage.find_or_create("Jalepeno Chips")
    tu3 = TransferUsage.find_or_create("Shopping Carts")
    tu1.created = tu1.created - timedelta(days=15)
    tu2.created = tu1.created - timedelta(days=15)
    tu3.created = tu1.created - timedelta(days=15)

    p1 = make_payment_transfer(100,
        create_organisation.token,
        send_user=user1,
        send_transfer_account=user1.default_transfer_account,
        receive_user=user2,
        receive_transfer_account=user2.default_transfer_account,
        transfer_use=str(int(tu1.id))
    )

    p2 = make_payment_transfer(25,
        create_organisation.token,
        send_user=user3,
        send_transfer_account=user3.default_transfer_account,
        receive_user=user4,
        receive_transfer_account=user4.default_transfer_account,
        transfer_use=str(int(tu1.id))
    )
    p2.created = p2.created - timedelta(days=1)

    p3 = make_payment_transfer(5,
        create_organisation.token,
        send_user=user4,
        send_transfer_account=user4.default_transfer_account,
        receive_user=user2,
        receive_transfer_account=user2.default_transfer_account,
        transfer_use=str(int(tu2.id))
    )
    p3.created = p3.created - timedelta(days=1)

    p4 = make_payment_transfer(20,
        create_organisation.token,
        send_user=user5,
        send_transfer_account=user5.default_transfer_account,
        receive_user=user6,
        receive_transfer_account=user6.default_transfer_account,
        transfer_use=str(int(tu3.id))
    )
    p4.created = p4.created - timedelta(days=4)

    p4 = make_payment_transfer(20,
        create_organisation.token,
        send_user=user6,
        send_transfer_account=user6.default_transfer_account,
        receive_user=user5,
        receive_transfer_account=user5.default_transfer_account,
        transfer_use=str(int(tu2.id))
    )
    p4.created = p4.created - timedelta(days=6)
    db.session.commit()

base_participant = {
    'data': 
        {'transfer_stats':
            {'active_filters': [],
            'active_group_by': 'recipient,account_type', 
            'active_users': {'aggregate': {'percent_change': None, 'total': 0},
            'timeseries': {}, 
            'type': {'display_decimals': 0, 'value_type': 'count'}}, 
            'mandatory_filter': {}, 
            'master_wallet_balance': 0,
            'users_created': {'aggregate': {'percent_change': 0.0, 'total': 1}, 
            'timeseries': {}, 
            'type': {'display_decimals': 0, 'value_type': 'count'}}}
        }, 
        'message': 'Successfully Loaded.', 
        'status': 'success'
    }


base_all = {
    'data': 
        {'transfer_stats': 
        {'active_filters': [], 
        'active_group_by': 'recipient,account_type', 
        'active_users': {'aggregate': {'percent_change': None, 'total': 0}, 
        'timeseries': {}, 
        'type': {'display_decimals': 0, 'value_type': 'count'}}, 
        'all_payments_volume': 
            {'aggregate': {'percent_change': None, 'total': 0}, 'timeseries': {}, 'type': {'currency_name': 'AUD Reserve Token', 'currency_symbol': 'AUD', 'display_decimals': 2, 'value_type': 'currency'}}, 
        'daily_transaction_count': 
            {'aggregate': {'percent_change': None, 'total': 0}, 'timeseries': {}, 'type': {'display_decimals': 0, 'value_type': 'count'}}, 
        'mandatory_filter': {}, 
        'master_wallet_balance': 0, 
        'total_distributed': 0.0, 
        'total_reclaimed': 0.0,
        'total_withdrawn': 0.0,
        'trades_per_user': 
            {'aggregate': {'percent_change': None, 'total': 0.0}, 'timeseries': {}, 'type': {'display_decimals': 2, 'value_type': 'count_average'}}, 
        'transfer_amount_per_user': 
            {'aggregate': {'percent_change': None, 'total': 0.0}, 'timeseries': {}, 'type': {'currency_name': 'AUD Reserve Token', 'currency_symbol': 'AUD', 'display_decimals': 2, 'value_type': 'currency'}}, 
        'users_created': 
            {'aggregate': {'percent_change': 0.0, 'total': 1}, 'timeseries': {}, 'type': {'display_decimals': 0, 'value_type': 'count'}}, 
        'users_who_made_purchase': 
            {'aggregate': {'percent_change': None, 'total': 0}, 'timeseries': {}, 'type': {'display_decimals': 0, 'value_type': 'count'}}}}, 
        'message': 'Successfully Loaded.', 
        'status': 'success'
    }

base_all_zero_decimals = {'data': 
    {'transfer_stats': 
    {'active_filters': [], 
    'active_group_by': 'recipient,account_type', 
    'active_users': {'aggregate': {'percent_change': None, 'total': 0}, 
    'timeseries': {}, 
    'type': {'display_decimals': 0, 'value_type': 'count'}}, 
    'all_payments_volume': {'aggregate': {'percent_change': None, 'total': 0}, 
    'timeseries': {}, 
    'type': {'currency_name': 'AUD Reserve Token', 'currency_symbol': 'AUD', 'display_decimals': 0, 'value_type': 'currency'}}, 
    'daily_transaction_count': {'aggregate': {'percent_change': None, 'total': 0}, 
    'timeseries': {}, 'type': {'display_decimals': 0, 'value_type': 'count'}}, 
    'mandatory_filter': {}, 'master_wallet_balance': 0, 'total_distributed': 0.0, 
    'total_reclaimed': 0.0, 
    'total_withdrawn': 0.0, 
    'trades_per_user': {'aggregate': {'percent_change': None, 'total': 0.0}, 
    'timeseries': {}, 
    'type': {'display_decimals': 2, 'value_type': 'count_average'}}, 
    'transfer_amount_per_user': {'aggregate': {'percent_change': None, 'total': 0.0}, 
    'timeseries': {}, 
    'type': {'currency_name': 'AUD Reserve Token', 
    'currency_symbol': 'AUD', 
    'display_decimals': 0, 'value_type': 'currency'}}, 
    'users_created': {'aggregate': {'percent_change': 0.0, 'total': 1}, 
    'timeseries': {}, 
    'type': {'display_decimals': 0, 'value_type': 'count'}}, 
    'users_who_made_purchase': {'aggregate': {'percent_change': None, 'total': 0}, 
    'timeseries': {}, 
    'type': {'display_decimals': 0, 'value_type': 'count'}}}}, 
    'message': 'Successfully Loaded.', 
    'status': 'success'}

base_transfer = {'data': 
    {'transfer_stats': 
    {'active_filters': [], 
    'active_group_by': 'recipient,account_type', 
    'all_payments_volume': 
        {'aggregate': {'percent_change': None, 'total': 0}, 'timeseries': {}, 'type': {'currency_name': 'AUD Reserve Token', 'currency_symbol': 'AUD', 'display_decimals': 2, 'value_type': 'currency'}}, 
    'daily_transaction_count': 
        {'aggregate': {'percent_change': None, 'total': 0}, 'timeseries': {}, 'type': {'display_decimals': 0, 'value_type': 'count'}}, 
    'mandatory_filter': {}, 
    'master_wallet_balance': 0, 
    'total_distributed': 0.0, 
    'total_reclaimed': 0.0,
    'total_withdrawn': 0.0,
    'trades_per_user': 
        {'aggregate': {'percent_change': None, 'total': 0.0}, 'timeseries': {}, 'type': {'display_decimals': 2, 'value_type': 'count_average'}}, 
    'transfer_amount_per_user': 
        {'aggregate': {'percent_change': None, 'total': 0.0}, 'timeseries': {}, 'type': {'currency_name': 'AUD Reserve Token', 'currency_symbol': 'AUD', 'display_decimals': 2, 'value_type': 'currency'}}, 
    'users_who_made_purchase': 
        {'aggregate': {'percent_change': None, 'total': 0}, 'timeseries': {}, 'type': {'display_decimals': 0, 'value_type': 'count'}}}}, 
    'message': 'Successfully Loaded.', 
    'status': 'success'}

@pytest.mark.parametrize("metric_type, status_code, display_decimals", [
    ("user", 200, 2),
    ("all", 200, 2),
    ("all", 200, 0),
    ("credit_transfer", 200, 2),
    ("notarealmetrictype", 500, 2),
])
def test_get_zero_metrics(test_client, complete_admin_auth_token, external_reserve_token, create_organisation,
                             metric_type, status_code, display_decimals):
    create_organisation.token.display_decimals = display_decimals
    def get_metrics(metric_type):
        return test_client.get(
            f'/api/v1/metrics/?metric_type={metric_type}&disable_cache=True&org={create_organisation.id}&group_by=recipient,account_type',
            headers=dict(
                Authorization=complete_admin_auth_token,
                Accept='application/json'
            ),
        )
    response = get_metrics(metric_type)
    assert response.status_code == status_code
    if response.json:
        returned_stats = response.json['data']['transfer_stats']
    else:
        returned_stats = None

    if status_code != 500:
        returned_stats['master_wallet_balance'] = 0
    if metric_type == 'credit_transfer':
        assert response.json == base_transfer
    elif metric_type == 'all' and display_decimals == 2:
        assert response.json == base_all
    elif metric_type == 'all' and display_decimals == 0:
        assert response.json == base_all_zero_decimals
    elif metric_type == 'user':
        assert response.json == base_participant

@pytest.mark.parametrize("metric_type, params, status_code, requested_metric, group_by, output_file", [
    ("all", None, 200, None, 'sender,account_type', 'all_by_account_type.json'),
    ("all", None, 200, None, 'colour,sender', 'all_by_sender_colour.json'),
    ("all", None, 200, None, 'colour,recipient', 'all_by_recipient_colour.json'),
    ("all", None, 200, None ,'sender,location', 'all_by_sender_location.json'),
    ("all", None, 200, None ,'recipient,location', 'all_by_recipient_location.json'),
    ("all", None, 200, None, 'ungrouped', 'all_ungrouped.json'),
    ("all", "rounded_account_balance,sender(GT)(2)", 200, None, 'sender,account_type', 'all_by_account_type_filtered_by_sender.json'),
    ("all", "rounded_account_balance,recipient(GT)(2)", 200, None, 'sender,account_type', 'all_by_account_type_filtered_by_recipient.json'),
    ("credit_transfer", None, 200, None, 'transfer_usage', 'credit_transfer_by_transfer_usage.json'),
    ("user", None, 200, None, 'sender,account_type', 'user_by_account_type.json'),
    ("credit_transfer", None, 200, None, 'transfer_type', 'credit_transfer_by_transfer_type.json'),
    ("all", None, 200, 'active_users', 'sender,account_type', 'requested_metric_active_users.json'),
    ("all", None, 500, None, 'transfer_usage', ''), # 500 because can't group all by transfer_usage 
    ("user", None, 500, None, 'transfer_usage', ''), # 500 because can't group user by transfer_usage
    ("user", 'transfer_amount(LT)(50)', 500, None, 'sender,account_type', ''), # 500 because can't filter user by transfer_amount
    ("all", 'transfer_amount(LT)(50)', 500, None, 'sender,account_type', ''), # 500 because can't filter all by transfer_amount
    ("notarealmetrictype", None, 500, None, 'transfer_usage', ''),
])
def test_get_summed_metrics(
        test_client, complete_admin_auth_token, external_reserve_token, create_organisation, generate_timeseries_metrics,
        metric_type, params, status_code, requested_metric, group_by, output_file
):
    def ts_sort(ts):
        return sorted(ts, key=lambda item: isoparse(item['date']))

    def get_metrics(metric_type):
        p = f'&params={params}' if params else ''
        rm = f'&requested_metric={requested_metric}' if requested_metric else ''
        return test_client.get(
            f'/api/v1/metrics/?metric_type={metric_type}{p}&disable_cache=True&org={create_organisation.id}&group_by={group_by}{rm}',
            headers=dict(
                Authorization=complete_admin_auth_token,
                Accept='application/json'
            ),
        )
    response = get_metrics(metric_type)
    assert response.status_code == status_code

    if response.json:
        returned_stats = response.json['data']['transfer_stats']
    else:
        returned_stats = None
    if status_code == 200:
        script_directory = os.path.dirname(os.path.realpath(__file__))
        desired_output_file = os.path.join(script_directory, 'metrics_outputs', output_file)
        desired_output = json.loads(open(desired_output_file, 'r').read())
        for do in desired_output:
            if not isinstance(desired_output[do], dict) or "timeseries" not in desired_output[do]:
                assert returned_stats[do] == desired_output[do]
            else:
                assert returned_stats[do]['type'] == desired_output[do]['type']
                assert returned_stats[do]['aggregate'] == desired_output[do]['aggregate']
                for timeseries_category in returned_stats[do]['timeseries']:
                    sorted_returned_stats = ts_sort(returned_stats[do]['timeseries'][timeseries_category])
                    sorted_desired_stats = ts_sort(desired_output[do]['timeseries'][timeseries_category])
                    for idx in range(len(returned_stats[do]['timeseries'][timeseries_category])):
                        assert sorted_returned_stats[idx]['value'] == sorted_desired_stats[idx]['value']

@pytest.mark.parametrize("metric_type, status_code, hide_sender", [
    ("user", 200, False),
    ("all", 200, False),
    ("credit_transfer", 200, False),
    ("notarealmetrictype", 500, False),
    ("all", 200, True),
])
def test_get_metric_filters(test_client, complete_admin_auth_token, external_reserve_token,
                             metric_type, status_code, generate_timeseries_metrics, hide_sender):
    if hide_sender:
        db.session.query(CustomAttribute).first().group_visibility = MetricsVisibility.RECIPIENT

    db.session.commit()
    # Tests getting list of availible metrics filters from the /api/v1/metrics/filters endpoint
    response = test_client.get(
        f'/api/v1/metrics/filters/?metric_type={metric_type}',
        headers=dict(
            Authorization=complete_admin_auth_token,
            Accept='application/json'
        ),
    )
    assert response.status_code == status_code
    filters = Filters()
    if status_code == 200:
        if metric_type == 'user':
            assert response.json['data']['filters'] == filters.USER_FILTERS
        elif metric_type == 'transfer':
            assert response.json['data']['filters'] == filters.TRANSFER_FILTERS
        assert response.json['data']['groups']['colour,recipient']['name'] == 'Colour'
        assert response.json['data']['groups']['colour,recipient']['sender_or_recipient'] == 'recipient'
        assert response.json['data']['groups']['colour,recipient']['table'] == 'custom_attribute_user_storage'
        if not hide_sender:
            assert response.json['data']['groups']['colour,sender']['name'] == 'Colour'
            assert response.json['data']['groups']['colour,sender']['sender_or_recipient'] == 'sender'
            assert response.json['data']['groups']['colour,sender']['table'] == 'custom_attribute_user_storage'
        else:
            assert 'colour,sender' not in response.json['data']['groups']
