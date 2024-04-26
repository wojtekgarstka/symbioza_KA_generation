# importing files
import pandas as pd
import input_data_handler as idh
import template_inserter as ti

def generate_poster_abstracts_tex(plenary_speakers_csv):
    list = idh.df_reader('test files/abstracts-for-posters.csv')
    ti.generate_tex_file(("templates/header_plenary.tex", "templates/body_plenary.tex", None), list,
                      {"INSERT-TYPE-OF-PRESENTATION": "P"}, name_of_output_file="test_poster_on_plenary.tex")

if __name__=='__main__':
    print("testing")

