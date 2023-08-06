# YATREP - Yes, Another Test REsult Parser

## Usage
You just need to run 'yatrep.sh' binary under 'bin' folder.
The only argument needed is the path to the xml file generated
by the C# nunit test.

```sh
./bin/yatrep.sh xml_result_file
```
If every test case is succeeded the script returns a 0 (success) code.
Otherwise, it returns -1.


## Running tests
To run tests, you must have 'nose' package installed. Also, we only
tested it with Python3.
```sh
./run_tests.sh
```
