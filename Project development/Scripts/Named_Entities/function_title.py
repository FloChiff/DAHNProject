import re

def title(text):
    """Apply tags to the regex

    :param text str: monography that has to be encoded
    :returns: monography encoded with the proper tags
    :rtype: str
    """

    #This series of statements contains regex of organizations from the corpus
    w0002 = re.compile(r"Atlantic Monthly( Review)?")
    w0003 = re.compile(r"Berliner Tageblatt")
    w0004 = re.compile(r"Figaro|FIGARO")
    w0005 = re.compile(r"Gazette de Zurich")
    w0006 = re.compile(r"J(ournal|OURNAL) (O|o)(fficiel|FFICIEL)")
    w0007 = re.compile(r"Journal de Genève")
    w0008 = re.compile(r"journal de l'Ouest")
    w0009 = re.compile(r"JOURNAL DES D(E|É)BATS|Journal des Débats")
    w0010 = re.compile(r"Journal Fléchois")
    w0011 = re.compile(r"Journal français d'Alsace-Lorraine")
    w0012 = re.compile(r"l'E(cho|CHO)")
    w0013 = re.compile(r"l'H(umanité|UMANITÉ)")
    w0014 = re.compile(r"l'Homme Enchaîné")
    w0015 = re.compile(r"l'I(llustration|LLUSTRATION)")
    w0016 = re.compile(r"Petit Journal")
    w0017 = re.compile(r"Revue de Paris")
    w0018 = re.compile(r"Revue des Deux-Mondes")
    w0019 = re.compile(r"Revue du 14 Juillet")
    w0020 = re.compile(r"Revue hebdomadaire")
    w0021 = re.compile(r"REVUE INTERNATIONALE")

    #This series of statements contains the encoding for the organizations from the corpus
    text = re.sub(w0002, r'<title ref="#w0002" type="pec">\g<0></title>', text)
    text = re.sub(w0003, r'<title ref="#w0003" type="pec">\g<0></title>', text)
    text = re.sub(w0004, r'<title ref="#w0004" type="pec">\g<0></title>', text)
    text = re.sub(w0005, r'<title ref="#w0005" type="pec">\g<0></title>', text)
    text = re.sub(w0006, r'<title ref="#w0006" type="pec">\g<0></title>', text)
    text = re.sub(w0007, r'<title ref="#w0007" type="pec">\g<0></title>', text)
    text = re.sub(w0008, r'<title ref="#w0008" type="pec">\g<0></title>', text)
    text = re.sub(w0009, r'<title ref="#w0009" type="pec">\g<0></title>', text)
    text = re.sub(w0010, r'<title ref="#w0010" type="pec">\g<0></title>', text)
    text = re.sub(w0011, r'<title ref="#w0011" type="pec">\g<0></title>', text)
    text = re.sub(w0012, r'<title ref="#w0012" type="pec">\g<0></title>', text)
    text = re.sub(w0013, r'<title ref="#w0013" type="pec">\g<0></title>', text)
    text = re.sub(w0014, r'<title ref="#w0014" type="pec">\g<0></title>', text)
    text = re.sub(w0015, r'<title ref="#w0015" type="pec">\g<0></title>', text)
    text = re.sub(w0016, r'<title ref="#w0016" type="pec">\g<0></title>', text)
    text = re.sub(w0017, r'<title ref="#w0017" type="pec">\g<0></title>', text)
    text = re.sub(w0018, r'<title ref="#w0018" type="pec">\g<0></title>', text)
    text = re.sub(w0019, r'<title ref="#w0019" type="pec">\g<0></title>', text)
    text = re.sub(w0020, r'<title ref="#w0020" type="pec">\g<0></title>', text)
    text = re.sub(w0021, r'<title ref="#w0021" type="pec">\g<0></title>', text) 
    return text