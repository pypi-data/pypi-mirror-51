import json
import re

from . import setting
from . import update


def __version_string(pref: setting.Setting, lock: setting.Lock):
    s = ''
    for t in ('major', 'minor', 'build', 'revision'):
        if getattr(pref, t).type != setting.Type.Null:
            s += str(getattr(lock, t).current) + '.'

    return s.rstrip('.')


def do_update(pref, lock):
    update.do_update(pref, lock, **{k: False for k in ('major', 'minor', 'build', 'revision')})


def generate(args):
    with open('vup.json') as fp:
        pref = setting.Setting.create(json.load(fp))
    with open('vup-lock.json') as fp:
        lock = setting.Lock.create(json.load(fp))

    if args.pre_update:
        do_update(pref, lock)

    file = args.output
    is_cxx = args.language == 'c++'
    file += '.hpp' if is_cxx else '.h'

    vs = re.sub(r'[^\d]+(\d+)', r'\1', args.standard)
    print(vs)
    cxx_version = int(vs)
    support_inline_variable = cxx_version >= 17

    with open(file, 'w') as fp:
        print('#ifndef VUP_AUTO_GENERATE_HEADER', file=fp)
        print('#define VUP_AUTO_GENERATE_HEADER', file=fp)

        print('', file=fp)
        if is_cxx:
            if cxx_version >= 17:
                print('#include <string_view>', file=fp)
            print('#include <string>', file=fp)
            print('', file=fp)
            print('namespace vup {', file=fp)
            if support_inline_variable:
                print(
                    '    inline constexpr std::string_view Version = "{}";'.format(__version_string(pref, lock)),
                    file=fp)
            print(
                '    inline std::string GetVersion() {' + 'return "{}";'.format(__version_string(pref, lock)) + '}',
                file=fp)
            print('} // namespace vup', file=fp)
        else:
            print(
                '    inline std::string VupGetVersion() {' + 'return "{}";'.format(__version_string(pref, lock)) + '}',
                file=fp)

        print('', file=fp)
        print('#endif // VUP_AUTO_GENERATE_HEADER', file=fp)

    if args.post_update:
        do_update(pref, lock)
