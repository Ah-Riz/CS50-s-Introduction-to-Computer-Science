import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # TODO: Read database file into a variable
    reader = []
    srt_list = []
    with open(sys.argv[1], "r") as file:
        data = csv.DictReader(file)
        for row in data:
            reader.append(row)
            if srt_list == []:
                srt_list = list(row.keys())
                srt_list.pop(0)  # Remove the 'name' header

    # TODO: Read DNA sequence file into a variable
    sequence = ""
    with open(sys.argv[2], "r") as file:
        data = csv.reader(file)
        sequence = next(data)[0]  # Assuming the sequence is in the first row and column
    
    # TODO: Find longest match of each STR in DNA sequence
    sequences = check_sequence(sequence, srt_list)

    # TODO: Check database for matching profiles
    name = check_database(reader, sequences)

    print(name)
    return

def check_database(reader, sequences):
    for row in reader:
        match = True
        for subsequence, count in sequences.items():
            if int(row[subsequence]) != count:
                match = False
                break
        if match:
            return row["name"]
    return "No match"

def check_sequence(sequence, srt_list):
    sequences = dict(zip(srt_list,[0] * len(srt_list)))
    for subsequence in sequences.keys():
        sequences[subsequence] = longest_match(sequence, subsequence)
    return sequences

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            
            # If there is no match in the substring
            else:
                break
        
        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
