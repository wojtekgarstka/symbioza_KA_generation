# importing files
import pandas as pd
import input_data_handler as idh
import template_inserter as ti

def generate_poster_abstracts_tex(plenary_speakers_csv):
    list_of_participants = idh.df_reader(plenary_speakers_csv)
    ti.generate_tex_file(("templates/header_poster.tex", "templates/body_poster.tex", None), list_of_participants,
                      {"INSERT-TYPE-OF-PRESENTATION": "P"}, name_of_output_file="poster_abstracts.tex")

def generate_oral_abstracts(oral_speakers_csv):
    list_of_participants = idh.df_reader(oral_speakers_csv)
    ti.generate_tex_file(("templates/header_oral.tex", "templates/body_oral.tex", None), list_of_participants,
                      {"INSERT-TYPE-OF-PRESENTATION": "O"}, name_of_output_file="oral_abstracts.tex")

def generate_plenary_lectures(oral_speakers_csv):
    list_of_participants = idh.df_reader(oral_speakers_csv)
    ti.generate_tex_file(("templates/header_plenary.tex", "templates/body_plenary.tex", None), list_of_participants,
                         {"INSERT-TYPE-OF-PRESENTATION": "PL"}, name_of_output_file="plenary_lectures.tex")

def generate_industry_abstracts(industry_csv):
    list_of_participants = idh.df_reader(industry_csv)
    ti.generate_tex_file(("templates/header_industry.tex", "templates/body_industry.tex", None), list_of_participants,
                         {"INSERT-TYPE-OF-PRESENTATION": "I"}, name_of_output_file="industry.tex")

if __name__=='__main__':
    generate_oral_abstracts("test files/abstracts-for-oral-presentat.csv")

