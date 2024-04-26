import input_data_handler as idh

def generate_tex_file(tuple_of_file_names=(None, None, None),
                      ordered_list_of_symbiosis_participants=None,
                      dict_of_keywords_inserts=None,
                      name_of_output_file="generated.tex"):
    header, body, tail = tuple_of_file_names
    with open(name_of_output_file, 'w') as tex_file:
        if header:
            with open(header) as header_f:
                tex_file.write(header_f.read())
        if body:  # this can be done better for sure
            with open(body) as body_f:
                participant_number = 1
                body_str = body_f.read()
                for participant in ordered_list_of_symbiosis_participants:
                    keyword_dict = participant.get_insert_dictionary()
                    keyword_dict.update(dict_of_keywords_inserts)
                    keyword_dict.update({"INSERT-NUMBER-OF-PRESENTATION": str(participant_number)})

                    page = body_str
                    for key in keyword_dict:
                        page = page.replace(key, keyword_dict[key])
                    tex_file.write(page)
                    participant_number += 1
        if tail:
            with open(tail) as tail:
                tex_file.write(header_f.read())
        tex_file.close()


if __name__ == "__main__":
    list = idh.df_reader('test files/abstracts-for-posters.csv')
    generate_tex_file(("templates/header_plenary.tex", "templates/body_plenary.tex", None), list,
                      {"INSERT-TYPE-OF-PRESENTATION": "P"}, name_of_output_file="test_poster_on_plenary.tex")
