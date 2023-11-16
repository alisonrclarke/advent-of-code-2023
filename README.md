# Advent of Code 2023


## How to run

To run with the test input, run;

```
python day<day>.py test
```

Make sure to use the 2-digit day number as per the created file name.

And to run with the main input, run:

```
python day<day>.py
```

Sometimes (e.g. for those pesky times when your code works on the test input but not on the full input), you might want to create multiple test input files. If you create them with the naming convention `day<day>_test_input<suffix>.txt` then you can add the suffix to the command line and your new test file will be found, e.g. if you create an additional file `day07_test_input2.txt` then you can run:


```
python day07.py test 2
```

## utils

`utils.py` contains some useful functions for parsing the input file:

 * `input_as_string` returns the content of the input file as a string
 * `input_as_lines` returns a list where each line in the input file is an element of the list
 * `input_as_ints` returns a list where each line in the input file is an element of the list, converted into an integer


