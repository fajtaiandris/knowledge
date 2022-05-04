# 🎛️ Argument handling

```python
import sys, getopt

if __name__ == '__main__':
    #----------------------------- ARGS ----------------------------------------
    opts, args = getopt.getopt(sys.argv[1:], "i:o:f:p:")

    INPUT_PATH = None
    OUTPUT_PATH = None
    FAILED_PATH = None
    PREPROCESSING = None

    for opt, arg in opts:
        if opt in ['-i']:
            INPUT_PATH = arg
        elif opt in ['-o']:
            OUTPUT_PATH = arg
        elif opt in ['-f']:
            FAILED_PATH = arg
        elif opt in ['-p']:
            if (arg == "true") :
                PREPROCESSING = True
            else:
                PREPROCESSING = False
    if (INPUT_PATH is None
        or OUTPUT_PATH is None
        or FAILED_PATH is None
        or PREPROCESSING is None):
        print("USAGE:\n$ python3 tool3.py -i /input-folder/ -o /output-folder/ -f /failed-folder/ -p true")
        exit(2)
```
