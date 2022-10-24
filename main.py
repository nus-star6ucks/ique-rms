
import json
import functions_framework
from sqlalchemy import inspect
from function.report import Report, filter_reports


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

@functions_framework.http
def get_reports(request):
    """
    return the store's all URL
    :param request: storeID, merchantID, reportID
    :return list<URL>
    """

    storeId = request.args.get('storeId')
    merchantId = request.args.get('merchantId')
    reportId = request.args.get('reportId')
    # print(f'* store id : {storeId}')
    # print(f'* merchant id : {merchantId}')
    # print(f'* report id : {reportId}')

    return json.dumps([object_as_dict(filter_reports(storeId, reportId, merchantId)) for ob in reports],
                      indent=4, sort_keys=True, default=str)


# @app.route('/generate', methods=['POST'])
@functions_framework.http
def generate_report(request):
    """
    [Scheduler]
    generate the specific report for the store
    :param request: storeID, reportType, unit
    """
    # print('$ generate method')

    # storeID = request.args.get('storeId')
    # reportType = request.args.get('reportType')
    # unit = request.args.get('unit', 'week')

    storeID = request.json['storeId']
    reportType = request.json['reportType']
    unit = request.json['unit']
    # print(f'* store id : {storeID}')
    # print(f'* report type : {reportType}')
    # print(f'* unit : {unit}')

    # generate report
    newreport = Report(storeID, reportType, unit)

    return newreport.url


