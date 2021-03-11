#!/usr/bin/env python
# coding: utf-8

# ## Check Input Sequences

# This notebook is dedicated to the handling and checking user inputs.
# 
# The user should only import the function:  seq = __Check_input(seq)__
# 
# * This function returns the origninal sequence if no issues are found.
# 
# 
# * The function all checks for a number of issues including empty strings, numeric inputs, short peptides sequences, and bad character inputs (e.g. '$').
# 
# 
# * The function also detects if the amino acid input sequence is in a three letter code format. It also checks if the three letter code is all upper case, lower case, or mixed case, and converts the three letter code into the single letter code representation. The fixed sequence is then returned.
# 

# In[400]:


Amino_acids = {'A':'Ala','G':'Gly','I':'Ile','L':'Leu','P':'Pro',
               'V':'Val','F':'Phe','W':'Trp','Y':'Tyr','D':'Asp',
               'E':'Glu','R':'Arg','H':'His','K':'Lys','S':'Ser',
               'T':'Thr','C':'Cys','M':'Met','N':'Asn','Q':'Gln',}



def Check_string(seq):
    if not isinstance(seq, str):
        assert False, "Input is not a string"

def Check_length(seq):
    if len(seq) < 2: # the shortest protein is TAL and it is 11 AA's long
        assert False, "The input "+"'"+seq+"'"+" is not an amino acid."
    elif len(seq) >=2 and len(seq) < 11: # the shortest protein is TAL and it is 11 AA's long
        assert False, "The peptide sequence "+"'"+seq+"'"+" is not an amino acid."
    else:
        pass
    
    
def check_empty(seq):
    """This function checks that the input is not empty or some null value.
    """
    issue = False
    if seq == []:
        issue = True
    elif seq == 'NaN':
        issue = True
    elif seq == 'NA':
        issue = True
    elif seq == '':
        issue = True
    elif seq.isspace() is True:
        issue = True
    else:
        pass
    if issue is True:
        assert False, ("The input is empty or not a valid input. " 
                        "Use only the single letter codes of the 20 essential amino acids")
    else:
        pass
        
        
         
def check_bad_chars(seq, Amino_acids):
    """ This checks for bad characters in amino acid string.
    """
    bad_characters = []
    for character in seq:
        if character not in Amino_acids.keys():
            bad_characters = bad_characters+[character]
        else:
            pass
    return bad_characters



# This raises an error if bad characters are found.
def raise_error_bad_char(bad_characters):
    """ This function just raises an assert if there are bad characters in the input.
    """
    if bad_characters != []:
        ', '.join(map(str, bad_characters))
        assert False, ("Your amino acid entry contains the following "
                                      "invalid characters: " + ', '.join(map(str, bad_characters))
                                      +". Use only the single letter codes of the 20 essential amino acids")
    else:
        pass



def check_for_three_letter_code(seq):
    """This code is checking to see if user entered three letter AA codes.
    """

    if not seq.islower() and not seq.isupper(): # Mixed sequence
        
        if len(seq)%3 == 0: # Could be three letter codes

            
            AA_code_len = 3
            # Get every three elements in string.
            AA_list = [seq[x:x+AA_code_len] for x in range(0, len(seq), AA_code_len)] 
            seq_new = '' 
            
            for AA in AA_list:
                if AA in Amino_acids.values():
                    
                    # Convert all three letter AA's to single letter AA's
                    for key, value in Amino_acids.items():
                        if AA == value:
                            seq_new += key
                    
                elif AA not in Amino_acids.values():
                    bad_characters = check_bad_chars(seq,Amino_acids)  
                    raise_error_bad_char(bad_characters)
                    
            return seq_new 
        
        else:
            assert False, ("The input is not a valid input. " 
                        "Use only the single letter codes of the 20 essential amino acids")
    
    elif seq.isupper(): # Check if three potential letter sequence is all upper case

        if len(seq)%3 == 0: # Could be three letter codes

            AA_code_len = 3
            AA_list = [seq[x:x+AA_code_len] for x in range(0, len(seq), AA_code_len)]
            seq_new = ''
            
            for AA in AA_list:
                if AA in {v.upper() for v in Amino_acids.values()}: # Checking if input is 3 letter upper case
                    # Convert all three letter AA's to single letter AA's
                    for key, value in Amino_acids.items():
                        if AA == value.upper():
                            seq_new += key
                            
                elif AA not in Amino_acids.values():
                    bad_characters = check_bad_chars(seq,Amino_acids)
                    if bad_characters == []:
                        return seq
                        break
                    else:
                        raise_error_bad_char(bad_characters)
            
            bad_characters = check_bad_chars(seq_new,Amino_acids)  
            raise_error_bad_char(bad_characters)
            return seq_new  
        
        bad_characters = check_bad_chars(seq,Amino_acids)  
        raise_error_bad_char(bad_characters)
        return False       
            
    elif seq.islower(): # Check if three potential letter sequence is all lower case 
#         assert False, ("The input is not a valid input. " 
#                         "Use only the upper case single letter codes of the 20 essential amino acids")

        if len(seq)%3 == 0: # Could be three letter codes

            AA_code_len = 3
            AA_list = [seq[x:x+AA_code_len] for x in range(0, len(seq), AA_code_len)]
            seq_new = ''
            
            for AA in AA_list:
                if AA in {v.lower() for v in Amino_acids.values()}: # Checking if input is 3 letter lower case
                    # Convert all three letter AA's to single letter AA's
                    for key, value in Amino_acids.items():
                        if AA == value.lower():
                            seq_new += key
                            
                elif AA not in {v.lower() for v in Amino_acids.values()}:
                    seq = seq.upper
                    bad_characters = check_bad_chars(seq,Amino_acids)
                    if bad_characters == []:
                        return seq
                        break
                    else:
                        raise_error_bad_char(bad_characters)
            
            bad_characters = check_bad_chars(seq_new,Amino_acids)  
            raise_error_bad_char(bad_characters)
            return seq_new  
        
        bad_characters = check_bad_chars(seq,Amino_acids)  
        raise_error_bad_char(bad_characters)
    else:
        return False 
    
def Check_input(seq):
    """ This function is the master function/ wrapper for the check input functions
    """
    Check_string(seq)
    Check_length(seq)
    check_empty(seq)

    output = ''
    output = check_for_three_letter_code(seq) 
    output
    if output != False:
        seq = output
        bad_characters = check_bad_chars(seq,Amino_acids)  
        raise_error_bad_char(bad_characters)
    else:
        pass
    return seq



### Example of running different cases for expected outcome and errors.
# # Six cases of different inputs cases.
# seq1 = 'ATGILPQNMCTFWDPSCVAGINMWRTC' # Case 1: Expected good input
# seq2 = '                     ' # Case 2 empty string
# seq3 = 'A' # Case 3 single amino acid
# seq4 = 'AAAAA' # Case 4 amino acid less than 11
# seq5 = 4 # Case 5 number input
# seq6 = 'ATGILPQXMCTFWDPSCUAGINMWRTC' # Case 6: Ambigious AA's
# seq7 = 'ATGIL$PQWMCTFWDPSCUAGINMWRTC' # Case 7: Bad characters in AA string
# seq8 = 'AlaHisLysThrValPheMetLysProTrpAsnGlnIleGlyArgLysArgCysSer' # Case 8: Three letter AA codes
# seq9 = 'ALAHISLYSTHRVALPHEMETLYSPROTRPASNGLNILEGLYARGLYSARGCYSSER' # Case 9: Three letter AA codes all upper case
# seq10 = 'alahislysthrvalphemetlysprotrpasnglnileglyarglysargcysgly' # Case 10: Three letter AA codes all lower case


# seq = seq1

# seq = Check_input(seq)
# print("Sequence = "+seq)

