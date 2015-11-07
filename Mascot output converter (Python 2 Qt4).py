############## MGF FILE CONVERTER
import sys
from PyQt4.QtGui import *
import csv

# Create a PyQt4 Application Object
a = QApplication(sys.argv)

# Before we start
w = QWidget()
selectionMessage = QMessageBox.information (w, "Mascot output converter", "This application will replace each 'Accession' name with the correspondent specific protein code")

# Message for selection (open)
w = QWidget()
selectionMessage = QMessageBox.information (w, "Mascot CSV file selection", "Select the Mascot CSV file to be converted")

# CSV file selection
w = QWidget()
inputfile = QFileDialog.getOpenFileName (w, 'Open CSV', '', 'CSV files (*.csv)')

# Message for selection (save)
w = QWidget()
selectionMessage = QMessageBox.information (w, "Mascot CSV file selection", "Select where to save the converted CSV file")

# Where to save the CSV file
w = QWidget()
outputfile = QFileDialog.getSaveFileName (w, 'Save CSV', '', 'CSV files (*.csv)')

### Add the extension to the file automatically
# Convert the outputfile into a string
outputfile = str(outputfile)
if not outputfile.endswith(".csv"):
    outputfile = outputfile + ".csv"



############################################# Conversion script
# Open the input file (in a temporary variable f)
with open(inputfile, "r") as f:
    # Read the actual csv values
    csvLines = csv.reader(f, delimiter=",", quotechar='\"')
    # Set a line threshold after which beginning the replacement
    threshold = False
    # Create the final list of lines
    outputLines = []
    # Scroll the lines of the CSV
    # Empty lines
    for line in csvLines:
        try:
            if line == "":
                outputLines.append (line)
            # If the line starts with "Family", this is the threshold
            elif line[0] == "Family":
                threshold = True
                outputLines.append (line)
            # If the line is before the threshold is set
            elif threshold is False:
                outputLines.append (line)
            # If the threshold has been set
            elif threshold is True:
                # Try to see if there is the protein code
                if line [len(line)-1] != " ":
                    # Replace the 4th element with the protein code (fixed, after the tr|)
                    protein_code = line [len(line)-1]
                    # Take only the first piece
                    protein_code = protein_code.split(",")[0]
                    if "tr|" in protein_code:
                        protein_code = protein_code.split()[0]
                    # Replace the fourth element with the protein code
                    line [3] = protein_code
                # If there is not, do not do nothing on the line
                else:
                    pass
                # Put the final line into the output file
                outputLines.append (line)
        except:
            outputLines.append (line)

with open (outputfile, 'w') as f:
    # Prepare to write the csv values with the function
    csvFileWrite = csv.writer(f)
    for line in outputLines:
        csvFileWrite.writerow (line)

# Conversion done!
w = QWidget()
selectionMessage = QMessageBox.information (w, "Mascot CSV conversion done", "The conversion has been successfully performed!")