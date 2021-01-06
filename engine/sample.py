import pandas as pd
from contextlib import redirect_stderr
import io, re, gc
from os import listdir
assert int(pd.__version__[0]) > 0,\
        f"the version of pandas {pd.__version__} is out of date, please upgrade to at least 1.0.0"

csvs = [file for file in listdir() if "data_" in file]
datafile = csvs[0]

#####
# # Redirect stderr to something we can report on.
# f = io.StringIO()
# with redirect_stderr(f):
#     df = pd.read_csv(
#         datafile, sep = "\t", error_bad_lines=False, warn_bad_lines=True, na_values = "_",
#     )
# if f.getvalue():
#     errorLines = [int(line[1:-2]) for line in re.findall(" [\d]+: ", f.getvalue())]

#####
# or simply ignore it

df = pd.read_csv(
        datafile, sep = "\t", error_bad_lines=False, warn_bad_lines=False, na_values = "_",
    )