from datetime import timedelta
from openprocurement.api.utils import calculate_certainly_business_date as ccbd


class Period(object):
    pass


class Date(object):
    pass


class AuctionDate(Date):
    name = 'auctionDate'

    def __init__(self):
        pass

    def __get__(self, instance, owner):
        self._date = ccbd(instance.rectificationPeriod.startDate, -timedelta(days=2))
        return self

    @property
    def date(self):
        return self._date


class TenderPeriod(Period):
    name = 'tenderPeriod'

    def __init__(self):
        self.duration = timedelta(days=3)
        self.working_days = False
        self.specific_hour = 20

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(self._startDate,
                                     self.duration,
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(self._endDate,
                                       -self.duration,
                                       working_days=self.working_days)
        elif instance.period == 'rectificationPeriod':
                self._startDate = instance.rectificationPeriod.endDate
                self._endDate = ccbd(self._startDate,
                                     self.duration,
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'enquiryPeriod':
                self._startDate = instance.enquiryPeriod.startDate
                self._endDate = ccbd(self._startDate,
                                     self.duration,
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'auctionDate':
                self._startDate = instance.rectificationPeriod.startDate
                self._endDate = ccbd(self._startDate,
                                     self.duration,
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        return self

    @property
    def endDate(self):
        return self._endDate

    @property
    def startDate(self):
        return self._startDate


class RectificationPeriod(Period):
    name = 'rectificationPeriod'

    def __init__(self):
        self.duration = timedelta(2)
        self.working_days = False

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(self._startDate, self.duration)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(self._endDate, -self.duration)
        elif instance.period == 'tenderPeriod':
                self._endDate = instance.tenderPeriod.startDate
                self._startDate = ccbd(self._endDate, -self.duration)
        elif instance.period == 'enquiryPeriod':
                self._endDate = instance.enquiryPeriod.startDate
                self._startDate = ccbd(self._endDate, -self.duration)
        elif instance.period == 'auctionDate':
                self._startDate = ccbd(instance.auctionDate.date, timedelta(days=3))
                self._endDate = ccbd(self._startDate, self.duration)
        return self

    @property
    def endDate(self):
        return self._endDate

    @property
    def startDate(self):
        return self._startDate


class EnquiryPeriod(Period):
    name = 'enquiryPeriod'

    def __init__(self):
        self.working_days = False

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(instance.auctionPeriod.shouldStartAfter, -timedelta(days=1))
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = instance.tender.Period.startDate

        elif instance.period == 'rectificationPeriod':
                self._startDate = instance.tenderPeriod.startDate
                self._endDate = ccbd(instance.tenderPeriod.endDate, timedelta(days=1))
        elif instance.period == 'tenderPeriod':
                self._startDate = instance.tenderPeriod.startDate
                self._endDate = ccbd(instance.tenderPeriod.endDate, timedelta(days=1))
        elif instance.period == 'auctionDate':
                self._startDate = instance.tenderPeriod.startDate
                self._endDate = ccbd(instance.tenderPeriod.endDate, timedelta(days=1))
        return self

    @property
    def endDate(self):
        return self._endDate

    @property
    def startDate(self):
        return self._startDate


class AuctionPeriod(Period):
    name = 'auctionPeriod'

    def __init__(self):
        self.default = 0

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'shouldStartAfter':
                self._shouldStartAfter = instance.time

        elif instance.period == 'rectificationPeriod':
                self._shouldStartAfter = ccbd(instance.enquiryPeriod.endDate, timedelta(days=1))
        elif instance.period == 'tenderPeriod':
                self._shouldStartAfter = ccbd(instance.enquiryPeriod.endDate, timedelta(days=1))
        elif instance.period == 'auctionDate':
                self._shouldStartAfter = ccbd(instance.auctionDate.date, timedelta(days=14))
        elif instance.period == 'enquiryPeriod':
                self._shouldStartAfter = ccbd(instance.enquiryPeriod.endDate, timedelta(days=1))
        return self

    @property
    def shouldStartAfter(self):
        return self._shouldStartAfter


class Calculator(object):
    rectificationPeriod = RectificationPeriod()
    tenderPeriod = TenderPeriod()
    enquiryPeriod = EnquiryPeriod()
    auctionPeriod = AuctionPeriod()
    auctionDate = AuctionDate()

    def __init__(self, time, period, state):
        self.time = time
        self.period = period
        self.state = state
