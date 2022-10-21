import os

from function import report
from function.report import Report
from flask import Flask, request

# connection to Google cloud
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './_key.json'

app = Flask(__name__)


@app.route('/')
def test():
    return 'Hello World'


# @functions_framework.http
# def getReports(request):
@app.route('/get', methods=['GET'])
def getReports():
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

    reports = report.GetReport(storeId, reportId, merchantId)

    # for r in reports:
    #     print(f"& report id : {r['report_id']} ; create time : {r['create_time']} ; type : {r['type']}")
    #
    # print('* Get successfully !! ')
    # get reports
    return reports


# @functions_framework.http
# def generateReport(request):
@app.route('/generate', methods=['POST'])
def generateReport():
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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
