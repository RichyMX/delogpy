#This script was created to extract specific information from large logfiles that contain all necessary data for all types of reports
#Using one standard logfile across the fleet makes it easier for new surveyors to continue the work and avoids unecessary errors or discrepancies
#  Data Extractor for Logfiles
#
#  Copyright (C) [2024] [Ricardo Barrera]
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import csv
import pandas as pd
import re
from datetime import datetime
from tkinter import Tk, filedialog, ttk, messagebox, Listbox, Scrollbar, Label, StringVar

def select_files():
    filepaths = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt"), ("CSV", "*.csv")])
    file_listbox.delete(0, 'end')
    for filepath in filepaths:
        file_listbox.insert('end', filepath)
    
    if filepaths:
        # Detect delimiter of the first selected file
        detected_delimiter = detect_delimiter(filepaths[0])
        delimiter_map = {',': 'Comma (,)', ';': 'Semicolon (;)', '\t': 'Tab (\\t)', ' ': 'Space ( )'}
        selected_delimiter = delimiter_map.get(detected_delimiter, 'Comma (,)')
        delimiter_combobox.set(selected_delimiter)


def load_headers():
    selected_indices = file_listbox.curselection()
    if not selected_indices:
        messagebox.showerror("Error", "Please select a file to load headers.")
        return

    selected_file = file_listbox.get(selected_indices[0])
    with open(selected_file, 'r', encoding='utf-8-sig') as infile:
        delimiter = detect_delimiter(selected_file)  # Ensure you have this function
        reader = csv.reader(infile, delimiter=delimiter)
        headers = next(reader)
        print(headers)  # This will print the headers to the console
        header_listbox.delete(0, 'end')
               # Print headers with their representations
        for header in headers:
            print(repr(header))  # This will show hidden characters
        for index, header in enumerate(headers):
            header_listbox.insert('end', f"[{index}] {header}")

def select_header(event):
    selected_indices = header_listbox.curselection()
    if not selected_indices:
        return

    selected_header = header_listbox.get(selected_indices[0])
    selected_listbox.insert('end', selected_header)
    header_listbox.delete(selected_indices[0])
    
def remove_header(event):
    selected_indices = selected_listbox.curselection()
    if not selected_indices:
        return

    selected_listbox.delete(selected_indices[0])

def detect_delimiter(filepath):
    with open(filepath, 'r', newline='', encoding='utf-8-sig') as file:
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(file.readline(), delimiters=",;\t ")
            return dialect.delimiter
        except csv.Error:
            # Default to comma if csv.Error is raised during sniffing
            return ','

def is_valid_date_time(row, date_format="%d/%m/%Y", time_format="%H:%M:%S"):
    try:
        datetime.strptime(row.iloc[0], date_format)
        datetime.strptime(row.iloc[1], time_format)
        return True
    except ValueError:
        return False

def extract_data():
    try:
        # This list will hold our dataframes
        dataframes = []
        
        # Get the selected files and headers
        selected_files = [file_listbox.get(idx) for idx in range(file_listbox.size())]
        selected_header_indices = [int(header.split(']')[0][1:]) for header in selected_listbox.get(0, 'end')]
        

        # Fetch the start and end datetime strings directly from the entry widgets
        start_datetime_str = start_datetime_entry.get()
        end_datetime_str = end_datetime_entry.get()

    
    
        if not start_datetime_str or not end_datetime_str:
            messagebox.showerror("Error", "Please specify the start and end date/time.")
            return
            
        start_datetime = datetime.strptime(start_datetime_str, "%d/%m/%Y %H:%M:%S")
        end_datetime = datetime.strptime(end_datetime_str, "%d/%m/%Y %H:%M:%S")
        
        
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid date/time format: {e}")
        return    
    
    try:
        # If only one file is selected, handle it separately
        if len(selected_files) == 1:
            single_file_path = selected_files[0]
            df = pd.read_csv(single_file_path, encoding='utf-8-sig')
            # Apply the non-header row filter
            df = df[df.apply(lambda row: is_valid_date_time(row), axis=1)]
            # Select columns by the indices after filtering
            df = df.iloc[:, selected_header_indices]
            if 0 not in selected_header_indices or 1 not in selected_header_indices:
                messagebox.showerror("Error", "Date and Time columns must be selected for datetime conversion.")
                return
            df['DateTime'] = pd.to_datetime(df.iloc[:, 0] + ' ' + df.iloc[:, 1], dayfirst=True)
            filtered_df = df[(df['DateTime'] >= start_datetime) & (df['DateTime'] <= end_datetime)]
            filtered_df = filtered_df.drop('DateTime', axis=1)
        else:
            # Process each selected file
            for file_index, file_path in enumerate(selected_files):
                # Read the CSV file
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            
                # If it's not the first file, remove any row that matches the header pattern
                if file_index != 0:
                    df = df[~df[df.columns[0]].str.contains('Date').fillna(False)]
            
                # Append the dataframe to our list
                dataframes.append(df)
            
            # Concatenate all dataframes
            combined_df = pd.concat(dataframes, ignore_index=True)
            
            # Select only the columns with the selected indices
            combined_df = combined_df.iloc[:, selected_header_indices]
            
            # Handle datetime and sorting (assuming first two selected indices are Date and Time)
            combined_df['DateTime'] = pd.to_datetime(combined_df.iloc[:, 0] + ' ' + combined_df.iloc[:, 1], dayfirst=True)
            combined_df.sort_values('DateTime', inplace=True)
            print(f"DataFrame before filtering:\n{combined_df[['DateTime']].head()}")
            # Filter the data based on the start_datetime and end_datetime
            filtered_df = combined_df[(combined_df['DateTime'] >= start_datetime) & (combined_df['DateTime'] <= end_datetime)]       
            print(f"DataFrame after filtering:\n{filtered_df[['DateTime']].head()}")
            # Remove the extra DateTime column for final output
            filtered_df.drop('DateTime', axis=1, inplace=True)
        
        # Save to a new CSV file
        output_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if output_file_path:
            filtered_df.to_csv(output_file_path, index=False)
            messagebox.showinfo("Success", "Data has been successfully extracted and merged into a single file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def populate_datetime_range():
    selected_files = file_listbox.get(0, 'end')
    if not selected_files:
        return

    min_datetime = None
    max_datetime = None

    for filepath in selected_files:
        with open(filepath, 'r', encoding='utf-8-sig') as infile:
            reader = csv.reader(infile)
            headers = next(reader)
            date_index = headers.index('Date')
            time_index = headers.index('Time')

            for row in reader:
                if len(row) > date_index and len(row) > time_index:
                    datetime_str = f"{row[date_index]} {row[time_index]}"
                    try:
                        current_datetime = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S")
                        if min_datetime is None or current_datetime < min_datetime:
                            min_datetime = current_datetime
                        if max_datetime is None or current_datetime > max_datetime:
                            max_datetime = current_datetime
                    except ValueError:
                        pass

    if min_datetime and max_datetime:
        start_datetime_var.set(min_datetime.strftime("%d/%m/%Y %H:%M:%S"))
        end_datetime_var.set(max_datetime.strftime("%d/%m/%Y %H:%M:%S"))

# Create the main window
window = Tk()
window.title("Data Extractor")

# File selection frame
file_frame = ttk.LabelFrame(window, text="Select Files")
file_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

file_listbox = Listbox(file_frame, selectmode='single', height=5)
file_listbox.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

file_scrollbar = Scrollbar(file_frame, orient='vertical', command=file_listbox.yview)
file_scrollbar.grid(row=0, column=1, sticky='ns')
file_listbox.config(yscrollcommand=file_scrollbar.set)

select_button = ttk.Button(file_frame, text="Select Files", command=select_files)
select_button.grid(row=1, column=0, padx=5, pady=5)

load_headers_button = ttk.Button(file_frame, text="Load Headers", command=load_headers)
load_headers_button.grid(row=2, column=0, padx=5, pady=5)

note_label = Label(file_frame, text="Need to highlight file to extract headers from")
note_label.grid(row=3, column=0, padx=5, pady=5)

# Header selection frame
header_frame = ttk.LabelFrame(window, text="Select Headers")
header_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

header_listbox = Listbox(header_frame, height=5)
header_listbox.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
header_listbox.bind('<Double-1>', select_header)

header_scrollbar = Scrollbar(header_frame, orient='vertical', command=header_listbox.yview)
header_scrollbar.grid(row=0, column=1, sticky='ns')
header_listbox.config(yscrollcommand=header_scrollbar.set)

selected_listbox = Listbox(header_frame, height=5)
selected_listbox.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
selected_listbox.bind('<Double-1>', remove_header)

selected_scrollbar = Scrollbar(header_frame, orient='vertical', command=selected_listbox.yview)
selected_scrollbar.grid(row=0, column=3, sticky='ns')
selected_listbox.config(yscrollcommand=selected_scrollbar.set)

# Date range frame
date_frame = ttk.LabelFrame(window, text="Date Range")
date_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

start_datetime_var = StringVar()
end_datetime_var = StringVar()

start_datetime_label = ttk.Label(date_frame, text="Start Date (DD/MM/YYYY):")
start_datetime_label.grid(row=0, column=0, padx=5, pady=5)
start_datetime_entry = ttk.Entry(date_frame, textvariable=start_datetime_var)
start_datetime_entry.grid(row=0, column=1, padx=5, pady=5)

end_datetime_label = ttk.Label(date_frame, text="End Date (DD/MM/YYYY):")
end_datetime_label.grid(row=0, column=2, padx=5, pady=5)
end_datetime_entry = ttk.Entry(date_frame, textvariable=end_datetime_var)
end_datetime_entry.grid(row=0, column=3, padx=5, pady=5)

populate_button = ttk.Button(date_frame, text="Populate Time Range", command=populate_datetime_range)
populate_button.grid(row=0, column=4, padx=5, pady=5)

# Extract button
extract_button = ttk.Button(window, text="Extract Data", command=extract_data)
extract_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Configure grid weights
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

file_frame.grid_rowconfigure(0, weight=1)
file_frame.grid_columnconfigure(0, weight=1)

header_frame.grid_rowconfigure(0, weight=1)
header_frame.grid_columnconfigure(0, weight=1)
header_frame.grid_columnconfigure(2, weight=1)

# Delimiter selection frame (Add this within your UI setup code)
delimiter_frame = ttk.LabelFrame(window, text="Select Delimiter")
delimiter_frame.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')

# Delimiter options
delimiter_options = ['Comma (,)', 'Semicolon (;)', 'Tab (\\t)', 'Space ( )']
delimiter_var = StringVar()
delimiter_var.set(delimiter_options[0])  # default to comma

delimiter_combobox = ttk.Combobox(delimiter_frame, textvariable=delimiter_var, values=delimiter_options, state='readonly')
delimiter_combobox.grid(row=0, column=0, padx=5, pady=5, sticky='ew')


# Start the main event loop
window.mainloop()