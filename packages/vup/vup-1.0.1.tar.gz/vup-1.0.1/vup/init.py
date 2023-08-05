from . import setting
import datetime
import json


def __default_value(t: setting.Type):
    return {
        setting.Type.Auto: 'auto',
        setting.Type.Manual: 'manual',
        setting.Type.Year: 'year',
        setting.Type.Month: 'month',
        setting.Type.Day: 'day',
        setting.Type.Days: 'days',
        setting.Type.Null: '',
    }[t]
    pass


def __none_condition(t, nn, n):
    if t is None:
        return n()
    return nn(t)


def __elvis(t, ope):
    return __none_condition(t, ope, lambda: None)


def init(args):
    def __default_init_value(f: setting.Field):
        fd = __none_condition(f.days_from, lambda v: v, lambda: datetime.date.today())
        diff = datetime.date.today() - fd
        return {
            setting.Type.Auto: 0,
            setting.Type.Manual: 0,
            setting.Type.Year: datetime.date.today().year,
            setting.Type.Month: datetime.date.today().month,
            setting.Type.Day: datetime.date.today().day,
            setting.Type.Days: diff.days
        }[f.type]

    pref = setting.Setting(**{
        p: setting.Field(
            version_type=setting.Type(getattr(args, '{}_type'.format(p))),
            days_from=__elvis(getattr(args, '{}_from'.format(p)), lambda d: setting.fromisoformat(d))
        )
        for p in ('major', 'minor', 'build', 'revision')
    })

    lock = setting.Lock(**{
        p: setting.LockSingle(
            current=__none_condition(
                getattr(args, '{}'.format(p)),
                lambda v: v,
                lambda: __default_init_value(getattr(pref, p))))
        for p in ('major', 'minor', 'build', 'revision')
    })

    with open('vup.json', 'w') as fp:
        json.dump(pref.data, fp, ensure_ascii=False, indent=2)
    with open('vup-lock.json', 'w') as fp:
        json.dump(lock.data, fp, ensure_ascii=False, indent=2)
