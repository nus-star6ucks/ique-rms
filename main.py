
import functions_framework
from function.report import Report, filter_reports

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

    reports = filter_reports(storeId, reportId, merchantId)

    return reports


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


