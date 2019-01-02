from work_with_db import *


def process_data(data_to_process):
    """Split all files contents and then combine unique words into resulting file.
    """
    # result = set()
    #
    # for _, contents in data_to_process.items():
    #     if isinstance(contents, bytes):
    #         text = contents.decode('utf-8')
    #     else:
    #         text = contents
    #     result |= set(text.split())
    #
    # if result:
    #     yield None, '\n'.join(sorted(list(result)))
    for key in data_to_process.keys():
        if key[-3:] == 'txt':
            write_to_db_metas(data_to_process)
        elif key[-5:] == 'conll':
            write_to_db_words(data_to_process)
        elif key[-4:] == 'xlsx':
            write_to_db_collocations(data_to_process)
        else:
            raise Exception("Wrong filename: {0}".format(key))

def search_data(data_to_search):
    return search_in_db(data_to_search)
