# VUP: Version UPdater

&copy; 2019 SiLeader and Cerussite.

## features
+ version number management
+ support some version type
  + auto increment
  + manual increment (increment by command execute)
  + year, month, day
  + number of days from specified date
+ dependent only standard Python libraries

## version string format
`MAJOR.MINOR.BUILD.REVISION`

## usage
1. run `init` sub command to initialize project
1. run `generate` sub command to generate header file
1. run `update` sub command to update version number

`T` is position of version string.
`T` is `major`, `minor`, `build`, or `revision`.

### `init` sub command
+ `--T-type` is type of version number
+ `--T` is initial value
+ `--T-from` is starting point

#### Type
| type | meaning |
|:----:|:--------|
| `auto` | auto increment by update sub command |
| `manual` | manual increment by update sub command |
| `days` | number of days from specified date (`--T-from`) |
| `year` | year |
| `month` | month |
| `day` | day |
| `none` | not use this field |

### `generate` sub command
+ `--language` or `-x`: target language (C++ or C)
+ `--output` or `-o`: output basename
+ `--pre-update`: update before generate
+ `--post-update`: update after generate
+ `--standard` or `--std`: C++ standard version

## License
GNU General Public License version 3.0 (GPLv3.0)

See LICENSE.
