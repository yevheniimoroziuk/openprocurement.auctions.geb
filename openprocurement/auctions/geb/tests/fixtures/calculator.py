from datetime import timedelta
from openprocurement.auctions.geb.utils import calculate_certainly_business_date as ccbd


class Period(object):
    pass


class Date(object):
    pass

# Auction Calculator


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
        self.working_days = False
        self.specific_hour = 20

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(instance.auctionPeriod.startDate,
                                     -timedelta(days=4),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(self._endDate,
                                       -timedelta(days=10))

        elif instance.period == 'rectificationPeriod':
                self._startDate = instance.rectificationPeriod.endDate
                self._endDate = ccbd(instance.auctionPeriod.startDate,
                                     -timedelta(days=4),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)

        elif instance.period == 'enquiryPeriod':
                self._startDate = ccbd(instance.enquiryPeriod.startDate,
                                       timedelta(days=2))
                self._endDate = ccbd(instance.auctionPeriod.startDate,
                                     -timedelta(days=4),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)

        elif instance.period == 'auctionDate':
                self._startDate = ccbd(self.auctionDate.date,
                                       timedelta(days=5))
                self._endDate = ccbd(instance.auctionPeriod.startDate,
                                     -timedelta(days=4),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)

        elif instance.period == 'auctionPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=16))

                self._endDate = ccbd(instance.time,
                                     -timedelta(days=4),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)

        elif instance.period == 'qualificationPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=15))

                self._endDate = ccbd(instance.time, -timedelta(days=4))

        elif instance.period == 'awardPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=15))

                self._endDate = ccbd(instance.time, -timedelta(days=4))
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
                self._endDate = instance.tenderPeriod.startDate
                self._startDate = ccbd(self._endDate, -self.duration)

        elif instance.period == 'auctionDate':
                self._startDate = ccbd(instance.auctionDate.date, timedelta(days=3))
                self._endDate = ccbd(self._startDate, self.duration)

        elif instance.period == 'auctionPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=18))

                self._endDate = ccbd(instance.time, -timedelta(days=14))

        elif instance.period == 'qualificationPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=19))

                self._endDate = ccbd(instance.time, -timedelta(days=15))

        elif instance.period == 'awardPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=19))

                self._endDate = ccbd(instance.time, -timedelta(days=15))
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
        self.specific_hour = 20

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(instance.auctionPeriod.startDate,
                                     -timedelta(days=1),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(instance.time, -timedelta(days=14))

        elif instance.period == 'rectificationPeriod':
                self._startDate = instance.time
                self._endDate = ccbd(instance.auctionPeriod.startDate,
                                     -timedelta(days=1),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'tenderPeriod':
                self._startDate = ccbd(instance.tenderPeriod.startDate,
                                       -timedelta(days=2))
                self._endDate = ccbd(instance.auctionPeriod.startDate,
                                     -timedelta(days=1),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'qualificationPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=19))
                self._endDate = ccbd(instance.time,
                                     -timedelta(days=2),
                                     specific_hour=self.specific_hour)

        elif instance.period == 'awardPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=19))
                self._endDate = ccbd(instance.time,
                                     -timedelta(days=2),
                                     specific_hour=self.specific_hour)

        elif instance.period == 'auctionDate':
                self._startDate = ccbd(instance.auctionDate.date,
                                       timedelta(days=1))
                self._endDate = ccbd(instance.auctionPeriod.startDate,
                                     -timedelta(days=1),
                                     working_days=self.working_days,
                                     specific_hour=self.specific_hour)
        elif instance.period == 'auctionPeriod':
                self._startDate = ccbd(instance.time, -timedelta(days=18))

                self._endDate = ccbd(instance.time,
                                     -timedelta(days=1),
                                     specific_hour=self.specific_hour)
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
            if instance.state == 'start':
                self._startDate = instance.time

        elif instance.period == 'rectificationPeriod':
                # auction starts 14 days after the rectificationPeriod start
                self._startDate = ccbd(instance.time, timedelta(days=14))
        elif instance.period == 'tenderPeriod':
                # auction starts 12 days after the tenderPeriod start
                self._startDate = ccbd(instance.time, timedelta(days=12))
        elif instance.period == 'enquiryPeriod':
            if instance.state == 'start':
                # auction starts 12 days after the enquiryPeriod start
                self._startDate = ccbd(instance.time, timedelta(days=12))
            elif instance.state == 'end':
                # auction starts in same time as  enquiryPeriod end
                self._startDate = instance.time
        elif instance.period == 'qualificationPeriod':
                # auction starts day defore qualification Period start
                self._startDate = ccbd(instance.time, -timedelta(days=0), specific_hour=10)
                # auction ends day defore at 17 00 qualification Period start
                self._endDate = ccbd(instance.time, -timedelta(days=0), specific_hour=16)
        elif instance.period == 'awardPeriod':
                # auction starts day defore qualification Period start
                self._startDate = ccbd(instance.time, -timedelta(days=0), specific_hour=10)
                # auction ends day defore at 17 00 qualification Period start
                self._endDate = ccbd(instance.time, -timedelta(days=0), specific_hour=16)
        elif instance.period == 'auctionDate':
                # Procedure starts 14 days after
                self._startDate = ccbd(instance.time, timedelta(days=14))

        return self

    @property
    def startDate(self):
        return self._startDate

    @property
    def endDate(self):
        return self._endDate


class AwardPeriod(Period):
    name = 'awardPeriod'

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(instance.time, -timedelta(days=0), specific_hour=16)
        elif instance.period == 'qualificationPeriod':
                self._startDate = instance.auctionPeriod.endDate
        return self

    @property
    def startDate(self):
        return self._startDate

    @property
    def endDate(self):
        return self._endDate


class QualificationPeriod(Period):
    name = 'qualificationPeriod'


class Calculator(object):
    auctionDate = AuctionDate()
    auctionPeriod = AuctionPeriod()
    awardPeriod = AwardPeriod()
    enquiryPeriod = EnquiryPeriod()
    qualificationPeriod = QualificationPeriod()
    rectificationPeriod = RectificationPeriod()
    tenderPeriod = TenderPeriod()

    def __init__(self, time, period, state):
        self.time = time
        self.period = period
        self.state = state

# Award Calculator


class AwardVerificationPeriod(Period):
    name = 'verificationPeriod'

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(instance.time, timedelta(days=0), specific_hour=18)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(instance.time, -timedelta(days=0), specific_hour=16)

        elif instance.period == 'signingPeriod':
                self._startDate = instance.signingPeriod.startDate
                self._endDate = ccbd(instance.signingPeriod.startDate, -timedelta(days=0), specific_hour=18)
        return self

    @property
    def startDate(self):
        return self._startDate

    @property
    def endDate(self):
        return self._endDate


class AwardSigningPeriod(Period):
    name = 'signingPeriod'

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(instance.time, timedelta(days=0), specific_hour=23) + timedelta(minutes=59)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(instance.time, -timedelta(days=0), specific_hour=16)
        elif instance.period == 'verificationPeriod':
                self._startDate = instance.verificationPeriod.startDate
                self._endDate = ccbd(instance.verificationPeriod.startDate, timedelta(days=0), specific_hour=23) + timedelta(minutes=59)
        return self

    @property
    def startDate(self):
        return self._startDate

    @property
    def endDate(self):
        return self._endDate


class AwardComplaintPeriod(Period):
    name = 'complaintPeriod'

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(instance.time, timedelta(days=0), specific_hour=18)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(instance.time, -timedelta(days=0), specific_hour=16)

        elif instance.period == 'verificationPeriod':
                self._startDate = instance.verificationPeriod.startDate
                self._endDate = instance.verificationPeriod.endDate
        elif instance.period == 'signingPeriod':
                self._startDate = ccbd(instance.signingPeriod.startDate, -timedelta(days=0), specific_hour=16)
                self._endDate = ccbd(instance.signingPeriod.startDate, -timedelta(days=0), specific_hour=18)
        return self

    @property
    def startDate(self):
        return self._startDate

    @property
    def endDate(self):
        return self._endDate


class AwardDate(Date):
    name = 'date'

    def __get__(self, instance, owner):
        if instance.period == 'verificationPeriod':
                self._date = instance.verificationPeriod.startDate
        elif instance.period == 'signingPeriod':
                self._date = instance.verificationPeriod.startDate
        return self._date


class AwardCalculator(object):
    verificationPeriod = AwardVerificationPeriod()
    signingPeriod = AwardSigningPeriod()
    complaintPeriod = AwardComplaintPeriod()
    date = AwardDate()

    def __init__(self, time, period, state):
        self.time = time
        self.period = period
        self.state = state


class ContractSigningPeriod(Period):
    name = 'signingPeriod'

    def __get__(self, instance, owner):
        if instance.period == self.name:
            if instance.state == 'start':
                self._startDate = instance.time
                self._endDate = ccbd(instance.time, timedelta(days=0), specific_hour=23) + timedelta(minutes=59)
            elif instance.state == 'end':
                self._endDate = instance.time
                self._startDate = ccbd(instance.time, -timedelta(days=0), specific_hour=16)
        return self

    @property
    def startDate(self):
        return self._startDate

    @property
    def endDate(self):
        return self._endDate


class ContractDate(Date):
    name = 'date'

    def __get__(self, instance, owner):
        if instance.period == 'signingPeriod':
            self._date = instance.signingPeriod.startDate
        return self._date


class ContractCalculator(object):
    signingPeriod = ContractSigningPeriod()
    date = ContractDate()

    def __init__(self, time, period, state):
        self.time = time
        self.period = period
        self.state = state
