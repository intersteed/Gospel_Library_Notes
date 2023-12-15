"""The purpose of this program is to take a gospel library notes csv file
and format it into a readable text file there was a decoding issue using the rt
so I used rb(binary) on a seperate function which fixed the problem"""

def binary_approach(notes_file: str,output_file: str):
    """this function takes any text file and writes it to another text file
    and replaces any 157 character with 34
    """
    def return_34_if_byte_is_157(byte):
        if byte == 157:
            return 34
        else:
            return byte

    with open(notes_file, "rb") as infile, open(output_file, "wb") as outfile:
        for line in infile:
            if 157 in line:
                index = 0
                for byte in line:
                    if byte == 157:
                        line = bytes([return_34_if_byte_is_157(byte) for byte in line])
                    index += 1
            outfile.write(line)