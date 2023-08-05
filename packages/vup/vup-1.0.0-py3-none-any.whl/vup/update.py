import json

import setting


def do_update(pref, lock, **do_on_manual):
    u = False
    for t in ('major', 'minor', 'build', 'revision'):
        u = getattr(lock, t).update(
            getattr(pref, t),
            do_on_manual=do_on_manual[t],
            clear=u,
        )

    with open('vup-lock.json', 'w') as fp:
        json.dump(lock.data, fp, ensure_ascii=False, indent=2)


def update(args):
    with open('vup.json') as fp:
        pref = setting.Setting.create(json.load(fp))
    with open('vup-lock.json') as fp:
        lock = setting.Lock.create(json.load(fp))

    do_update(pref, lock, **{k: getattr(args, k) for k in ('major', 'minor', 'build', 'revision')})
