import pandas as pd

class OrderedAuthorsList:
    """
    A class holding list of authors, their references, and links of references
    """
    ordered_tupled_list_of_authors = None  # list like (author_name, corresponding?, [list, of, affiliations])
    list_of_references = None
    corresponding_mails = None
    def __init__(self):
        pass

class SymbiosisActiveParticipantInfo:
    """
    A class holding information of symbiosis participants which can recreate fully abstracts for posters
    """
    name_of_participant = None
    presentation_title = None
    authors_list_class = None
    participants_mail = None
    abstract_main_part = None
    image_link = None  # if not none, then fetch it and put into folder
    keywords = None

    def __init__(self, infodump):
        pass

def abstract_csv_reader(link_to_csv):
    pass


if __name__== '__main__':
    pass