# Data Extractor for Logfiles

The Data Extractor for Logfiles is a Python script with a graphical user interface (GUI) that allows users to extract specific information from large logfiles containing data for various types of reports. By using a standard logfile format across the fleet, this tool simplifies the process for new surveyors and reduces the risk of errors or discrepancies.

## Features

- Select multiple logfiles (CSV or TXT) for data extraction
- Automatically detect the delimiter used in the logfiles
- Load and select specific headers (columns) for extraction
- Specify a date and time range for filtering the data
- Merge the extracted data from multiple files into a single output file
- Automatically populate the date and time range based on the selected files

## Requirements

- Python 3.x
- pandas
- tkinter

## Installation

1. Clone the repository or download the script file.
2. Install the required dependencies using pip:
   e.g. pip install pandas

## Usage

1. Run the script using Python:
   e.g. py ScriptGUI.py
2. Click the "Select Files" button to choose the logfiles you want to extract data from.
3. Select a file and click the "Load Headers" button to load the available headers (columns).
4. Double-click on the desired headers in the "Select Headers" listbox to select them for extraction.
5. Specify the start and end date/time for filtering the data.
- You can manually enter the date and time in the format "DD/MM/YYYY HH:MM:SS".
- Alternatively, click the "Populate Time Range" button to automatically populate the date and time range based on the selected files.
6. Click the "Extract Data" button to extract and merge the selected data from the logfiles.
7. Choose a location and filename for the output file when prompted.
8. The extracted data will be saved as a CSV file in the specified location.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository. I'm new to this so any help and suggestions are encouraged!

## Contact

For any questions or inquiries, please contact Ricardo Barrera at richymx@gmail.com.



