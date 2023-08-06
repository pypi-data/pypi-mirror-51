# YATREP - Yes, Another Test REsult Parser

# Usage

## Quick setup
You just need to run 'bin/run_parser.py' python file.
The only argument needed is the path to the xml file generated
by the C# nunit test.

```sh
python3 ./bin/run_parser.py xml_result_file.py
```
If all your tests are healthy it returns a 0 (success) code.
Otherwise, it returns -1.


# Development

## Running tests
To run tests, you must have 'nose' package installed. Also, we only
tested it with Python3.
```sh
./run_tests.sh
```
