import requests

def loai_bo_trung_lap(lst):
    lst_moi = []
    for item in lst:
        if item not in lst_moi:
            lst_moi.append(item)
    return lst_moi


def cleanup_meaning(meaning):
    # Loại bỏ phần trong dấu ngoặc
    cleaned_meaning = meaning.split('(')[0].strip()
    # Nếu có dấu phẩy, chỉ lấy phần trước dấu phẩy
    if ',' in cleaned_meaning:
        cleaned_meaning = cleaned_meaning.split(',')[0].strip()
    return cleaned_meaning


def lookup_word_jisho(word):
    url = f"https://jisho.org/api/v1/search/words?keyword={word}"

    try:
        response = requests.get(url)
        data = response.json()

        if "data" in data and data["data"]:
            meanings = []
            for entry in data["data"]:
                english_meanings = [cleanup_meaning(sense["english_definitions"][0]) for sense in entry["senses"]]
                meanings.extend(english_meanings)

            meanings = list(map(lambda x: x.lower(), meanings))

            for i in meanings:
                if len(i) > 17 or len(i) == 0:
                    meanings.remove(i)

            # meanings = loai_bo_trung_lap(meanings)

            return meanings
        else:
            return None

    except Exception as e:
        print("Error:", e)
        return None


# input_file = 'kata_word.txt'
# output_file = 'kata_word_translated.txt'
#
# wordlist = []
# with open(input_file, 'r') as file:
#     words = file.readlines()
#     for word in words:
#         word = word.strip()
#         wordlist.append(word)
#
# with open(output_file, 'w') as file:
#     for word in wordlist:
#         meanings = lookup_word_jisho(word)
#         if meanings:
#             meanings_str = ', '.join(meanings)
#             file.write(meanings_str)
#             file.write('\n')
#         else:
#             file.write('\n')

word = input("Nhập từ tiếng Nhật: ")
meanings_list = lookup_word_jisho(word)
if meanings_list:
    print("Nghĩa tiếng Anh:")
    print(meanings_list)
else:
    print("Không tìm thấy từ.")

