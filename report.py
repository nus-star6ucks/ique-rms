"""
Includes all functions used to generate Report
"""
from enum import Enum
import datetime
import pandas as pd
import requests
import Postgres
import Mongo
import GCloud
from visual import generateURL

prefix = 'https://mock.apifox.cn/m1/1701091-0-default'


class ReportType(Enum):
    AWT = 1  # average waiting time
    NUM = 2  # waiting customer number & actual diner number


class UnitType(Enum):
    day = 12  # minium interval = 2 hours
    week = 7  # minium interval = day
    month = 5  # minium interval = week
    year = 13  # minium interval = year


twohour = 60 * 60 * 2
oneday = twohour * 12
oneweek = oneday * 7
# onemonth = [oneday * 31,
#             oneday * 28,
#             oneday * 31,
#             oneday * 30,
#             oneday * 31,
#             oneday * 30,
#             oneday * 31,
#             oneday * 31,
#             oneday * 30,
#             oneday * 31,
#             oneday * 30,
#             oneday * 31
#             ]

ticketStatus = ['seated', 'pending', 'skipped']

reportTypeValue = {'AWT': 1,
                   'NUM': 2
                   }

unitValue = {'day': 12,
             'week': 7,
             'month': 5,
             'year': 13
             }

unitValueReverse = dict(zip(unitValue.values(), unitValue.keys()))


def GetReport(stID, reportID, merchantID):
    """
    get reports from DB
    :param stID: report ID
    :param reportID: store ID
    :param merchantID: merchant ID
    :return reports: array[report]
    """
    if reportID is not None:
        reports = Postgres.Report.select().where(Postgres.Report.report_id == reportID).dicts()
    elif stID is not None:
        reports = Postgres.Report.select().where(Postgres.Report.store_id == stID).dicts()
    else:
        reports = Postgres.Report.select().where(Postgres.Report.merchant_id == merchantID).dicts()

    return list(reports)


class Report:

    def __init__(self, stID, rtype, timeunit):
        """
        Report
        :param stID: store ID
        :param timeunit
        :param rtype: type of report
        """
        self.ID = None  # DB created automatically; get while saved it into DB
        self.storeID = stID
        self.reportType = rtype
        self.unit = timeunit
        self.createTime = datetime.datetime.now()  # year-month-day hour-minute-second
        # print(f'* create time : {self.createTime}')
        self.data = None  #
        self.DBdata = None  # data formal for DB
        self.url = None
        self.begin = None
        # default end time is the start of next day of creat day (year-month-day-0-0-0-0)
        self.end = (self.createTime + pd.DateOffset(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        self.store = None
        # count begin time
        self.getBeginTime(unitValue[self.unit])
        # print(f'* begin time : {self.begin}')
        # print(f'* end time : {self.end}')
        # save store DB entity
        store = Postgres.Store.select().where(Postgres.Store.store_id == self.storeID)
        for s in store:
            self.store = s

        # print(f'* store : {self.store.name}')
        # print(f'* merchant id : {self.store.merchant_id}')
        # print('$ start generating .....')

        # generate url of this report
        self.generateReport(self.storeID, reportTypeValue[self.reportType], unitValue[self.unit])
        # reset data's time
        self.resetTimezone(unitValue[self.unit])
        self.url = generateURL(self.reportType, self.data, unitValue[self.unit], self.store, self.createTime)
        # print(f'* Create URL Successful : {self.url}')
        # save report into SQL
        self.saveData()
        # print(f'* report id : {self.ID}')
        # print('* Done !')

    def generateReport(self, storeID, rtype, unit):
        """
        generate report
        :param storeID: store ID
        :param rtype: report type
        :param unit: time unit of report
        """
        if rtype == ReportType.AWT.value:
            self.getAWT(storeID, unit)
        elif rtype == ReportType.NUM.value:
            self.getWCNandADN(storeID, unit)

    def saveData(self):
        """
        save data into DB: NoSQL / SQL
        """
        # save report into SQL
        report = Postgres.Report.create(store_id=self.storeID,
                                        type=self.reportType,
                                        unit=self.unit,
                                        create_time=self.createTime,
                                        url=self.url,
                                        merchant_id=self.store.merchant_id)
        report.save()

        # get report ID
        self.ID = report.report_id

        # save generated data into NoSQL
        reportdata = Mongo.Reportdata(report_id=self.ID,
                                      store_id=self.storeID,
                                      data_type=self.reportType,
                                      unit=self.unit,
                                      start_time=self.begin,
                                      end_time=self.end,
                                      data=self.data)
        reportdata.save()
        # print('* Save DB successfully !')

    def getBeginTime(self, unit):
        """
        count begin time
        :param unit
        """
        # print(f'* unit : {unit}')

        # set integrate value: year-month-day-0-0-0-0
        if unit == UnitType.day.value:
            self.begin = (self.end - pd.DateOffset(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif unit == UnitType.week.value:
            self.begin = (self.end - pd.DateOffset(weeks=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif unit == UnitType.month.value:
            self.begin = (self.end - pd.DateOffset(months=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif unit == UnitType.year.value:
            self.begin = (self.end - pd.DateOffset(years=1)).replace(hour=0, minute=0, second=0, microsecond=0)

    def timeCount(self, op, time, unit, factor):
        """
        define calculate time
        :param op
        :param time
        :param unit
        :param factor: count factor
        :return new-time
        """
        # print(f'& begin time : {time} ; factor : {factor}')
        if op is '-':
            if unit == UnitType.day.value:
                return time - pd.DateOffset(hours=factor * 2)
            elif unit == UnitType.week.value:
                return time - pd.DateOffset(days=factor)
            elif unit == UnitType.month.value:
                return time - pd.DateOffset(weeks=factor)
            elif unit == UnitType.year.value:
                return time - pd.DateOffset(months=factor)
        else:
            if unit == UnitType.day.value:
                return time + pd.DateOffset(hours=factor * 2)
            elif unit == UnitType.week.value:
                return time + pd.DateOffset(days=factor)
            elif unit == UnitType.month.value:
                # print('* count month')
                # print(f'& result time : {time + pd.DateOffset(weeks=factor)}')
                return time + pd.DateOffset(weeks=factor)
            elif unit == UnitType.year.value:
                return time + pd.DateOffset(months=factor)

    def Divided(self, tickets, unit):
        """
        divided tickets into different time zone
        :param unit
        :param tickets
        :return new-tickets[]
        """
        newTickets = [[]] * 12
        # print(f'& test new tickets array : {newTickets}')
        factor = None
        # day: 12 * 2hours
        # week: 7 * 1day
        # month: 5 * 1week
        # year: 12 * 1month

        if unit is UnitType.day.value:
            factor = twohour
        elif unit is UnitType.week.value:
            factor = oneday
        elif unit is UnitType.month.value:
            factor = oneweek

        # count the difference between ticket's start time and begin time
        # and divided by 2 to get interval sequence
        # round down
        for t in tickets:
            # print(f'& ticket start time : {t.start_time}')
            if unit is UnitType.year.value:                    # divided by month
                zone = t.start_time.month       # firstly divided by its month

                if t.start_time.day < self.begin.day:          # if day less than begin date, it should be divided into last zone
                    zone -= 1

                if t.start_time.year > self.begin.year:        # current year: backward
                    zone += 12 - self.begin.month
                else:                                          # last year: forward
                    zone -= self.begin.month
            else:
                zone = int((t.start_time - self.begin).total_seconds() / factor)
            # print(f'& zone : {zone}')
            if len(newTickets[zone]) is 0:
                newTickets[zone] = []
            newTickets[zone].append(t)
        #     print(f'& new tickets : {newTickets}')
        # print('# ticket time zone')
        # print(newTickets)
        return newTickets

    def Filter(self, type, tickets, unit, seatType):
        """
        filter tickets by type according to data
        :param type: filter choice[time,status,seat]
        :param unit
        :param tickets
        :param seatType: array of seat type
        :return data[]
        """
        result = {}

        if type is 'time':  # filter by time

            Tickets = []
            # ticket's start time should greater than or equal to beginTime
            # and its start time should not greater than endTime
            for t in tickets:
                # print(f'# ticket id : {t.ticket_id} ; start time : {t.start_time}')
                if self.begin <= t.start_time < self.end:
                    # print(f'# YES ')
                    Tickets.append(t)
            # print(f'# selected tickets : {Tickets}')
            # divided tickets according to unit
            result['time'] = self.Divided(Tickets, unit)
        elif type is 'status':  # filter by status
            pendingT = []
            seatedT = []
            skippedT = []
            for t in tickets:
                if t.status == 'pending':
                    pendingT.append(t)
                elif t.status == 'seated':
                    seatedT.append(t)
                else:
                    skippedT.append(t)
            result['seated'] = seatedT
            result['pending'] = pendingT
            result['skipped'] = skippedT
        else:
            # create array for every seat type ID
            for stype in seatType:
                result[str(stype.seattype_id)] = []
                # print(f'& seat type : {stype.seattype_id}')

            # group tickets by its seat type ID
            for t in tickets:
                # print(f'& ticket : {t.ticket_id} ; seat type:{t.seattype_id}')
                result[str(t.seattype_id)].append(t)

        # print(f'& result array : {result}')
        # print(f'$ {type} / filter finish !! ')
        return result

    def resetTimezone(self, unit):
        """
        convert data's time field into diagram value
       :param unit:
       """
        ending = unit
        if unit is UnitType.year.value:
            ending -= 1
        for idx in range(0, ending):
            for d in self.data['Period ' + str(idx + 1)]:
                if unit is UnitType.day.value:  # day : hour period
                    d['Time'] = d['Time'].strftime("%H:%M") + "-" + (d['Time'] + pd.DateOffset(hours=2)).strftime("%H:%M")
                elif unit is UnitType.week.value:  # week : day date
                    d['Time'] = d['Time'].strftime("%m.%d")
                elif unit is UnitType.month.value:  # month : day period
                    if idx is 4:  # the end of last week is the end time of this report
                        d['Time'] = d['Time'].strftime("%m.%d") + "-" + (self.end - pd.DateOffset(days=1)).strftime("%m.%d")
                    else:
                        d['Time'] = d['Time'].strftime("%m.%d") + "-" + (d['Time'] + pd.DateOffset(weeks=1)).strftime("%m.%d")
                elif unit is UnitType.year.value:  # year : month period
                    right = d['Time'] + pd.DateOffset(months=1) - pd.DateOffset(days=1)
                    if right.year == d['Time'].year:
                        d['Time'] = d['Time'].strftime("%y.%m.%d") + "-" + right.strftime("%m.%d")
                    else:
                        d['Time'] = d['Time'].strftime("%y.%m.%d") + "-" + right.strftime("%y.%m.%d")

    def getAWT(self, storeID, unit):
        """
        generate AWT report for thr store
        :param storeID:
        :param unit:
        :return URL
        """
        # get array[ticket]
        tickets = Postgres.Ticket.select().where(Postgres.Ticket.store_id == storeID)
        # for t in tickets:
        #     print(f'# start time : {t.start_time}')

        # get seat type of the store
        seatType = Postgres.Seattype.select().where(Postgres.Seattype.store_id == storeID)
        # for s in seatType:
        #     print(f'# seat type id : {s.seattype_id}')

        # filter tickets by time
        tickets = self.Filter('time', tickets, unit, {})['time']

        newtickets = []
        ending = unit
        if unit is UnitType.year.value:
            ending -= 1

        # filter every time zone tickets by seat type
        idx = 0
        for tlist in tickets[:ending]:
            # if not tlist:
            #     break
            # print(f'# time zone : {idx}')
            idx += 1
            newtickets.append(self.Filter('seat', tlist, unit, seatType))

        # print('* new tickets filter by seat type')
        # print(newtickets)

        # save data and divided by period time
        Data = {}

        idx = 0
        # accumulate sum of waiting time of each seat type in every time zone
        for tlist in newtickets[:ending]:
            # print(f'# time zone : {idx} ---- ')
            # count unit begin time
            T = self.timeCount('+', self.begin, unit, idx)
            Data['Period ' + str(idx + 1)] = []
            for stype in seatType:
                # print(f'& seat type : {stype.seattype_id}')
                # only count when there are tickets
                AWT = {'Time': T, 'Seat Type': stype.name, 'Seat Type Id': stype.seattype_id, 'Average Wait Time': 0}
                # print(f'& ticket list : {tlist[str(stype.seattype_id)]}')
                # print(f'& list length : {len(tlist[str(stype.seattype_id)])}')
                if len(tlist[str(stype.seattype_id)]) > 0:
                    for t in tlist[str(stype.seattype_id)]:
                        # print(f"& ticket : {t.end_time} ; {t.start_time}")
                        # print(f"& ticket time : {t.end_time - t.start_time}")
                        AWT['Average Wait Time'] += (t.end_time - t.start_time).total_seconds() / 60
                    # print(f"# Sum AWT : {AWT['Average Wait Time']}")
                    # print(f'# ticket amount : {len(tlist[str(stype.seattype_id)])}')
                    AWT['Average Wait Time'] = int(
                        AWT['Average Wait Time'] / len(tlist[str(stype.seattype_id)]))  # assign new value to AWT
                # print(f'* AWT : {AWT}')
                Data['Period ' + str(idx + 1)].append(AWT)  # period : array[data{time;seattype;seattypeid;awt}]
                # print(f'* {Data}')
            idx += 1

        # print(f'* {Data}')

        # save generated data
        self.data = Data

    def getWCNandADN(self, storeID, unit):
        """
        generate WCN and ADN report for thr store
        :param storeID:
        :param unit:
        :return URL
        """
        # get array[ticket]1
        tickets = Postgres.Ticket.select().where(Postgres.Ticket.store_id == storeID)
        # for t in tickets:
        #     print(f'# start time : {t.start_time}')

        # filter tickets by time firstly
        tickets = self.Filter('time', tickets, unit, {})['time']

        newtickets = []
        ending = unit
        if unit is UnitType.year.value:
            ending -= 1
        idx = 0
        # filter tickets by status
        for tlist in tickets[:ending]:
            # print(f'# time zone : {idx}')
            idx += 1
            newtickets.append(self.Filter('status', tlist, unit, {}))

        # print('* new tickets filter by status')
        # print(newtickets)

        # save data and divided by period time
        Data = {}

        idx = 0
        for tlist in newtickets[:ending]:
            T = self.timeCount('+', self.begin, unit, idx)
            Data['Period ' + str(idx + 1)] = []
            for s in ticketStatus:
                num = {'Time': T, 'Status': s, 'Number': len(tlist[s])}
                # print(f'# data : {num}')
                Data['Period ' + str(idx + 1)].append(num)  # period : data{time;number
            # print(f'* {Data}')
            idx += 1

        # save generated data
        self.data = Data
