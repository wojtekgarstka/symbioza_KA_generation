import pandas as pd

class OrderedAuthorsList:
    """
    A class holding list of authors, their references, and links of references
    """
    id = None
    ordered_tupled_list_of_authors = []  # list like (author_name, corresponding?, [list, of, affiliations])
    list_of_references = None
    affiliations_names=[]
    affiliations_nums=[]
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
dir='test files/abstracts-for-posters.csv'
df=pd.read_csv(dir) #to be put in function

participants=[]
for i in range(len(df)):
    participant=OrderedAuthorsList()
    authorslist=[]
    #generates list ofauthors with authors names for every presentation
    for a in range(5):
        author_num = str("Author " + str(a+1)) #Author 1, Author 2 etc.
        #if df[author_num][i]!=[]: #checks if file is not empty
        is_nan=df[author_num].notna()
        if is_nan[i]: #Checks if cell isn't empty
            author_name= df[author_num][i]
            authorslist.append(author_name)
        else:
            break
    participant.ordered_tupled_list_of_authors=authorslist
    '''affiliations unique'''
    affilist=[]
    affilist_nums=[]
    #generates list of unique affiliations with affi names for every presentation
    #generates list of 
    b=1
    for a in range(5):
        #affi index
        author_num = str("Author " + str(a+1)) #Author 1, Author 2 etc.
        affi_num = str("Affiliation " + str(a+1)) #Affi 1, Affi 2 etc.
        is_nan=df[author_num].notna()
        if is_nan[i]: #Checks if cell isn't empty
            
            affi_name= df[affi_num][i]
            if affi_name not in affilist:
                affilist.append(affi_name)
                affilist_nums.append(b)
                b+=1
            else:
                affilist_nums.append(affilist.index(affi_name)+1)

        else:
            break
    participant.affiliations_names=affilist 
    participant.affiliations_nums=affilist_nums 
    participants.append(participant)

def abstract_csv_reader(link_to_csv):
    pass


if __name__== '__main__':
    pass



#testing
for i in range(len(df)):
    for j in range(len(participants[i].ordered_tupled_list_of_authors)):
        print(str(participants[i].ordered_tupled_list_of_authors[j])+': '+str(participants[i].affiliations_nums[j]))
    for j in range(len(participants[i].affiliations_names)):
        print(str(j+1)+': '+str(participants[i].affiliations_names[j]))