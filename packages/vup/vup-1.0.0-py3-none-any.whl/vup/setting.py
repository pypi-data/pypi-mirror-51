import enum
import typing
import datetime


def fromisoformat(d):
    dt = datetime.datetime.strptime(d, '%Y-%m-%d')
    return datetime.date(dt.year, dt.month, dt.day)


class Type(enum.Enum):
    Auto = 'auto'
    Manual = 'manual'
    Year = 'year'
    Month = 'month'
    Day = 'day'
    Days = 'days'
    Null = 'none'


class LockSingle:
    def __init__(self, current: int):
        self.__current = current
        
    @staticmethod
    def create(data):
        return LockSingle(
            current=data['current']
        )

    @property
    def current(self):
        return self.__current
    
    def update(self, f: 'Field', do_on_manual=False, clear=False, do_clear_on_date=False):
        if f.type == Type.Null:
            return False
        if clear:
            if f.is_date:
                if do_clear_on_date:
                    self.clear()
                    return True
            else:
                self.clear()
                return True

        if not do_on_manual and f.type == Type.Manual:
            return clear
        if f.days_from is None:
            fd = datetime.date.today()
        else:
            fd = f.days_from
        diff = datetime.date.today() - fd
        self.__current = {
            Type.Auto: self.__current + 1,
            Type.Manual: self.__current + 1,
            Type.Year: datetime.date.today().year,
            Type.Month: datetime.date.today().month,
            Type.Day: datetime.date.today().day,
            Type.Days: diff.days
        }[f.type]
        return clear if f.is_date else True

    def clear(self):
        self.__current = 0

    @property
    def data(self):
        return {
            'current': self.current
        }


class Lock:
    def __init__(self, major: LockSingle, minor: LockSingle, build: LockSingle, revision: LockSingle):
        self.__major = major
        self.__minor = minor
        self.__build = build
        self.__revision = revision
        
    @staticmethod
    def create(data):
        return Lock(
            major=LockSingle.create(data['major']),
            minor=LockSingle.create(data['minor']),
            build=LockSingle.create(data['build']),
            revision=LockSingle.create(data['revision']),
        )

    @property
    def major(self):
        return self.__major

    @property
    def minor(self):
        return self.__minor

    @property
    def build(self):
        return self.__build

    @property
    def revision(self):
        return self.__revision

    @property
    def data(self):
        return {
            'major': self.major.data,
            'minor': self.minor.data,
            'build': self.build.data,
            'revision': self.revision.data,
        }


class Field:
    def __init__(self, version_type: Type, days_from: typing.Optional[datetime.date] = None):
        self.__type = version_type
        self.__from = days_from

    @staticmethod
    def create(data):
        return Field(
            version_type=Type(data['type']),
            days_from=fromisoformat(data['from']) if 'from' in data and data['from'] is not None else None
        )

    @property
    def type(self):
        return self.__type

    @property
    def days_from(self):
        return self.__from

    @property
    def is_date(self):
        return self.type in (Type.Year, Type.Month, Type.Day, Type.Days)

    @property
    def data(self):
        return {
            'type': self.type.value,
            'from': self.days_from.isoformat() if self.days_from is not None else None
        }


class Setting:
    def __init__(self, major: Field, minor: Field, build: Field, revision: Field):
        self.__major = major
        self.__minor = minor
        self.__build = build
        self.__revision = revision

    @staticmethod
    def create(data):
        return Setting(
            major=Field.create(data['major']),
            minor=Field.create(data['minor']),
            build=Field.create(data['build']),
            revision=Field.create(data['revision']),
        )

    @property
    def major(self) -> Field:
        return self.__major

    @property
    def minor(self) -> Field:
        return self.__minor

    @property
    def build(self) -> Field:
        return self.__build

    @property
    def revision(self) -> Field:
        return self.__revision

    @property
    def data(self):
        return {
            'major': self.major.data,
            'minor': self.minor.data,
            'build': self.build.data,
            'revision': self.revision.data,
        }
