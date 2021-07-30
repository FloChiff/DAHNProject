# -*- UTF-8 -*-

"""
- author: Floriane Chiffoleau
- date: June 2020
- description: Creating XML files from a CSV and encoding some metadata
- input: CSV file
- output: XML files
- usage :
    ======
    python name_of_this_script.py arg1 arg2

    arg1: csv of the metadata
    arg2: folder for the XML files created

"""

import csv
import sys
import os
from bs4 import BeautifulSoup

with open(sys.argv[1], 'r', encoding='UTF-8') as csvfile:
    print("reading from " + sys.argv[1])
    index = csv.DictReader(csvfile, delimiter=';')
    for root, dirs, files in os.walk(sys.argv[2]):
        for filename in root: #files?
            for row in index:
                header = list(row.keys())
                number = row[header[0]]
                date = row[header[1]]
                french = row[header[2]]
                english = row[header[3]]
                fulldate = row[header[4]]
                pages = row[header[5]]
                before_number = row[header[6]]
                before_date = row[header[7]]
                after_number = row[header[8]]
                after_date = row[header[9]]
                filename = f"""Lettre{number}_{fulldate}.xml"""
                tree = f""" <?xml-model href="../Guidelines/out/Documentation-Correspondance.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
                <TEI xmlns="http://www.tei-c.org/ns/1.0">
                    <teiHeader>
                        <fileDesc>
                            <titleStmt>
                                <title xml:lang="en">Letter number {number} from Paul d'Estournelles de Constant to Nicholas Murray Butler ({english})</title>
                                <title xml:lang="fr">Lettre n°{number} de Paul d'Estournelles de Constant à Nicholas Murray Butler ({french})</title>
                                <funder>Ministry of Higher Education, Research and Innovation</funder>
                                <principal>
                                    <persName ref="#anne.baillot">
                                        <forename>Anne</forename>
                                        <surname>Baillot</surname>
                                    </persName>
                                    <affiliation>
                                        <orgName ref="#mans.uni">Le Mans Université</orgName>
                                        <address>
                                            <street>Avenue Olivier Messiaen</street>
                                            <postCode>72085</postCode>
                                            <settlement>Le Mans</settlement>
                                            <country key="FR">France</country>
                                        </address>
                                    </affiliation>
                                </principal>
                                <respStmt>
                                    <resp>Edited by</resp>
                                    <persName ref="#anne.baillot">
                                        <forename>Anne</forename>
                                        <surname>Baillot</surname>
                                    </persName>
                                </respStmt>
                                <respStmt>
                                    <resp>Edited by</resp>
                                    <persName ref="#stephane.tison">
                                        <forename>Stéphane</forename>
                                        <surname>Tison</surname>
                                    </persName>
                                </respStmt>
                                <respStmt>
                                    <resp>Transcription by</resp>
                                    <persName ref="#floriane.chiffoleau">
                                        <forename>Floriane</forename>
                                        <surname>Chiffoleau</surname>
                                    </persName>
                                </respStmt>
                                <respStmt>
                                    <resp>Encoding by</resp>
                                    <persName ref="#floriane.chiffoleau">
                                        <forename>Floriane</forename>
                                        <surname>Chiffoleau</surname>
                                    </persName>
                                </respStmt>
                                <respStmt>
                                    <resp>Digitization by</resp>
                                    <orgName ref="#ADSarthe">Archives départementales de la Sarthe</orgName>
                                </respStmt>
                            </titleStmt>
                            <publicationStmt>
                                <authority>Le Mans Université</authority>
                                <availability>
                                    <licence target="https://creativecommons.org/licenses/by/3.0/deed.en">Attribution 3.0 Unported (CC BY 3.0) </licence>
                                </availability>
                                <date when-iso="2020"/>
                            </publicationStmt>
                            <seriesStmt>
                                <title type="main">Correspondence of Paul d'Estournelles de Constant</title>
                                <title type="genre">Letters</title>
                                <title type="topic"> </title>
                                <title type="topic"> </title>
                            </seriesStmt>
                            <sourceDesc>
                                <msDesc>
                                    <msIdentifier>
                                        <location>
                                            <address>
                                                <street>9 rue Christian Pineau</street>
                                                <postCode>72100</postCode>
                                                <settlement>Le Mans</settlement>
                                                <region>Pays de la Loire</region>
                                                <country key="FR">France</country>
                                            </address>
                                        </location>
                                        <institution ref="#ADSarthe">Archives départementales de la Sarthe</institution>
                                        <repository>Fonds des archives privées</repository>
                                        <collection>Fonds d'Estournelles de Constant</collection>
                                        <idno>12 J</idno>
                                    </msIdentifier>
                                    <msContents>
                                        <msItem>
                                            <docDate when="{date}"/>
                                            <note resp="#floriane.chiffoleau"> </note>
                                            <note type="keyword" resp="#floriane.chiffoleau"> </note>
                                        </msItem>
                                    </msContents>
                                    <physDesc>
                                        <objectDesc>
                                            <supportDesc>
                                                <support>
                                                    <material/>
                                                </support>
                                                <extent>
                                                    <measure type="folio" xml:lang="fr">{pages} feuillets de textes +  feuillets d'annexes</measure>
                                                    <measure type="folio" xml:lang="en">{pages} text folio +  annex folio</measure>
                                                    <dimensions unit="cm">
                                                        <height/>
                                                        <width/>
                                                    </dimensions>
                                                </extent>
                                                <foliation>
                                                    <p xml:lang="fr">La numérotation des pages a été faite à la machine à écrire, comme le reste de la lettre</p>
                                                    <p xml:lang="en">The numerotation has been made with a typewriter, just like the rest of the letter</p>
                                                </foliation>
                                                <condition>
                                                    <p xml:lang="fr">La lettre est bien conservée</p>
                                                    <p xml:lang="en">The letter is well preserved</p>
                                                </condition>
                                            </supportDesc>
                                            <layoutDesc>
                                                <layout xml:id="lh-senat">
                                                    <p xml:lang="fr">Un en-tête, où est écrit "Sénat" en majuscule et souligné, est imprimé en haut à gauche de la
                                                        première feuille de la lettre.</p>
                                                    <p xml:lang="en">A letterhead, where an underlined uppercased "Sénat" is written, is printed on the top left of
                                                        the first folio of the letter.</p>
                                                </layout>
                                            </layoutDesc>
                                        </objectDesc>
                                        <handDesc>
                                            <handNote xml:id="major_hand" medium="black_ink" scope="minor" scribe="author" scribeRef="#p0001">
                                                <p xml:lang="fr">Main de l'auteur, Paul d'Estournelles de Constant, qui écrit à l'encre noir à la machine à
                                                    écrire</p>
                                                <p xml:lang="en">Hand of the author, Paul d'Estournelles de Constant, who write in black ink with a
                                                    typewriter.</p>
                                            </handNote>
                                            <handNote xml:id="annotation" medium="pencil" scope="minor" scribe="author" scribeRef="#p0001">
                                                <p xml:lang="fr">Main de l'auteur Paul d'Estournelles de Constant, qui annote son texte et signe son nom de sa main
                                                    à la fin</p>
                                                <p xml:lang="en">Hand of the author, Paul d'Estournelles de Constant, who annotate his text and hand sign it at the
                                                    end.</p>
                                            </handNote>
                                            <handNote xml:id="stamp" medium="black_ink" scope="minor" scribe="archivist" scribeRef="#ADSarthe">
                                                <p xml:lang="fr">Main de l'archiviste qui a collecté les lettres et qui a apposé un tampon sur chacune des feuilles
                                                    du dossier.</p>
                                                <p xml:lang="en">Hand of the archivist who collected the letters and applied a stamp on each folio.</p>
                                            </handNote>
                                        </handDesc>
                                        <additions>
                                            <p xml:lang="fr">L'institution qui conserve ce fond a apposé sur toutes les feuilles de textes, généralement dans la
                                                marge, un tampon où il est inscrit : <stamp resp="#stamp">Archives de la Sarthe <lb/>Propriété publique</stamp></p>
                                            <p xml:lang="en">The institution that held the collection applied on each folio, usually in the margin, a stamp where it
                                                is written: <stamp resp="#stamp">Archives de la Sarthe <lb/>Propriété publique</stamp></p>
                                        </additions>
                                        <!-- <accMat>
                                            <p xml:lang="fr">La lettre est accompagnée de ... </p>
                                            <p xml:lang="en">The letter also contains .. </p>
                                        </accMat> -->
                                    </physDesc>
                                    <history>
                                        <origin>
                                            <p xml:lang="fr">La lettre a été écrite à <origPlace>...</origPlace> le <origDate when-iso="{date}">{french}</origDate></p>
                                            <p xml:lang="en">The letter has been written in <origPlace>...</origPlace> on <origDate when-iso="{date}">{english}</origDate></p>
                                        </origin>
                                        <acquisition>
                                            <p xml:lang="fr">Les papiers de Paul d'Estournelles ont été versés aux Archives départementales de la Sarthe en <date
                                                when="1957">1957</date> par sa fille <persName>Mme Albert Le Guillard</persName>.</p>
                                            <p xml:lang="en">Paul d'Estournelles papers have been placed at the Departmental Archives of Sarthe in <date when="1957"
                                                >1957</date> by his daughter, <persName>Mrs Albert le Guillard</persName>.</p>
                                        </acquisition>
                                    </history>
                                    <additional>
                                        <listBibl>
                                            <bibl xml:lang="fr">De multiples extraits de la correspondance se retrouvent dans <persName>AKHUND Nadine</persName>, <persName>TISON
                                                Stéphane</persName>, <title>En guerre pour la paix, 1914-1919. Correspondance Paul d'Estournelles de Constant et
                                                    Nicholas Murray-Butler</title>.</bibl>
                                            <bibl xml:lang="en">Many correspondence excerpt are found in <persName>AKHUND Nadine</persName>, <persName>TISON
                                                Stéphane</persName>, <title>En guerre pour la paix, 1914-1919. Correspondance Paul d'Estournelles de Constant et
                                                    Nicholas Murray-Butler</title>.</bibl>
                                           </listBibl>
                                    </additional>
                                </msDesc>
                            </sourceDesc>
                        </fileDesc>
                        <encodingDesc>
                            <projectDesc>
                                <p xml:lang="fr">L'encodage de ce document s'est fait dans le cadre du projet DAHN d'"Éditions numérique de manuscrits historiques
                                    (correspondances)"</p>
                                <p xml:lang="en">The encoding of this document is part of the DAHN Project "Digital Editions of historical manuscripts
                                    (correspondences)"</p>
                            </projectDesc>
                            <editorialDecl>
                                <correction>
                                    <p xml:lang="fr">Aucune correction</p>
                                    <p xml:lang="en">No correction</p>
                                </correction>
                                <hyphenation eol="all" rend="sh">
                                    <p xml:lang="fr">Toutes les coupures de mots pour fin de ligne (indiquées principalement avec un tiret simple) ont été conservées.</p>
                                    <p xml:lang="en">All the end-of-line hyphenation (made with a single hyphen) have been kept</p>
                                </hyphenation>
                            </editorialDecl>
                        </encodingDesc>
                        <profileDesc>
                            <correspDesc>
                                <correspAction type="sent">
                                    <persName ref="https://viaf.org/viaf/15798950/">Paul d'Estournelles de Constant</persName>
                                    <placeName ref="https://www.geonames.org/"> </placeName>
                                    <date when-iso="{date}"/>
                                </correspAction>
                                <correspAction type="received">
                                    <persName ref="https://viaf.org/viaf/17333392/">Nicholas Murray Butler</persName>
                                    <placeName ref="https://www.geonames.org/5128581">New-York</placeName>
                                </correspAction>
                                <correspContext>
                                    <ref type="prev" target="Lettre{before_number}_{before_date}.xml"/>
                                    <ref type="next" target="Lettre{after_number}_{after_date}.xml"/>
                                </correspContext>
                            </correspDesc>
                            <langUsage>
                                <language ident="fr"/>
                            </langUsage>
                        </profileDesc>
                        <revisionDesc status="raw_transcription">
                            <change when-iso="2021-05-19" who="#floriane.chiffoleau">Creation of the file</change>
                        </revisionDesc>
                    </teiHeader>
                    <text>
                        <body>
                            <div type="transcription">
                                <pb n="" facs=".JPG"/>
                            </div>
                        </body>
                    </text>
                </TEI>
                """
                soup = BeautifulSoup(tree, 'xml')
                with open(sys.argv[2] + filename, 'w', encoding='utf8') as xml_file:
                    xml_file.write(str(soup))
                    print("creating " + filename)