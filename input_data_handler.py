import pandas as pd
from math import isnan
from pprint import pp, pprint
import os
import requests



class OrderedAuthorsList:
    """
    A class holding list of authors, their references, and links of references
    """
    ordered_tupled_list_of_authors = None
    # list like (author_name, [affiliations index],  corresponding_bool None or adress, presenting_bool)
    affiliations = None  # holds affiliations
    '''PROBLEM #1: Only option of 1 coresponding author(further corresponding authors to be added in the future)'''



    def __init__(self, df):
        #df[['Affiliation 1', 'Author 2', 'Affiliation 2', 'Author 3',
        #    'Affiliation 3', 'Author 4', 'Affiliation 4', 'Author 5',
        #    'Affiliation 5', 'More than 5 co-authors?',
        #    'Please provide the list of all authors',
        #    'Please provide the list of all authors\' afiliations',' Presenter',
        #    "Corresponding author", "Corresponding author's email"]]
        self.ordered_tupled_list_of_authors = []
        self.affiliations =[]
        for author in range(1,6):
            if nan_handler(df[f"Author {author}"]):
                if df[f"Affiliation {author}"] not in self.affiliations:
                    self.affiliations.append(df[f"Affiliation {author}"])
                corresponding = None
                if df[f"Author {author}"] == df[f"Corresponding author"]:
                    corresponding = df["Corresponding author's email"]
                presenting = False
                if df[f"Author {author}"] == df[f"Presenter"]:
                    presenting = True
                self.ordered_tupled_list_of_authors.append(
                    (df[f"Author {author}"],
                     self.affiliations.index(df[f"Affiliation {author}"]),
                    corresponding,
                    presenting)
                )
            if author == 5:
                if nan_handler(df['More than 5 co-authors?']):
                    self.ordered_tupled_list_of_authors.append(("MORE HAVE TO BE ADDED MANUALLY SORRY",
                                                                None, None, False))
    def get_authors_names(self):
        # ugly function
        author_number = 0
        string_to_insert = ""
        used_mails = 0
        mails_pointers = ["*", "#", "&"]
        for author in self.ordered_tupled_list_of_authors:
            #print(author)
            author_str = author[0]
            if author[3]: # if presenting we underscore
                author_str = "\\underline{"+author_str+"}"
            if author[2]: # if corresponding we add
                author_str += f"{mails_pointers[used_mails]}"
            # now appending affiliations
            #print("what",author[1] )
            if author[1] or author[1]==0: # if there is an affiliation, xdddd 0 is false i forgot
                #print(str(author[1] + 1))
                author_str += "$^{"+str(author[1]+1)+"}$"
            if ",$^{" in author_str: # makeshift so the corresponding would have superscript comma
                author_str = author_str.replace(',$^{','$^{,')
            string_to_insert = string_to_insert + author_str
            if author_number != len(self.ordered_tupled_list_of_authors)-1:
                string_to_insert = string_to_insert + ", "
                if author_number % 3 == 0 and author_number != 0:
                    string_to_insert = string_to_insert + "\\\\"
            author_number += 1
        #print(string_to_insert)
        return string_to_insert

    def get_affiliations(self):
        string_to_insert = ""
        for index, affiliation in enumerate(self.affiliations):
            if string_to_insert != "":
                string_to_insert += "\\\\"
            string_to_insert = f"$^{{{1}}}$ {affiliation}"
        return string_to_insert

    def get_corresponding_mails(self):
        used_mails = 0
        mails_pointers = ["*", "#", "&"]
        string_to_insert = ""
        for author in self.ordered_tupled_list_of_authors:
            _, _, corresponding, _ = author
            if corresponding:
                if string_to_insert != "":
                    string_to_insert += "~~~~"
                string_to_insert += f"{mails_pointers[used_mails]}\\href{{mailto:{corresponding}}}{{{corresponding}}}"
        return string_to_insert


def download_image(image_link, image_name):
    print(image_link)
    img_data = requests.get(image_link).content
    with open(f'downloaded/{image_name}.jpg', 'wb') as handler:
        handler.write(img_data)

class SymbiosisActiveParticipantInfo:
    """
    A class holding information of symbiosis participants which can recreate fully abstracts for posters
    """
    participant_name = None
    presentation_title = None
    participants_mail = None
    abstract = None
    image_link = None  # if not none, then fetch it and put into folder
    keywords = None

    authors_list_class = None

    def __init__(self, df):
        '''
        Takes a person and creates object for it

        this is so ugh
        TODO make this not dependent on format of csv as it is VERY unstable

        :param df: dataframe WITH CORRECT NAMES
        '''
        self.participants_mail = df["Email - same as in the registration form"]
        if nan_handler(df["Do you wish to include an image in your abstract?"]) in [True, "True", "Yes"]:
            # istfg get your forms columns right
            self.image_link = df["Upload image"]
            download_image(self.image_link, )
            self.abstract = df["Abstract.1"]
        else:
            self.abstract = df["Abstract"]
        self.abstract = self.abstract

        self.abstract_title = df['Abstract title']
        self.keywords = df["keywords"]

        # TODO prone to column name changes
        self.authors_list_class = OrderedAuthorsList(
            df[['Author 1', 'Affiliation 1', 'Author 2', 'Affiliation 2', 'Author 3',
                'Affiliation 3', 'Author 4', 'Affiliation 4', 'Author 5',
                'Affiliation 5', 'More than 5 co-authors?',
                'Please provide the list of all authors',
                'Please provide the list of all authors\' afiliations', 'Presenter',
                "Corresponding author", "Corresponding author's email"]])
        self.participant_name = df["Presenter"]

    def get_insert_dictionary(self):
        dict = {
            "INSERT-TITLE": self.abstract_title,
            "INSERT-AUTHORS-NAMES": self.authors_list_class.get_authors_names(),
            "INSERT-AFFILIATIONS": self.authors_list_class.get_affiliations(),
            "INSERT-CORRESPONDING-EMAILS": self.authors_list_class.get_corresponding_mails().replace('_','\_'),
            "INSERT-MAIN-TEXT": self.abstract.replace(". ", ".\n").replace("%", "\%"),
            "INSERT-KEYWORDS": self.keywords
        }
        return dict


def nan_handler(something):
    """
    Forces a variable into string or returns None if it is a nan (as pandas love transfering to it)
    :param something:
    :return:
    """
    if type(something) == float:  # nan is a float, everything else should be either str or something else
        if isnan(something):
            return None
        else:
            assert False, "error, somehow there is a float that isn't float"
    else:
        return str(something)


file_path = 'test files/abstracts-for-posters.csv'



# list of all participants
def df_reader(file_path):
    df = pd.read_csv(file_path)
    participants = []
    for index, row in df.iterrows():
        participant = SymbiosisActiveParticipantInfo(row)
        participants.append(participant)
    return participants



if __name__ == '__main__':
    # function working for sample dir
    participants = df_reader('test files/abstracts-for-posters.csv')
    # print(dir(participants))
    # testing no. 1 -> bardziej czytelne dla ludzi
    for i in range(0, 5):
        attrs = vars(participants[i])
        #print(', \n'.join("%s: %s" % item for item in attrs.items()))
        print("showing authors")
        attrs = vars(participants[i].authors_list_class)
        print(', \n'.join("%s: %s" % item for item in attrs.items()))



