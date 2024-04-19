import pandas as pd

class OrderedAuthorsList:
    """
    A class holding list of authors, their references, and links of references
    """
    id = None
    abstract_title = None #hold abstract title
    abstract_content = None #holds abstract content, if abstract content==None reports error
    '''PROBLEM #0: There are to abstract columns, I'd suggest concatenating them'''
    ordered_tupled_list_of_authors = []  # list like (author_name, corresponding?, [list, of, affiliations])
    list_of_references = None
    affiliations_names = [] #holds affiliations with underlined presenter and * added to the first corresponding author 
    '''PROBLEM #1: Only option of 1 coresponding author(further corresponding authors to be added in the future)'''
    affiliations_nums = [] #holds numbers for affiliations
    corresponding_mails = [] #holds corresponding mail assinged to a exact person with that mail, not really useful
    '''PROBLEM #2: problem 1 continuation, no way of adding second author's email'''
    image_link = [] #holds link for image
    keywords = None #holds keywords
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

    def __init__(self, infodump):
        pass
dir='test files/abstracts-for-posters.csv'
df=pd.read_csv(dir) #to be put in function

#list of all participants
participants=[]
for i in range(len(df)):
    participant=OrderedAuthorsList()
    '''Abstract title'''
    participant.abstract_title=str(df['Abstract title'][i])
    '''Abstract content'''
    if df['Abstract'].notna()[i]:
        participant.abstract_content=str(df['Abstract'][i])
    else:
        participant.abstract_content="Warning!!!!! EMPTY"
    '''image link'''
    if df['Upload image'].notna()[i]:
        participant.image_link=str(df['Upload image'][i])
    else:
        participant.image_link = None
    '''Abstract keywords'''
    participant.keywords = str(df['keywords'][i])
    '''List of authors'''
    authorslist=[]
    corresponding_sings = ['*',str("#"), str('$')] 
    print(corresponding_sings)
    #generates list of authors with authors names for every presentation
    corresp_counter=0
    for a in range(5):
        author_num = str("Author " + str(a+1)) #Author 1, Author 2 etc.
        #if df[author_num][i]!=[]: #checks if file is not empty
        is_nan=df[author_num].notna()
        if is_nan[i]: #Checks if cell isn't empty
            author_name= df[author_num][i]
            author_name1=author_name
            if author_name1==df["Presenter"][i]:
                author_name = "\\underline{"+str(author_name)+"}" #adds underline in LaTeX
            if author_name1==df["Corresponding author"][i]: #adds first corresponding author
                if corresp_counter==0:
                    author_name=author_name+"*"
            authorslist.append(author_name)
            

        else:
            break
    # TO BE CHANGED: here shall we put additional authors and affiliations (if there are more than 5)
    participant.ordered_tupled_list_of_authors=authorslist
    '''gives corresponding mails were listed'''
    maillist = []
    b=0
    for a in range(5):
        author_num = str("Author " + str(a+1)) #Author 1, Author 2 etc.
        #if df[author_num][i]!=[]: #checks if file is not empty
        is_nan=df[author_num].notna()
        if is_nan[i]: #Checks if cell isn't empty
            author_name= df[author_num][i]
            author_name1=author_name
            if author_name1==df['Corresponding author'][i]:
                mail = df['Corresponding author\'s email'][i] #adds underline in LaTeX
                b=1
            else:
                mail = None
            maillist.append(mail)
    if b==1:
        participant.corresponding_mails=maillist
    else:
        participant.corresponding_mails=df['Corresponding author\'s email'][i]

    '''List of unique affiliations + list of numbers corresponding to affilations'''
    affilist=[] #list of affiliations
    affilist_nums=[] # list of numbers corresponding to affilations
    
    b=1 # b as a counter for affiliations used
    for a in range(5):
        #affi index
        author_num = str("Author " + str(a+1)) #Author 1, Author 2 etc.
        affi_num = str("Affiliation " + str(a+1)) #Affi 1, Affi 2 etc.
        is_nan=df[author_num].notna() #it is counted by author_num, because there are names without affis, but there aren't affis without names
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


    #adds participant to list of participants
    participants.append(participant)

def abstract_csv_reader(link_to_csv):
    pass


if __name__== '__main__':
    pass

#testing no. 1 -> bardziej czytelne dla ludzi
for i in range(len(df)):
    print(str(participants[i].abstract_title))
    for j in range(len(participants[i].ordered_tupled_list_of_authors)):
        print(str(participants[i].ordered_tupled_list_of_authors[j])+': '+str(participants[i].affiliations_nums[j]))
    for j in range(len(participants[i].affiliations_names)):
        print(str(j+1)+': '+str(participants[i].affiliations_names[j]))
    for j in range(len(participants[i].corresponding_mails)):
        if participants[i].corresponding_mails[j]!=None:
            print(str(participants[i].corresponding_mails[j]))
        else:
            None
    print('')
    print(participants[i].abstract_content)
    print('')

#testing no. 2 -> próba generacji LaTeX
for i in range(len(df)):
    print("")
    print("\\newpage \hypertarget"+"{oral:"+"{a}".format(a=str(i+1))+"}{"+"}" )
    print("\OralTitle{O-"+"{a}): ".format(a=str(i+1))+str(participants[i].abstract_title)+"}")
    print('')
    print("\AbstractAuthors{",end='')
    for j in range(len(participants[i].ordered_tupled_list_of_authors)-1):
        print(str(participants[i].ordered_tupled_list_of_authors[j])+'$^{'+str(participants[i].affiliations_nums[j])+'}$',end=', ')
    print(str(participants[i].ordered_tupled_list_of_authors[len(participants[i].ordered_tupled_list_of_authors)-1])+'$^{'+str(participants[i].affiliations_nums[len(participants[i].ordered_tupled_list_of_authors)-1])+'}$'+"}")
    print("\Affiliation{",end='')
    for j in range(len(participants[i].affiliations_names)-1):
        print('$^{'+str(participants[i].affiliations_nums[j])+'}$'+str(participants[i].affiliations_names[j]),end=', ')
    print('$^{'+str(participants[i].affiliations_nums[len(participants[i].affiliations_names)-1])+'}$'+str(participants[i].affiliations_names[len(participants[i].affiliations_names)-1])+"}")
    print('')
    print("\Email{*\href{mailto:",end='')
    for j in range(len(participants[i].corresponding_mails)):
        if participants[i].corresponding_mails[j]!=None:
            print(str(participants[i].corresponding_mails[j])+"}{"+str(participants[i].corresponding_mails[j]),end='')
        else:
            None
    print("}"+"}")
    print('')
    print(participants[i].abstract_content)
    print('')
    if participants[i].image_link!=None:
        print("link to img: " + str(participants[i].image_link))
    print('\Keywords{\\textbf{Keywords:} '+str(participants[i].keywords))
