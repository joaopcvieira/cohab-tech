import pandas as pd
import re
from fuzzywuzzy import process

CERTAINTY = 95


def remove_accents_and_special_characters(word: str) -> str:
    """
    It removes accents and special characters from a word

    :param word: The word to be processed
    :return: A string with all the accents and special characters removed.
    """
    word = word.lower().strip(' ')
    word = re.sub(pattern=r'[àáâãäå]', repl='a', string=word)
    word = re.sub(pattern=r'[èéêë]', repl='e', string=word)
    word = re.sub(pattern=r'[ìíîï]', repl='i', string=word)
    word = re.sub(pattern=r'[òóôõö]', repl='o', string=word)
    word = re.sub(pattern=r'[ùúûü]', repl='u', string=word)
    word = re.sub(
        # Remove anything that is not a word or digit
        pattern=r'[^a-zA-Z0-9\s]', repl='', string=word
    )
    return word


def fix_cpf(cpf):
    """
    It takes a cpf, removes all the dots, dashes, and spaces, and then adds a zero
    to the front if it's missing

    :param cpf: The CPF number you want to validate
    :return: the cpf variable.
    """
    cpf = str(cpf)
    cpf = cpf.replace('.', '').replace('-', '').replace(' ', '')
    if(len(cpf) == 11):
        return cpf
    elif(len(cpf) == 10):
        return '0' + cpf
    else:
        return "ERRO CPF INVALIDO"


def fix_number(number):
    """
    It takes a number as a string, replaces all commas with dots, and then tries to convert it to a
    float. 
    If it fails, it returns 0
    
    :param number: The number to be fixed
    :return: A float
    """

    number = str(number)
    try:
        number = float(number.replace('.', '').replace(',', '.'))
    except:
        number = 0
    return number


def fix_cel(cel):
    """
    It takes a string, removes all the parenthesis, dashes, and spaces, and then checks to see if the
    length of the string is 10 or 11. If it is, it returns the string. If it's not, it returns an error
    message

    :param cel: The cell phone number
    :return: the fixed cell phone number.
    """
    cel = str(cel)
    cel = cel.replace('(', '').replace(')', '').replace(
        '-', '').replace(' ', '')
    if(len(cel) == 11):
        return cel
    elif(len(cel) == 10):
        return cel
    else:
        return "ERRO CEL INVALIDO"


def is_name_in_list(name: str, names_list: list, certainty=CERTAINTY) -> tuple:
    """
    It checks if the name is in the names_list

    :param name: The name you want to check
    :param names_list: The list of names you want to check against
    :param certainty: The certainty you want to check against
    :return: True if the name is in the list, False otherwise
    """
    name = remove_accents_and_special_characters(name)
    temp_name_list = [remove_accents_and_special_characters(name) for name in names_list]

    best_name, best_certainty = process.extractOne(name, temp_name_list)
    if best_certainty >= certainty:
        return [True, process.extractOne(best_name, names_list)[0]]
    else:
        return [False, ""]

    
    # for n in names_list:
    #     temp = remove_accents_and_special_characters(n)
    #     if name == temp:
    #         return [True, n]
    #     elif process.extractOne(name, [temp])[1] >= certainty:
    #         return [True, n]
    # return [False, ""]


def is_name_equivalent(name1 = "", name2 = "", certainty=CERTAINTY) -> tuple:
    """
    It checks if the name1 is equivalent to name2

    :param name1: The name you want to check
    :param name2: The name you want to check against
    :param certainty: The certainty you want to check against
    :return: True if the name is in the list, False otherwise
    """
    name1 = remove_accents_and_special_characters(name1)
    name2 = remove_accents_and_special_characters(name2)
    if name1 == name2:
        return [True, 100]
    elif process.extractOne(name1, [name2])[1] >= certainty:
        return [True, process.extractOne(name1, [name2])[1]]

    return [False, process.extractOne(name1, [name2])[1]]


def name_and_nickname_test(name1: str, nickname1: str, name2: str, nickname2: str, certainty=CERTAINTY) -> bool:
    """
    If the names are equivalent, return True. If the names are not equivalent, but the nicknames are,
    return True. Otherwise, return False

    :param name1: str, nickname1: str, name2: str, nickname2: str, certainty=CERTAINTY
    :type name1: str
    :param nickname1: str, nickname2: str,
    :type nickname1: str
    :param name2: str, nickname2: str, certainty=CERTAINTY
    :type name2: str
    :param nickname2: str, certainty=CERTAINTY
    :type nickname2: str
    :param certainty: The certainty that the names are equivalent
    :return: A boolean value.
    """
    name1 = remove_accents_and_special_characters(name1)
    name2 = remove_accents_and_special_characters(name2)
    nickname1 = remove_accents_and_special_characters(nickname1)
    nickname2 = remove_accents_and_special_characters(nickname2)
    if is_name_equivalent(name1, name2, certainty)[0]:
        return True
    elif is_name_equivalent(name1, name2, certainty=70)[0] and is_name_equivalent(nickname1, nickname2, certainty=85)[0]:
        return True
    else:
        return False


def is_name_and_apelido_in_list(name: str, apelido: str, names_list: list, apelido_list: list, certainty=CERTAINTY) -> tuple:
    """
    It checks if the name is in the names_list

    :param name: The name you want to check
    :param apelido: The apelido you want to check
    :param names_list: The list of names you want to check against
    :param apelido_list: The list of apelidos you want to check against
    :param certainty: The certainty you want to check against
    :return: True if the name is in the list, False otherwise
    """
    name = remove_accents_and_special_characters(name)
    apelido = remove_accents_and_special_characters(apelido)


    best_name, best_certainty_name = process.extractOne(name, names_list)
    best_apelido, best_certainty_apelido = process.extractOne(apelido, apelido_list)

    if best_certainty_name >= certainty:
        return [True,
                process.extractOne(best_name, names_list)[1],
                best_apelido]

    if is_name_in_list(name=name, names_list=names_list, certainty=85)[0] and \
            is_name_in_list(apelido, names_list=apelido_list, certainty=90)[0]:
        return [True,
                is_name_in_list(
                    name=name, names_list=names_list, certainty=80)[1],
                is_name_in_list(
                    apelido, names_list=apelido_list, certainty=90)[1]
                ]
    else:
        return [False, "", ""]

