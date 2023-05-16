Monaco Racing Report
Monaco Racing Report is a Python package that analyzes race data and generates a report of the fastest racers. It provides a command-line interface and supports various options.

Requirements
Documentation: The package includes module-level and function-level documentation to guide users on its usage and functionality.

The data files required for the analysis are stored in a separate folder within the package.

Build and Print Functions: The package contains two main functions:

build_report(files: str, order: str) -> [dict, dict]: Reads race data from files, calculates time differences, and returns dictionaries containing information about all racers and only the fastest racers.
print_report(files: str, order: str) -> NoReturn: Calls build_report function and prints the report of the fastest racers.

Command-Line Interface: The package includes a command-line interface with the following options:

--files <folder_path>: Specifies the path to the folder containing the race data files.
--order -o "<asc | desc>" (optional): Specifies the sorting order of the fastest racers' list. The default order is ascending.
--driver_info -d "<driver_name>" (optional): Prints statistics about a specific driver.


Example usage:

python report.py --order -o "[asc | desc]"
python report.py --files -f <folder_path> --driver "<driver_name>"
Python Package: The application is converted into a Python package, allowing it to be easily installed and used as a module in other projects.

Installation

To install Monaco Racing Report, follow these steps:

Clone the repository or download the source code.
Navigate to the package's root directory.
Run the following command to install the package and its dependencies:
pip install .