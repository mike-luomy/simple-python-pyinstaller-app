import csv
import xml.etree.ElementTree as ET
import sys

def xml_to_csv(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['File', 'Line', 'Hits', 'Misses', 'Branch', 'Hits'])  # Adjust columns as needed

        for package in root.findall('packages/package'):
            for class_ in package.findall('classes/class'):
                filename = class_.get('filename')
                for line in class_.findall('lines/line'):
                    line_number = line.get('number')
                    hits = line.get('hits')
                    branch = line.get('branch')  # If branches are present
                    condition_coverage = line.get('condition-coverage')  # If conditions are present

                    csvwriter.writerow([filename, line_number, hits, branch, condition_coverage])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_coverage_xml_to_csv.py <input.xml> <output.csv>")
        sys.exit(1)

    xml_file = sys.argv[1]
    csv_file = sys.argv[2]

    xml_to_csv(xml_file, csv_file)
