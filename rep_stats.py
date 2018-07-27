import argparse
import csv

def run_script(script, stdin=None):
    """Returns (stdout, stderr), raises error on non-zero return code"""
    import subprocess
    # Note: by using a list here (['bash', ...]) you avoid quoting issues, as the 
    # arguments are passed in exactly this order (spaces, quotes, and newlines won't
    # cause problems):
    proc = subprocess.Popen(['bash', '-c', script],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode:
        raise ScriptException(proc.returncode, stdout, stderr, script)
    return stdout, stderr

class ScriptException(Exception):
    def __init__(self, returncode, stdout, stderr, script):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        Exception.__init__('Error in script')

parser = argparse.ArgumentParser(description='Process L1Base csv in order to obtain LINEs statistics')
parser.add_argument('input_filename', type = str, nargs = 1, help = 'LINEs CSV filename')
parser.add_argument('output_filename', type = str, nargs = 1, help = 'Output files name (e.g.: if \'horse\' is entered, two files (lines-horse.csv and lines-horse.fasta) will be generated)')
parser.add_argument('chromosome_filename', type = str, nargs = 1, help = 'Chromosomes folder and part of the filename (e.g.: \'human/Homo_sapiens.GRCh38.dna.chromosome.\')')
args = parser.parse_args()

input_filename = args.input_filename[0]
run_script('sed -i -E \'s/\",\"/\"$\"/g\' ' + input_filename)
output_substring = args.output_filename[0]
output_file = open('lines-' + output_substring + '.csv', 'w')
multifasta_file = open('lines-' + output_substring + '.fasta', 'w')
chromosome_filename = args.chromosome_filename[0]
output_file.write('ID,CHROMOSOME,START,END,LENGTH,LINE\n')
written_sequences = 0

with open(input_filename) as csvfile:
    next(csvfile)
    readCSV = csv.reader(csvfile, delimiter='$')
    for row in readCSV:
        print(row[0])
        start = min(int(row[3]), int(row[4]))
        end = max(int(row[3]), int(row[4]))
        length = end - start
        chromosome = row[2]
        repeat = ''
        current_index = 0
        with open(chromosome_filename + chromosome + '.fa') as infile:
            next(infile)
            write_flag = True
            for line in infile:
                if current_index + len(line) < start:
                    current_index = current_index + len(line) - 1
                elif current_index > end:
                    break
                else:
                    for character in line:
                        if current_index > start and current_index < end:
                            if(character != '\n'):
                                if character == 'N':
                                    write_flag = False
                                    break
                                repeat += character
                                # written_nucleotides += 1
                                # if written_nucleotides % 70 == 0:
                                    # repeat += '\n    '
                                current_index = current_index + 1
                        else:
                            current_index = current_index + 1
            if write_flag:
                written_sequences += 1
                multifasta_file.write('> ' + output_substring + '_' + str(written_sequences) + '_' + chromosome + '\n' + repeat + '\n*\n')
                output_file.write(str(written_sequences) + ',' + chromosome + ',' + str(start) + ',' + str(end) + ',' + str(length) + ',' + repeat + '\n')