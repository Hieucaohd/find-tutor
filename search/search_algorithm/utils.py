import rapidfuzz
# import pylcs
import re
import unidecode

def replace_special_character(text: str) -> str:
    if not text:
        return text

    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    list_word = text.split()

    list_word_normal = (re.sub(r'[^\w\s]', '', word) for word in list_word)

    result = " ".join(list_word_normal)
    result = unidecode.unidecode(result)
    return result


def compare_two_string(text_1: str, text_2: str) -> int:
    if not text_2 or not text_1:
        return 0

    levenshtein_dis = rapidfuzz.string_metric.levenshtein(text_1, text_2)
    # common_substring= pylcs.lcs2(text_1, text_2)
    # common_subsequen = pylcs.lcs(text_1, text_2)

    common_substring_phan_tram = common_substring / len(text_1) * 100
    common_subsequen_phan_tram = common_subsequen / len(text_1) * 100

    # thông số thử nghiệm:
    # hamming 
    limit_same_length_hamming = 2
    score_same_length_hamming = 1000

    # levenshtein same length
    limit_same_length_levenshtein = 3
    score_same_length_levenshtein = 300

    # substring same length
    limit_same_length_substring = 40 # phan tram
    score_same_length_substring = 2
    
    # levenshtein diff length
    limit_diff_length_levenshtein = 2
    score_diff_length_levenshtein = 50

    # substring diff length
    limit_diff_length_substring = 50 # phan tram
    score_diff_length_substring = score_same_length_substring * 0.8

    # subsequense
    limit_diff_length_subsequen = 40 # phan tram
    score_diff_length_subsequen = score_same_length_substring * 0.4
    # end

    hamming_dis = 0
    result = 0
    if len(text_1) == len(text_2):
        hamming_dis = rapidfuzz.string_metric.hamming(text_1, text_2)

        if hamming_dis <= limit_same_length_hamming:
            result = (limit_same_length_hamming + 1 - hamming_dis) * score_same_length_hamming

        elif levenshtein_dis <= limit_same_length_levenshtein:
            result = (limit_same_length_levenshtein + 1 - levenshtein_dis) * score_same_length_levenshtein

        elif common_substring_phan_tram >= limit_same_length_substring: 
            result = common_substring_phan_tram * score_same_length_substring
    else:
        
        if levenshtein_dis <= limit_diff_length_levenshtein:
            result = (limit_diff_length_levenshtein + 1 - levenshtein_dis) * score_diff_length_levenshtein
        
        elif common_substring_phan_tram >= limit_diff_length_substring:
            result = common_substring_phan_tram * score_diff_length_substring
        
        elif common_subsequen_phan_tram >= limit_diff_length_subsequen:
            result = common_subsequen_phan_tram * score_diff_length_subsequen
    
    return result

def string_is_number(string_number: str) -> bool:
    try:
        string_number = int(string_number)
        return True
    except ValueError:
        return False

def tach_lop(text: str) -> int:
    last_index = len(text) - 1
    b = text.find('lop')

    if last_index >= b+5:
        word_b4 = text[b+4]
        word_b5 = text[b+5]

        if string_is_number(word_b5) and string_is_number(word_b4):
            return int(word_b4+word_b5)
        elif string_is_number(word_b4):
            return int(word_b4)
        else:
            return None
    elif last_index == b+4:
        word_b4 = text[b+4]
        if string_is_number(word_b4):
            return int(word_b4)
        else:
            return None
    else:
        return None


def normal_search_room_text(text: str) -> str:
    text = replace_special_character(text)

    replace_what = [{'word_replace': 'mon ', 'with': ''}, 
                    {'word_replace': ' hoc', 'with': ''}]

    for item in replace_what:
        text = text.replace(item.get('word_replace'), item.get('with'))


    if 'lop' in text:
        number_lop = tach_lop(text)

        if number_lop:
            lop_from_kwargs = kwargs.get('lop')
            if lop_from_kwargs:
                lop_from_kwargs.append(number_lop)
                get_lop_query()
            else:
                kwargs['lop'] = [number_lop]
                get_lop_query()

            text = text.replace(' ' + str(number_lop), '', 1)

        b = text.find('lop')
        if b == 0:
            text = text.replace('lop', '', 1)
        else:
            text = text.replace(' lop', '', 1)

    return text


