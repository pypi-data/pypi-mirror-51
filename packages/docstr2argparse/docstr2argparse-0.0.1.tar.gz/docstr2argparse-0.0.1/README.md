# Turn a docstring to argparse arguments.

This reduces the boilerplate for automatically creating command line scripts with python.
Probably other projects like this exist, but this one is small.
Right now we only support google style of documentation.
This will be augmented with time, and extra dependency upon 'docstring_parser' droped.
I needed this fast.

# How it works?

Consider this function with a long long description:
```{python}
def apex3d(raw_folder,
           output_dir,
           lock_mass_z2=785.8426,
           lock_mass_tol_amu=.25,
           low_energy_thr=300,
           high_energy_thr=30,
           lowest_intensity_thr=750,
           write_xml=True,
           write_binary=True,
           write_csv=False,
           max_used_cores=1,
           path_to_apex3d='C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe',
           PLGS=True,
           cuda=True,
           unsupported_gpu=True,
           debug=False,
           **kwds):
    """A wrapper around the infamous Apex3D.
    
    It wraps in Python what would otherwise had to be called with a batch script.
    Like a batch script? Com'on, this seriously sucks, just like all this Windows Crap.

    Args:
        raw_folder (str): a path to the input folder with raw Waters data.
        output_dir (str): Path to where to place the output.
        lock_mass_z2 (float): The lock mass for doubly charged ion (which one, dunno, but I guess a very important one).
        lock_mass_tol_amu (float): Tolerance around lock mass (in atomic mass units, amu).
        low_energy_thr (int): The minimal intensity of a precursor ion so that it ain't a noise peak.
        high_energy_thr (int): The minimal intensity of a fragment ion so that it ain't a noise peak.
        lowest_intensity_thr (int): The minimal intensity of a peak to be analyzed.
        write_xml (boolean): Write the output in an xml in the output folder.
        write_binary (boolean): Write the binary output in an xml in the output folder.
        write_csv (boolean): Write the output in a csv in the output folder (doesn't work).
        max_used_cores (int): The maximal number of cores to use.
        path_to_apex3d (str): Path to the "Apex3D.exe" executable.
        PLGS (boolean): No idea what it is.
        cuda (boolean): Use CUDA.
        unsupported_gpu (boolean): Try using an unsupported GPU for calculations. If it doesn't work, the pipeline switches to CPU which is usually much slower.
        debug (boolean): Debug mode.
        kwds: other parameters for 'subprocess.run'.
    
    Returns:
        tuple: the path to the outcome (no extension: choose it yourself and believe more in capitalism) and the completed process.
    """
    pass
```

Note the impoliteness towards Bill Gates' product in the long descroption.
In you custom command line script you can now simply write:

```{python}
from docstr2argparse import register_docs

parser = register_docs(apex3d)
args = parser.parse_args() # parser is just an 'argparse' parser object.

print(args.__dict__)
```

Now, running it all from terminal (hopefully on all major platforms, I tested it on Windows and Ubuntu), you will see:
```{bash}
$ python our_custom_script -h
usage: parse.py [-h] [--lock_mass_z2 LOCK_MASS_Z2]
                [--lock_mass_tol_amu LOCK_MASS_TOL_AMU]
                [--low_energy_thr LOW_ENERGY_THR]
                [--high_energy_thr HIGH_ENERGY_THR]
                [--lowest_intensity_thr LOWEST_INTENSITY_THR]
                [--write_xml WRITE_XML] [--write_binary WRITE_BINARY]
                [--write_csv WRITE_CSV] [--max_used_cores MAX_USED_CORES]
                [--path_to_apex3d PATH_TO_APEX3D] [--PLGS PLGS] [--cuda CUDA]
                [--unsupported_gpu UNSUPPORTED_GPU] [--debug DEBUG]
                raw_folder output_dir

A wrapper around the infamous Apex3D.

positional arguments:
  raw_folder            a path to the input folder with raw Waters data.
  output_dir            Path to where to place the output.

optional arguments:
  -h, --help            show this help message and exit
  --lock_mass_z2 LOCK_MASS_Z2
                        The lock mass for doubly charged ion (which one,
                        dunno, but I guess a very important one). [default =
                        785.8426]
  --lock_mass_tol_amu LOCK_MASS_TOL_AMU
                        Tolerance around lock mass (in atomic mass units,
                        amu). [default = 0.25]
  --low_energy_thr LOW_ENERGY_THR
                        The minimal intensity of a precursor ion so that it
                        ain't a noise peak. [default = 300]
  --high_energy_thr HIGH_ENERGY_THR
                        The minimal intensity of a fragment ion so that it
                        ain't a noise peak. [default = 30]
  --lowest_intensity_thr LOWEST_INTENSITY_THR
                        The minimal intensity of a peak to be analyzed.
                        [default = 750]
  --write_xml WRITE_XML
                        Write the output in an xml in the output folder.
                        [default = True]
  --write_binary WRITE_BINARY
                        Write the binary output in an xml in the output
                        folder. [default = True]
  --write_csv WRITE_CSV
                        Write the output in a csv in the output folder
                        (doesn't work). [default = False]
  --max_used_cores MAX_USED_CORES
                        The maximal number of cores to use. [default = 1]
  --path_to_apex3d PATH_TO_APEX3D
                        Path to the "Apex3D.exe" executable. [default =
                        C:/SYMPHONY_VODKAS/plgs/Apex3D64.exe]
  --PLGS PLGS           No idea what it is. [default = True]
  --cuda CUDA           Use CUDA. [default = True]
  --unsupported_gpu UNSUPPORTED_GPU
                        Try using an unsupported GPU for calculations. If it
                        doesn't work, the pipeline switches to CPU which is
                        usually much slower. [default = True]
  --debug DEBUG         Debug mode. [default = False]
```

Pretty neet, right?

# Installation
It should work under both Pythons, but use Python3 just to make Michał Startek feel old and useless.
```{bash}
pip3 install docstr2argparse
```