from text import norm_text, sequence_to_text, text_to_sequence

if __name__ == "__main__":
    txt = "yatangiye uruzinduko rw’iminsi itatu mu Rwanda, kuri uyu wa 25 Mutarama 2024, rwaturutse ku butumire yahawe na mugenzi we"
    print(norm_text(txt))
    print(sequence_to_text(text_to_sequence(norm_text(txt))))
