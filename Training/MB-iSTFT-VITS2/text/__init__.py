from kinya import sequence_to_text, text_to_sequence

_symbol_to_id = kinya._symbol_to_id
_id_to_symbol = kinya._id_to_symbol

def clean_text(text):
    return sequence_to_text(text_to_sequence(text))

def _clean_text(text, cleaner_names):
    return clean_text(text)
