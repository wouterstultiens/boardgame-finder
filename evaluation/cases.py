# tests/cases.py
from dataclasses import dataclass
from typing import List, Dict, Optional, Union

@dataclass(frozen=True)
class BGGMatch():
    id: Optional[str]
    title: Optional[str]
    lang: Optional[str]
    exact_match: bool

@dataclass(frozen=True)
class PromptTestCase:
    name: str
    title: str
    description: str
    image_texts: List[str]
    expected_extraction: List[Dict[str, str]]
    expected_matches: List[Dict[str, Union[List[str], str, bool]]]

TEST_CASES: List[PromptTestCase] = [
    PromptTestCase(
        name="nl_party_co_multiple",
        title="Party & Co + 1000 extra vragen",
        description="Niet veel gebruikt",
        image_texts=[
            "TM\nPARTY\nCO\nDiset\nOMDAT EEN SPEL MET VRIENDEN ALTIJD EEN FEEST IS\nTM\nPARTY\n& CO\n1000\nNIEUWE VRAGEN\nDiset\nAANVULLINGSSET MET 200 NIEUWE KAARTEN"
        ],
        expected_extraction=[
            {"llm_name": "Party & Co", "llm_lang": "nl"},
            {"llm_name": "Party & Co: 1000 Nieuwe Vragen", "llm_lang": "nl"}
        ],
        expected_matches=[
            {"id": "13972", "name": "Party & Co", "lang": "en", "exact_match": True}, 
            {"id": "31395", "name": "Party & Co: Expansion", "lang": "en", "exact_match": True}
        ]
    ),
    PromptTestCase(
        name="en_bandida",
        title="Bandida Kaartspel",
        description="Leuk kaartspel Bandida, in zo goed als nieuwe staat. Geschikt voor 1-4 spelers. Probeer samen te voorkomen dat Bandida ontsnapt! Een spannend en snel spel voor het hele gezin.",
        image_texts=[
            "BANDIDA\nWANTED⭑",
            "6-99\n1-4\n15'\nCoop\nGame Author: Martin Nedergaard Andersen\nGraphics & Illustration: Odile Sageat\nEN Bandida is trying to escape AGAIN. Team\nup to either stop her or help her escape!\nES Bandida está tratando de escapar\notra vez. ¡Únete al equipo para\ndetenerla o para ayudarla a evadirse!\nFR Bandida tente ENCORE de s'évader.\nUnissez vos forces pour l'arrêter\nou pour l'aider à s'échapper!\nDE Bandida versucht SCHON WIEDER\nauszubrechen. Haltet sie gemeinsam\nauf oder helft ihr zu fliehen!\n-\nIT Bandida sta DI NUOVO tentando\ndi evadere. Unite le forze per\nfermarla o per aiutarla a fuggire!\nNL Bandida probeert OPNIEUW te ontsnap-\npen. Werk samen om haar te stoppen\nof help haar samen ontsnappen!\n70 Cards\n1 Super card\nVideo rules\nwww.helvetiq.com"
        ],
        expected_extraction=[{"llm_name": "Bandida", "llm_lang": "en"}],
        expected_matches=[{"id": ["299571"], "name": "Bandida", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="nl_oud_en_nieuw_spel",
        title="Het Oud & Nieuw Spel - Dilemma's, Vragen, Uitbeelden",
        description="Leuk spel voor Oud & Nieuw! Bevat 20 dilemma's, 20 vragen en 20 uitbeeldingen. Perfect om de avond mee te vullen met vrienden en familie.",
        image_texts=[
            "HET OUD\n& NIEUW\nSPEL\n20X DILEMMA'S\n20X VRAGEN\n20X UITBEELDEN\nJEUX POUR SAINT SYLVESTRE\n20X DILEMMES, 20X QUESTIONS,\n20X MIMES"
        ],
        expected_extraction=[{"llm_name": "Het Oud & Nieuw Spel", "llm_lang": "nl"}],
        expected_matches=[{"id": [""], "name": "", "lang": "", "exact_match": False}] # Not on expected_matches
    ),
    PromptTestCase(
        name="en_ticket_to_ride_europa",
        title="Ticket to Ride: Europa 1912",
        description="Ticket to Ride: Europa 1912 uitbreiding.  Voeg nieuwe varianten en routes toe aan je Ticket to Ride Europa spel.  Geschikt voor meerdere spelers. In goede staat.",
        image_texts=[
            "EUROPA 2\n1912\n4.183\nExpansion\nExtension\nA\nLisäosa\nZUG UM ZUG\nTICKET TO RIDE\nLES AVENTURIERS DU RAIL\nExpansion\nAVENTUREROS AL TREN!\nMENOLIPPU\nDAYS OF\nWONDER\nEUROPA",
            "EUROPA\n1912\nhe fumpu 1912 expamion brings new Warehouses and\nDepots to the exploration of your favorite European\ncities and introduces a whole n t of Destination Tickets!\nContains 5 Players Washouses, 25 in Depots,\n11 Destra\nTicket to Ride Europe with 5 new\nThis dut\nTickets t\nfor the Ticket to Ride family of board, A\nto play with the new Waries & Depois rule the new fickets induded are for\nuse only with it so ide up\nvec Europo 1912, apprener à utiliser les Entrepits et Depots dismisse\nplateau de jeu pour acquérir de nouvelles cartes et remporter la victoire\nDe nouvelles cartes Destination vous attendent également dans cette extension\nContents 25 been 101 cartes destination per even dead wige (\nCe produit est une EXTENSION s jeux de la série Les Aventuriery du at est poble de j\nfees riges des Entrepits et épôts aves tout explaire de la série. La nasc\nDestination set tables qu'avec Les Aventales d\nErweiterung Faropa 1912 bringt orue lagerhallen, Depots and Zielkarten ins Spiel\nSo steht der Erkandung Ihrer europaischen Lieblingsstädte nichts mehrt West\nDieses Spiel ist eine\nund Depots\nfor die Spiele der leg um fag\nspielen. Die in dieser trweiterung enthaltenes new\nke und k\nkaren sind hie\nAlso includes rules in\n\"\n24968\n11771\nLFCACA149\nMade\nin Germany\nCE\nDAYS OF\nWONDER"
        ],
        expected_extraction=[{"llm_name": "Ticket to Ride: Europa 1912", "llm_lang": "en"}],
        expected_matches=[{"id": ["53383"], "name": "Ticket to Ride: Europa 1912", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="nl_ticket_to_ride_london",
        title="Ticket to Ride: London - Bordspel",
        description="Ticket to Ride: London is een snelle en toegankelijke versie van het populaire Ticket to Ride bordspel. Spelers verzamelen transportkaarten en claimen routes op een kaart van Londen. Probeer de meeste routes te voltooien en de meeste punten te scoren! Geschikt voor 2-4 spelers. In goede staat.",
        image_texts=[
            "Alan Pe Morn\nTICKET TO RIDE\nLONDON\nPEACE\n153\nTRAFALGA\nDOW N1\nDAYS OF\nWONDER",
            "81\nCROSS\nHE CHARTERHOUSE\nLONDON\nTICKET TO RIDE\nLONDON\nAlan To Your\n61\n03\n122024\n22\nTOZE IN\nST PAUL'S\nTOWER OF\nBRICK\nLANE\n29\n002\n28\n26\nRICKE\nDAYS OF\nWONDER",
            "This is\nTICKET TO RIDE London calling!\nWelkom in de\njaren 70! Ontdek de\nmode- en muziekhoofdstad\nvan de wereld door aan boord\nte springen van de beroemde\ndubbeldekker bus, die een bezoek\nbrengt aan historische locaties\nzoals Buckingham Palace, het\nBritish Museum en de Big Ben\nIn dit snelle Ticket to Ride\" spel\nracen de spelers tegen elkaar in de\nhoofdstad van het Verenigd Koninkrijk\nom de belangrijkste buslijnen te\nclaimen, districten te voltooien en om\nhun bestemmingskaarten te behalen.\nTicket to Ride\" is zowel leuk voor\nbeginnende als gevorderde spelers\ndankzij het eenvoudige spelverloop.\nLONDON\nBar Me\nPatar Cas\nCOVENT GARDEY\nICKE\nLONDO\nPARK\n45\n40\nLONDON\nINHOUD\n1 spelbard van het transport-\nartwerk van Londen\n68 plastic busse\n(17 van elke kleur)\n+44 tramportkaarten\n20 bestemmingskaartes\ncarepiannen\n+1 spelhandleiding\nLeer het spel in slechts 3 minuten\nen je zult het nog uren spelen!\nwww.daysofwonder.com/\n720561\nwww.ticket2ridegame.com\nDays of Wonder Earpe: Days of Wander\n10 County Road W\n2-4\n8+\n10-15 8\n24968 20561\nMot\n1-2 USA\nMade in Germany E\nDAYS OF\nWONDER"
        ],
        expected_extraction=[{"llm_name": "Ticket to Ride: London", "llm_lang": "nl"}],
        expected_matches=[{"id": ["276894"], "name": "Ticket to Ride: London", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="en_ticket_to_ride_india_switzerland",
        title="Ticket to Ride: India + Zwitserland",
        description="Ticket to Ride: India en Zwitserland uitbreiding. Reis door India en Zwitserland in dit spannende bordspel. Geschikt voor meerdere spelers.",
        image_texts=[
            "Alan R. Moon\nTICKET TO RIDE\nINDIA\nBy Jan Vincent\nExtension\nZUG ZUG\nTICKET TO RIDE\nLES AVENTURIERS RAIL\n¡AVENTUREROS TREN!,\nMENOLIPPU\nDAYS OF\nWONDER\nराजहंस\n611\nAlan R. Moon\n+SWITZERLAND\n644",
            "Al R. Men\nAlan R. Mon\nTICKET TO RIDE\n+ SWITZERLAND\nET TO RIDE\nINDIA\nDAYS OF\nWONDER\nMARZALA\nMADRAS\nERODE\nDAYS OF\nWONDER\nINDIAN EXPRESS\nराजहंस\n+SWITZERLAND\nLAND"
        ],
        expected_extraction=[{"llm_name": "Ticket to Ride: India + Switzerland", "llm_lang": "en"}],
        expected_matches=[{"id": ["106645"], "name": "Ticket to Ride Map Collection 2: India & Switzerland", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="nl_ticket_to_ride_nederland",
        title="Ticket to Ride: Nederland - Bordspel",
        description="Ticket to Ride: Nederland is een spannend bordspel waarin spelers spoorwegroutes bouwen door Nederland. Verzamel wagons, claim routes en verbind steden om de meeste punten te scoren. Geschikt voor meerdere spelers en een leuke uitdaging voor de hele familie!",
        image_texts=[
            "Alan R. Moon\nTICKET TO RIDE\n&NEDERLAND\nExtensi\nZUG\nZUG\nTICKET TO RIDE\nLES AVENTURIERS RAIL\nSTAVENTUREROS TREN!.\nMENOLIPPU\nDAYS OF\nWONDER",
            "Alan R. Moon\nAlan R. Moon\nTICKET TO RIDE\nHAO\nNEDERLAND\nTO RIDE\nNEDERLAND\nDeutschlan\nNEDERLAND"
        ],
        expected_extraction=[{"llm_name": "Ticket to Ride: Nederland", "llm_lang": "nl"}],
        expected_matches=[{"id": ["147938"], "name": "Ticket to Ride Map Collection 4: Nederland", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="nl_monopoly_bathmen",
        title="Gezelschapspel hasbro monopoly bathmen editie nieuw in doos",
        description="Gezelschapspel hasbro monopoly bathmen editie nieuw in doos\nKerst / sint tip\nVaste prijs 30 euro\nVzk en risico koper",
        image_texts=[
            "JUMBO\nHet beroemde vastgoedspel voor snelle onderhandelaars +\nBATHHEINE\nMONOPOLY\nBATHMEN\nJUMBO\nJUMBO",       
            "Herende vatranete onderhandelaar+\nMONOPOLY\nBATHMEN\nMet gepaste trots presenteren w\nMONOPOLY Bathment\nDeze unieke editie is een\nverzamelaarsobject voor iedereen\ndie Bathmen een warm hart\ntoedraagt\nLeef nu als vastgoedmagreat in Bathven\nLoop over het bord van de Brink via de\nSchoolstraat naar die Smidsweg Word eigenaar\n90\nB\nvan de Vegerinkskamp. Doe je boodschappen bij\nBB\nJumbo Johan Mersink aan de Larenseweg Koop huizen in elke straat\nbouw hotels op alle hotspots en laat het geld maar binnenstromen\nKoop, onderhandel en investeer zo veel je wit, maar blijf wel opletten: er is maar één winner\nSpeel dit fantastische spel met je familie, vrienden en bekenden en word dé vastgoedmagnaat ven Bathmen\nVeel speelpleziert\nJumbo Johan Mensink en team\n(met dank aan Camills en Enc Kein Nagelvoort)\nFotografe Cal HIVE\nHHOLD\nSpreng, speeien 80sencebean\n10 Kanton 10 kan met Algemeen Fond\n1 p MONOPOLY geld, 32 huler, 12 ho\n2dobbe\nMONOPOLY\nres THOSE DOM\nSTART"
        ],
        expected_extraction=[{"llm_name": "Monopoly: Bathmen", "llm_lang": "nl"}],
        expected_matches=[{"id": ["1406"], "name": "Monopoly", "lang": "en", "exact_match": False}] # Almost all Dutch editions not on expected_matches
    ),
    PromptTestCase(
        name="nl_monopoly_colmschate",
        title="Monopoly Colmschate",
        description="Als nieuw\n\nOphalen in Schalkhaar",
        image_texts=[
            "◆ Het beroemde vastgoedspel voor snelle onderhandelaars◆\nMONOPOLY\nCOLMSCHATE\nDalhuisen keurslager\nK\n8+8\n400\nELOVEDDIN\n460\nSTATIONSWEG\nSTART\nJE KRIJGT\nM200 SALARIS\nRCRA\n№400\nBETAAL 100\nOB\nWinkelcentrum\nColmschate"  
        ],
        expected_extraction=[{"llm_name": "Monopoly: Colmschate", "llm_lang": "nl"}],
        expected_matches=[{"id": ["1406"], "name": "Monopoly", "lang": "en", "exact_match": False}] # Almost all Dutch editions not on expected_matches
    ),
    PromptTestCase(
        name="nl_party_co",
        title="Party & co Original",
        description="Niet veel gebruikt",
        image_texts=[
            "14+\n45\n3-20\nHERZIENE\nEDITIE\nPARTY\n-& co\nORIGINAL\nMEER DAN EEN SPEL,\nHET IS ECHT EEN FEEST!"
        ],
        expected_extraction=[{"llm_name": "Party & Co: Original", "llm_lang": "nl"}],
        expected_matches=[{"id": ["13972", "29281"], "name": "Party & Co: Original", "lang": "en", "exact_match": True}] # 29281 is also Party & Co: Original
    ),
    PromptTestCase(
        name="nl_billy_bever",
        title="bert bever ravensburger",
        description="Bert Bever heeft in de rivier boomstammen opgestapeld die hij zorgvuldig bewaakt. Maar de beverkinderen proberen steeds weer de stammen te pikken. Eén voor één schuiven ze uit de stapel- heel voorzichtig, zodat er niets wiebelt! Anders merkt Bert de brutale diefstal en gaat hij als een razende tekeer.\n\nMaar pas op! In sommige stammen zijn houtwormen verstopt. Wat een pech! Want alleen die stammen tellen, die als symbool jaarringen of een ster hebben. Nu wordt snel nagekeken wat er op de magische toverfolie staat. De spanning stijgt! Wie zal als eerste zes waardevolle stammen buit maken? Hilarisch speelplezier voor de hele familie van Ravensburger.\n\nInhoud:\n\n1 beverdam(beek met twee oevers), 42 boomstammen en 42 boomschijven in 3 kleuren, 1 bever, 1 houten stokje, spelregels.",
        image_texts=[
            ""
        ],
        expected_extraction=[{"llm_name": "Bert Bever", "llm_lang": "nl"}],
        expected_matches=[{"id": ["50458", "35652"], "name": "Billy Biber", "lang": "en", "exact_match": True}] # 35652 Log Jam is the same game
    ),
    PromptTestCase(
        name="nl_camel_up",
        title="Nieuw! Camel Up bordspel - 999 Games",
        description="Helemaal nieuw in de folie / seal. Het bord spel Camel up van 999 Games. Onbeschadigd.",
        image_texts=[
            "STEFFEN\nBOGEN\nCAMEL\nSTAPEL\nDEGEKKE KAMELENRACE\n999\nGAMES\nSpeelggés\nJaar.nl\n牛油",
            "999\nGAMES\nDE STEKKE KAMELENRACE",
            "EL\nDESTANE KAMELENRACE\nWees getuige van de gekste kamelenrace ooit. De dieren springen onderweg op\nelkaar. Complete piramides Maan plotseling ondersteboven. Howl jij je huid keel in het\nhertst van de west\nAls leden van de Eeptische adel verzamelen de spelers sich in de woestijn met I simpel doel, het\nvendienen van zoveel mogelijk geld. Daartoe proberen ze te gokken welke kameel een cappe of\narifs de hele race wint. Gelak is hier echter niet de enige factor Wie de dynamiek van de wedstrijd\ngond leest en gevoel voor timing heeft, maalt net zoveel kans om de overwinning te behalen\nCamel Up is een eenvoudig, vlot en razend spannend familiespel voor maximaal 5 spelers\nInhoud: speelbord, I dabbelstenenpiramide, 5 kamelen, 5 dobbelstenen, 40 acetickets,\n15 etappetickets, 5 piramidetegels, 8 woestijntegels, 20 geldkaarten, 50 munten,\nI startspelerfiche, de spelregels\n220\n問\n2014 Eggertspete GmbH & C\n999 ver en distributeur\n909 Games B\nPostbus 103 30\nNL1320 AG A\nwww.999games w\nWantesenice\n0900-90000\nkantenservice 0999games.n\nGAMES Alle rechten voorbehouden\nMade in Germa\n特\nArt. Nr.: 999-CAM01\n2-8\n30\n8-99\nONLINE\nSPELUITLEG\nBLUF\nGELUK:\n8 717249 198598\nTACTIEK:\n*****\n*****\nAuteur: Steffen Bogen\nBustrats Dess\n20-beeld: Andreas Resch\nwww.\nCЄ"
        ],
        expected_extraction=[{"llm_name": "Camel Up", "llm_lang": "nl"}],
        expected_matches=[{"id": ["153938"], "name": "Camel Up", "lang": "nl", "exact_match": True}]
    ),
    PromptTestCase(
        name="nl_carcassonne_reiseditie",
        title="Carcassonne reiseditie - ongebruikt - 999 Games",
        description="Aangebodene de reis editie van het bekende spel Carcassonne. Met kleinere speelstukken in een doosje van ca 20 x 20 cm. Nog nooit gespeeld. De speelstukken moeten nog uit het karton worden gedrukt. Compleet.\n\nLichte gebruikssporen van schuiven in de kast en kleine beschadiging op achterzijde doos.",
        image_texts=[
            "Carcassonne Reiseditie\n999\nGAMES",
            "30\n20\n10",
            "Tegeloverzicht\n2x\nIN\nD\n4x\n3x K\n3x 1\nIN\nM\n2x N\n3x o\n3x Q\nSpeelmateriaal\n7 landh wander 1 stankaat mes doskese achterkam)\nrown defensa steden wegen, weiden en kleeders\n40 hoog in ken\nInder lige kan al taller\nunner her of\nweden ingrert Fen horige per\nkleur wordt als trharen gut\nDe spelregels en verbal\nHet doel van het spel\nA\nAlan\nHig\nyiner",
            ""
        ],
        expected_extraction=[{"llm_name": "Carcassonne Reiseditie", "llm_lang": "nl"}],
        expected_matches=[{"id": ["822"], "name": "Carcassonne", "lang": "en", "exact_match": False}] # Dutch edition not on expected_matches
    ),
    PromptTestCase(
        name="nl_kalaha",
        title="Kalaha - een vintage spel van Papita",
        description="Een mooi oud spel Kalaha van het merk Papita. Het spel is compleet, want alle (van piepschuim gemaakte) balletjes zijn aanwezig. Goed voor uren speelplezier.",
        image_texts=[
            "•\n.\npapita\nin the Noen kes\nme le pla\nDeskspiel erike\nKALAHA\nkpel at rika r\nThen het handig\n1965 ty tedenandse petentatinek tv Amsterdam under Berne and Universal Copyright Conventions",
            ""
        ],
        expected_extraction=[{"llm_name": "Kalaha", "llm_lang": "nl"}], # It is Dutch text on the cover, but hard to read
        expected_matches=[{"id": [""], "name": "", "lang": "", "exact_match": False}] # No Kalaha on expected_matches
    ),
    PromptTestCase(
        name="nl_monopoly_arnhem",
        title="Monopoly Arnhem Editie",
        description="Speel Monopoly in de Arnhem editie! Een leuke variant van het klassieke vastgoedspel. Geschikt voor snelle onderhandelaars en urenlang speelplezier. Inclusief alle originele onderdelen.",
        image_texts=[
            "Exclusieve\neditie\nMONOPOLY\nHet beroemde vastgoedspel voor snelle onderhandelaars\nARNHEM\nGONTY",
            "Exclusieve\neditie\nMONOPOLY\nHet beroemde vastgoedspel voor snelle onderhandelaars\nARNHEM\nU ONTVANGT\nM 200 SALARIS",
            "MONOPOLY\nARNHEM EDITIE 2016\nMONOPOLY.COM\nMONOPOLY\nARNHEM\n17 48\nB\n3\nBO\nBO\nARNHEM\nAhe nga heet dead brens He Aheme dech (mem) wat sterk af van arre\ndoor Heden\nbomen en parte ut en cuar te verlegenbad in dead Het Hedelench\nAe beendet\ne per ju e\nMONOPOLY\nARNHEM\nSTART\nberoemde od po\nCO0191040\nFutograhe\nVoor echte snelle spelers...\nTekstredacti\nOvative\nHOUD\nd&pone end"
        ],
        expected_extraction=[{"llm_name": "Monopoly: Arnhem", "llm_lang": "nl"}],
        expected_matches=[{"id": ["1406"], "name": "Monopoly", "lang": "en", "exact_match": False}] # Almost all Dutch editions not on expected_matches
    ),
    PromptTestCase(
        name="nl_monopoly_wereld",
        title="Monopoly Wereld Editie - Nieuw!",
        description="Gloednieuwe Monopoly Wereld Editie. Reis de wereld rond en koop bekende steden! Compleet en in perfecte staat. Geschikt voor de hele familie. Met de 'Snel Dobbelsteen' voor een sneller spel!",
        image_texts=[

        ],
        expected_extraction=[{"llm_name": "Monopoly: Wereldeditie", "llm_lang": "nl"}],
        expected_matches=[{"id": ["295051"], "name": "Monopoly World", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="en_rummy_o_deluxe",
        title="Rummy-O Deluxe Editie", # Or Rummy-O De Luxe
        description="Complete Rummy-O Deluxe editie in metalen doos. Het spel is in gebruikte staat, maar alle stenen en houders zijn aanwezig. Geschikt voor gezellige spelavonden met vrienden en familie.",
        image_texts=[
            "6 10\nCLASSIC GAMES.\n1 2 4\n35\n8 10 11\n11 12\n8\n3912\n8 10\nRUMMY-OF\nDE LUXE\n1 GAME SET ENS. DE 1 JEUX\nFamily\nFamille\nAge\nAge\n6+\nCardinal\nA WARNING:\nCHOKING HAZARD- Small parts.\nNot for children under 3 years.\nA AVERTISSEMENT:\nDANGER DE SUFFOCATION - Petites pièces.\nNe convient pas aux enfants de moins de 3 ans.",
            "SCORING VALUE OF T\nGOING\nNO\n8\n8\n5",
            "11\n10\n8\n5",
            "UK Instructions\nRUMMY-O\nA GAME FOR 2-4 PLAYERS\nA game of skill for adults 106 plastic tiles, 4 plastic racke\nHOW TO PLAY\nTHE TILES\nThe gaha Rummy Can comes of 106 1\nNUMBER OF PLAYERS\ncomponding to two packs of co\no it The unbon 111\nour players and a game com 4 rounds-sach say playing first one rodean playing, sach\nPILING AND DEALING THE TILES\nw each player has\nTHE PLAY\nLach pay\nthe it takes a\nThe test pay ate arranging h\nsher for a tas down stack or the the just acad\ntrange theses to Mets There are two type\nSCORING VALUE OF TILES\n18 11 12 13 counts 10 ports sack 2 through 9 count as\nGOING ON BOARD\nA\nThe dicas\nthe he\nGROUPS-thew"
        ],
        expected_extraction=[{"llm_name": "Rummy-O: Deluxe", "llm_lang": "en"}],
        expected_matches=[{"id": ["811"], "name": "Rummikub", "lang": "en", "exact_match": False}] # Rummikub == Rummy-O in English, Deluxe edition not on expected_matches
    ),
    PromptTestCase(
        name="nl_regenwormen",
        title="Regenwormen Dobbelspel - Familiespel vanaf 7 jaar",
        description="Leuk en educatief familiespel Regenwormen. Geschikt voor kinderen vanaf 7 jaar. Een spannend dobbelspel waarbij je slim moet gokken en tactisch moet spelen om de meeste regenwormen te verzamelen!",
        image_texts=[
            "Reiner Knizia\nRegerwormer\nCURRY\nlechts\nvers\nJakkie & Bak\nCollectie\n999\nGAMES",
            "GO/697-60/\n36 34\n3125\n::",
            "Reiner Knizia\nRegerwome!\nΣε\nBR322\nBEZOE\nO\nP\nને\n9\n31",
            "Voorbeelden van speelbeurten zonder resultaat:\nAfb6a\nKaren\nAfb6b\nMarianne\nAfb6c\n26\n28\n30\n2727\n25\nPeter\nEen tegel inleveren\nKaren dobbelt in haar vierde\nworp uitsluitend symbolen die ze\nal heeft afgelegd.\nMarianne dobbelt in haar derde\nworp twee vijven Hoewel ze\neen resultaat van 31 heeft en de\ntegel met waarde 31 openligt.\nmag ze geen tegel nemen, omdat\nze geen regenwormen heeft\ngedobbeld\nPeter dobbelt twee enen en\nkomt daarmee op 25. De tegel\nmet waarde 25 heeft hij al en er\nliggen geen lagere tegels meer in\nde rij. Pech gehad.\nWie een tegel moet inleveren, legt deze open terug in de rij. op de juiste plaats in\nde cijferreeks. Vervolgens draait hij de tegel met de hoogste waarde in de rij om\nzodat deze gedekt ligt. Deze tegel blijft de rest van het spel zo liggen en is uit het\nspel (zie afb. 7a).\nAls de zojuist teruggelegde tegel de hoogste waarde heeft. blijft deze openlig-\ngen en wordt er geen tegel omgedraaid (zie afb. 7b).\n7\nVoorbeelden van het inleveren van een tegel\n31\n33 34\n33 33\n27 Peter:\nམ3།|སྐམ།\n28 29\nKaren\n212\n30\nEinde van het spel\nPeter moet zijn openliggende\ntegel terug in de rij leggen\nOmdat de tegel met waarde 341\nmomenteel de hoogste is, draait\nhij deze om.\nKaren moet de tegel met waande\n30 terug in de rij leggen Omdat\ndeze tegel zelf de hoogste\nwaarde heeft, blijft deze openlig-\ngen. In dit geval wordt er geen\nandere tegel omgedraaid.\nHet spel is afgelopen als er geen open tegels meer in de rij liggen\nIedere speler telt nu het aantal regenwormen op zijn tegels. Wie de meeste\nregenwormen heeft. wint het spel Bij een gelijke stand wint de speler met de\ntegel met de hoogste waarde.\nVariant\nWie de speelduur wil verkorten of graag met\nmeer personen tegelijk (5-7 spelers) speelt.\nkan de volgende variant proberen Draai een\nteruggelegde tegel wel om als deze op dat\nmoment de hoogste waarde heeft.\n8\n©2005 Zoch\nIllustraties: Doris Matthaus\nAuteur Reiner Knizia\nUitgever en distributeur\n999 Games b.v.\nPostbus 60230\nNL-1320 AG Almere\nwww.999games.nl\nKlantenservice: 0900-999 00 00\nAlle rechten voorbehouden\nMade in Germany",
        ],
        expected_extraction=[{'llm_name': 'Regenwormen', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['15818'], 'name': 'pickomino', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_set",
        title="SET Kaartspel Ravensburger - Reactiespel voor Familie",
        description="Leuk en uitdagend reactiespel SET van Ravensburger. Geschikt voor spelers van 6 tot 99 jaar. Speel met het hele gezin en kijk wie de meeste sets kan verzamelen! Een snel en spannend spel dat de reactiesnelheid en het observatievermogen traint.",
        image_texts=[
            "SET!\nBBB\nUS\nBESTSELLER\nRavensburger\n27 175 7\nSET!\nRavensburger",
            "SET!\nBBB\nUS\nSETY\nRavensburger\nSET!\nSET!\nSET!\nBBB\nUS\nRavensburger",
            "",
            "Kaarten die een SET\nvormen hoeven niet\nLet op:\n000\n2222\nDe 3 kaarten die een SET vormen hoeven niet\nbij elkaar te liggen persé in een bepaald verband met elkaar te liggen\nledereen zoekt\ntegelijkertijd, de\nsnelste roept SET!\nGoed: speler krijgt\nSET, de kaarten\nworden weer tot 12\naangevuld\nmaar kunnen willekeurig door elkaar liggen. De drie\ngemarkeerde kaarten b.v. vormen een SET.\nAllen spelen tegelijkertijd! leder probeert zo snel\nmogelijk een SET te ontdekken. Wie denkt er één\ngevonden te hebben, roept luid en duidelijk \"SET\"\nen wijst de combinatie aan.\nAls het inderdaad klopt, neemt de speler de\nbetreffende 3 kaarten van tafel en legt ze blind\nvoor zich neer. Eén van de spelers vult de\nkaarten weer aan met 3 kaarten uit de stapel -\nen het spel gaat weer verder.\nAls het echter niet klopt, gaat het spel gewoon\nverder. De \"fout-speler\" mag als straf voor zijn\nvergissing niet meer meedoen tot een andere\nspeler een SET gevonden heeft.\nEr ligt geen SET op tafel? Het kan voorkomen dat\ner met de 12 kaarten op tafel geen SET te vormen\nis (of dat de spelers er na lang zoeken geen één\nkunnen vinden). In dat geval worden er gewoon\n3 kaarten bijgelegd. Na de volgende SET wordt het\naantal echter niet weer aangevuld tot 15.\nSET'S ALL! Einde van het spel\nHet spel is afgelopen wanneer alle kaarten van\nde stapel gebruikt zijn en er geen SET meer op\ntafel ligt.\nWie de meeste kaarten heeft, wint. SET'S the\nwinner!\nCHANGE SET! Varianten\nSET'S EASY\nEen vereenvoudiging voor beginners en jonge\nkinderen is het om slechts met de 27 kaarten van\neen kleur te spelen. Hiermee valt de eigenschap\nkleur helemaal weg en het spel wordt beduidend\neenvoudiger en sneller te overzien. In dit geval\nwordt gespeeld met 3 x 3 kaarten. Alle andere\nregels blijven gelden.\nNL\nFout: speler mag\nniet meedoen\nHet aantal uitge-\nlegde kaarten kan\ntijdelijk tot\n15 kaarten worden\nuitgebreid\nWinnaar is diegene\ndie de meeste\nkaarten heeft\nSlechts met één\nkleur spelen\n37",
        ],
        expected_extraction=[{'llm_name': 'SET', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['1198'], 'name': 'SET', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_snuffie_hup",
        title="Snuffie Hup! - Het Grappige Vang-het-Konijn Spel",
        description="Leuk en spannend spel Snuffie Hup! Probeer de konijntjes te vangen voordat ze wegspringen! Compleet met alle onderdelen. Geschikt voor kinderen vanaf 2 jaar.\nNog helemaal compleet en goed, alleen de doos is wel beschadigd.",
        image_texts=[
            "War\nSmiffic\nHET GRAPPIGE\nVANG-HET-KONIJN SPEL\n2013\nSpeelgoed\nJaar.nl",
        ],
        expected_extraction=[{'llm_name': 'Snuffie Hup!', 'llm_lang': 'nl'}],
        expected_matches=[{'id': [''], 'name': '', 'lang': '', 'exact_match': False}],
    ),
    PromptTestCase(
        name="nl_postcodeloterij_quiz_bingo",
        title="Postcodeloterij Quiz Bingo - Familiespel",
        description="Leuk en leerzaam familiespel: Postcodeloterij Quiz Bingo! Geschikt voor 3 tot 6 spelers vanaf 8 jaar. Test je kennis en speel bingo tegelijk! Een gezellig spel voor de hele familie.",
        image_texts=[
            "NATIONALE\nPOSTCODE\nPOSTCODE LOTERIJ\nQUIZ BINGO\nEEN KANJER VAN EEN SPEL!\nJUMBO",
            "BNATIONALE\nPOSTCODE\nBLOTERIJE\nPOSTCODE LOTERIJ\nQUIZ BINGO\nEEN KANJER VAN EEN SPEL!\n12.500\nCHEQUE\n8+\n45 min.\n3-6\nNL SPELREGELS\n5.00\nJUMBO",
            "POSTCODE LOTERIJ\nQUIZ BINGO\nEEN KANJER VAN EEN SPEL\nJUMBO\n2009\nPOSTCODE LOTERIJ\nQUIZ BINGO",
            "500\n000'0\nNATIONE\nBLOTERIJE\n10.000\n000'S\nSwitch\n2-\nтерма\n9-\nS+\nNAAM\n2\n3\n4\nA\nB\nPOSTCODE LOTERIJ\nBINGOKAART\n1 2 3 4 AB\nPRIJZEN\n아\n00\nSwitch\nSwitch\n+6\nCHEQUE\"\nPOSTCOM LOTECTIN QUE BINGO\nc2.500-\nPOSTCOM Lona QUIE BIG\n€12.500\nPOSTCOM LOTERIJ QUIZ\n10.000\nPOSTCOM LOTU QUE BONGO\n€5.000\n€5.000",
        ],
        expected_extraction=[{'llm_name': 'Postcodeloterij Quiz Bingo', 'llm_lang': 'nl'}],
        expected_matches=[{'id': [''], 'name': '', 'lang': '', 'exact_match': False}],
    ),
    PromptTestCase(
        name="nl_escape_room_the_game_vr",
        title="Escape Room The Game - Virtual Reality",
        description="Escape Room The Game Virtual Reality. Speel met of zonder het basisspel. Inclusief VR-bril. Geschikt voor 3-5 spelers vanaf 16 jaar. Met 2 spannende VR escape rooms.",
        image_texts=[
            "KAN MET EN ZONDER HET BASISSPEL GESPEELD WORDEN\nGenomme\n2017\nSpeelgoed\nJaar.nl\nESCAPE ROOM\nTHE GAME\nVIRTUAL REALITY\nESCARE\n1000INCLUSIEF VR-BRIL\n60\nMINUTES\nTO ESCAPE\nFriends\n16 3-5\nMET 2 SPANNENDE VR ESCAPE ROOMS\nIdentity\nGamos",
        ],
        expected_extraction=[{'llm_name': 'Escape Room: The Game - Virtual Reality', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['229315'], 'name': 'Escape Room: The Game – Virtual Reality', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="en_triominos",
        title="Triominos De Luxe - Leuk familiespel!",
        description="Triominos De Luxe, een spannend dominospel met driehoekige stenen. Geschikt voor jong en oud, en speelbaar met 1 tot 4 spelers.  Urenlang speelplezier gegarandeerd!\nInhoud: 56 stenen",
        image_texts=[
            "ــى\nt\n0\nD\n°\n5\nThe most fascinating variation of\nthe well-known game of Dominos, Now\nTriominos\nDe Luxe\ngiven an added dimension because strategy and logic. For 1-4 players\nGB) es. A game 6 Contents: 50 solid triangular tiles, 4 holding racks,\nNot suitable for children instructions\nKeep information for future reference.\nDe Luxe\nLa variante la plus\nfascinante du jeu de\nmentaire par les plaques triangulaires\nUn jeu de Fintech the four\n14 joueurs Contenu: 56 plaques\nNe convient pas aux entante en dessous de",
            "5\nـى\n5\nTriominos\nDe Luxe\nung Wichtig\n5\n5\nheld\nà la sortée de\nbeblos en kinderen ni mot deze plástic\nspele, in verband met mogelijk\nportant\nAre Pal donocarpent\nante\no, lontano dal biebe\nliore da asia guardar este erfor\necover buera del alcance de les nits.",
            "Safety First\nTo avoid dange of suffocation keep the wrapp\naway from batles and childre\nAchtung Wichtig\nDitte verhindem Sie, dass diese Hole in die Hande\nvon Baby und kleinkindern gelangt: Erstickungs\nAx\nimpogent\nNe polaisser ce sac la portée des enfants pour\néviter tout risqea asphyx\nVelligheid\nZorg dat babies en kinderen niotmet dezo plastic\nak kunnen spelen, in verba met gepeke\nverstocking\nImportante\nPor evitare Pericoil di soffocamento, teneto questo\nCinvolucro in ego sipuro, lontano dal bambini.\nImportante\nPara evitarligro de asfixia, guardar este\ntono en lugar seguro, fuera del alcance de los niños.\n(28215/20000225-134)",
        ],
        expected_extraction=[{'llm_name': 'Triominos De Luxe', 'llm_lang': 'en'}],
        expected_matches=[{'id': ['4040'], 'name': 'Tri-Ominos', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_monopoly_junior",
        title="Monopoly Junior - Leuk en Leerzaam!",
        description="Verkoop Monopoly Junior, het ideale bordspel voor jonge spelers! Leer spelenderwijs omgaan met geld en vastgoed. Geschikt voor 2-4 spelers. Uren speelplezier gegarandeerd!",
        image_texts=[
            "Het vastgoedspel voor snelle onderhandelaars &\nMONOPOLY\nJUNIOR\nMIJN EERSTE\nMONOPOLY-\nSPEL\nKLEINE DWARREL\nKLEINE T-REX\nLEEFTIJD\n5+\nRIJGT\nLARIS\nALS JE LANGS\nSTAR\nKO\nA WAARSCHUWING: MOET DOOR EEN\nVERSTICKINGSGEVAAR-bevat de\nNiet geschikt voor kinderen\nVOLWASSENE\nKAAR\nWORDEN.\nKLEINE PINGUIN\nHasbro\nGaming\nBADEENDJE",
        ],
        expected_extraction=[{'llm_name': 'Monopoly Junior', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['5339'], 'name': 'Monopoly Junior', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_wie_is_het_sterkste",
        title="Wie is het sterkste",
        description="Leuk gezelschapsspel om 4 personen te spelen. Nieuw de kaarten zijn  nog in de ingestelde verpakking.",
        image_texts=[
            "FINISH\nSTART\nsterkste team?..'\n'..wie is het\n?\n'..wie is het\n?\n?\nsterkste team?..\n?\nOOO",
            "..wie is het\nsterkste team?..\nteam!\nSTART\nH\na\nวอน S! อ!M\",\n'..wie is het\nsterkste team?..'",
            "tempo-team\n'..wie is\nhet sterkste\nteam?..'\nHet 30 seconden partyspel",
        ],
        expected_extraction=[{'llm_name': 'Wie is het sterkste team?', 'llm_lang': 'nl'}],
        expected_matches=[{'id': [''], 'name': '', 'lang': '', 'exact_match': False}],
    ),
    PromptTestCase(
        name="nl_de_zwakste_schakel",
        title="De Zwakste Schakel Bordspel",
        description="Compleet bordspel 'De Zwakste Schakel', gebaseerd op de bekende BBC quiz. Geschikt voor 4-9 spelers. In goede staat, inclusief alle onderdelen en spelregels.",
        image_texts=[
            "DE\nSHAKE\nHasbro\n4-9 Spelers\n12+\nJIJ\nbent de Zwakste Schakel.\ntot ziens!\nBBC",
            "2500\n2000\n1500\n1000\n500\n200\n100\n09\n4-9\nW&0000 2000\nLicensed by BBC Worldwide d\n2001\nrationale\nhet kort",
        ],
        expected_extraction=[{'llm_name': 'De Zwakste Schakel', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['57441'], 'name': 'Weakest Link', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_trivial_pursuit",
        title="Triviant pursuit",
        description="Gezelschapsspel om met meerdere personen te spelen",
        image_texts=[
            "Trivial Pursuit\nTrivial Pursui\nTrivial Pursuit\nTrivial Pursuit\nTAKE-AWAYS\nPKLAAR",
            "HORSZAWIE\nGENUS EDITIE\nTrivial Annuit\nFricial Parsal\nGENUS EDITIE\nTAKE-AWAY\nHAPKLAAR\nGROBE AW\nGENUS EDITIE",
            "Trivial Pursuit\nDE TWEEDE\nEDITIE\nKOMPLETE SET- GENUS EDITIE",
            "Pursuit\nEDITIE\nHAPKLA\nע\nfed ad\nSPELREGELS\nALLKER WAN",
        ],
        expected_extraction=[{'llm_name': 'Trivial Pursuit: Genus Editie', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['2952'], 'name': 'Trivial Pursuit: Genus Edition', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_geen_ja_nee",
        title="Geen Ja/Nee! - Leuk Vragenspel",
        description="Leuk en uitdagend vragenspel 'Geen Ja/Nee!' voor jong en oud. Test je kennis en reactievermogen met meer dan 900 vragen over diverse onderwerpen. Geschikt voor kinderen en volwassenen. Speelduur ongeveer 20 minuten.",
        image_texts=[
            "Ja\nGEEN\nGEEN\nNEE\nNe\nHet spel waarbij het verboden is\nJA of NEE te zeggen !\n• Een eenvoudig spel waarbij klein en\ngroot hun handigheid en verbeelding\nbewijzen!\n• Amuseer jullie met meer dan 900 vragen\ndie heel zorgvuldig werden bedacht om de\nhele familie te misleiden.\n• Vragen opgedeeld in 2 niveau's, voor\nkinderen en volwassenen, over allerlei\nonderwerpen:\ngeschiedenis, aardrijkskunde, muziek,\nsport, televisie...\nKan je in bomen klimmen?\ntot\nSPELERS\nvanaf\n7 JAAR\n1.\n2.\nHeb je geen hoogtevrees?\n3.\nWeet je wat dat is?\n1.\nIs dat een ziekte?\nZijn al je tanden nog echt?\n四\n2.\nHeb je de waterpokken al\ngehad?\n3.\n6.\nKrijg je die wanneer je te lang in\nhet water hebt gelegen?\nKAART VOOR KINDEREN\nSPELREGELS\nPoets je je tanden voor het ontbijt?\nOf ema?\nVoor je je 's ochtends wast?\nOfnadien?\nhebt?\nBen je zeker dat je geen valse tanc\ntanden dus nooit?\nWaar was ikah ja, je poetst je\nZei je nu ja?\n9.\nVoor het ontbijt?\n10. Dus niet erna?\nKAART VOOR VOLWASSENEN\nTrek een kaart en stel de vraag in de\njuiste volgorde aan je tegenstander. Als je\n\"ja\" of \"nee\" hoort, druk je zo snel mogelijk\nop de bel. De eerste die belt mag één stap\nvooruit op het bord.\nKan de tegenstander alle vragen beantwoorden\nzonder \"ja\" of \"nee\" te zeggen, dan mag hij\néén stap vooruit op het bord\nDe speler die als eerste het midden van het\nspelbord bereikt is de winnaar.\nSpelduur: ongeveer 20 minuten\nReferentie: N° 678 500\n3 760046 785008\nNee\n2 spelniveau's\n900\ngrappige\nvragen!\nComentats de mos of gouent des déments de s\nInhoud: 1 spelbord, 6 pionnen, 1 bel, 55 kaarten voor kinderen, 55 kaarten voor volwasenen, spelregels\nles Les comemon pouvoit a\nvoor kinderen jo",
            "GEEN\nGeen\nJa\nNee\nJa\nGEEN\nGeen\nNee\nKinderen\nVolwassenen",
            "1.\n1.\n1. 1.\nKen je het verhaal\nRoodkapje?\nDroom je vaak?\n2. Heb je soms nachtmerries?\n2. 2 2.\nHeeft zij een rode 3. Een mooie droom is toch leuker\n3. Zoals die van de\n[54]\n1.\nKijk je naar sport op televisie?\n[15]\n2.\nZei je ja?\n3. Hou je van voetbal?\n4.\nWie is je favoriete speler bij de\nnationale ploeg?\n5. Echt?\ndan een nachtmerrie, niet?\n6.\n3\n4.\n3\n4. Heeft de wolf Ro\nWeet je altijd nog wat je\n4 4\nopgegeten?\nwordt?\ngedroomd hebt, als je wakker\n7.\n8.\n55. En de drie big 5. Ik snurk 's nachts. Jij niet?\nE\n6. Dat is dus ee\n6. Zei je nee?\nIs ons land al eens Europees\nkampioen geweest?\nWas dat in 1996?\nDenk je dat ze nog eens Europees\nkampioen worden?\n9. Welk land heeft de laatste\nwereldbeker gewonnen?\n10. Ben je daar zeker van?\n2011 MEGABLEU\n2011 MEGABLEU",
            "ceen\nGeen\nNee\nDinc\nNee\nNee\nKinderen\nVolwassenen 9\nMEGABLEU\nJa\nCEEN\nGeen\nNEE\nDinc\nDinc\nHet spel waarbij het verboden is\nJA of NEE te zeggen!\n2\n900\nspelniveau's\ngrappige\nvragen!",
        ],
        expected_extraction=[{'llm_name': 'Geen Ja/Nee!', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['115435'], 'name': 'Nicht Ja, Nicht Nein', 'lang': 'de', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_party_co_junior",
        title="Party & Co Junior - Bordspel",
        description="Leuk en uitdagend bordspel Party & Co Junior van Jumbo. Met 560 vragen en opdrachten in 5 categorieën. Geschikt voor 3-20 spelers. Test je kennis en vaardigheden met dit gezellige spel!",
        image_texts=[
            "Met\n560 vragen &\nopdrachten\nin 5\ncategorieën\nPARTY\nTM\nJunior\nJUMBO\nVraag\n& Antwoord\nSchetsen\nNeuriën\nMimiek en gebaren\nVerboden Woord\n回家回\n8-13\n45 min.\n3-20\n回味\nOMDAT EEN SPEL MET VRIENDEN ALTIJD EEN FEEST IS",
        ],
        expected_extraction=[{'llm_name': 'Party & Co Junior', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['29268'], 'name': 'Party & Co: Junior', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_tik_tak_boem_junior",
        title="Tik Tak Boem Junior - Leuk familiespel!",
        description="Tik Tak Boem Junior is een spannend en leuk familiespel waarbij je snel moet denken! Verzin woorden die passen bij het thema op de kaart voordat de bom ontploft. Geschikt voor kinderen en volwassenen. Compleet met spelbord, kaarten en dobbelsteen.",
        image_texts=[
            "TIK\nTAK\nBOEM\nJUNIOR\n'Verzin een woord dat\nbij het thema op de kaarten\npast en geef de bom door aan\neen tegenspeler!'\nGoliath",
            "овшог\nPARTY\nPARTY\nPARTY\n200MENT\nGROOM 3008\n✔VIDED 10 XUSTMEN\nNEMOS",
        ],
        expected_extraction=[{'llm_name': 'Tik Tak Boem Junior', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['15383'], 'name': 'Pass the Bomb Junior', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_wie_is_het",
        title="Wie is het",
        description="Wie is het\nMet veel Disney en pixar figuren\nTe koop voor 10 euro",
        image_texts=[
            "B DISNEY\nLEN\nfiguren\nor elke\nan!\nWIE IS\nHETO\nMet heel\nveel van je favoriete\nDISNEY PIXAR\nfiguren!\nHet bekende omklapspel heeft een DISNEY-gezicht gekregen!",
            "୦୯୬,\nDe knappe prins",
        ],
        expected_extraction=[{'llm_name': 'Wie is het: Disney & Pixar', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['4143'], 'name': 'Guess Who?', 'lang': 'en', 'exact_match': False}],
    ),
    PromptTestCase(
        name="nl_taxi_mania_amsterdam",
        title="Taxi mania",
        description="Super leuk spel.ye koop voor 15 euro",
        image_texts=[
            "HESIMPLEM\nLOMON\nAnsore\nSTART\nKN\nTaxi.\nMania\nAMSTERDAM\n田\n100\nMama\n50\nMarua\nKanskaart\n501\nKlantkaart\nRitkaart\n20\nTax\nMama\n10\nRUS\nMama\n10\n5\nGoliath\nJaxia\nPUZZLE\nPUZZ\nS",
        ],
        expected_extraction=[{'llm_name': 'Taxi Mania: Amsterdam', 'llm_lang': 'en'}],
        expected_matches=[{'id': ['38647'], 'name': 'Taxifolie', 'lang': 'en', 'exact_match': True}], # Taxi Mania: Amsterdam is in alternate titles on BGG
    ),
    PromptTestCase(
        name="en_jenga",
        title="Jenga",
        description="Te koop je ga spel.\nTe koop voor 10 euro\nWord niet verzonden\n\nIk heb dit spel 2 keer.\nOok leuk om mee te bouwen",
        image_texts=[
            "JENGA",
            "",
        ],
        expected_extraction=[{'llm_name': 'Jenga', 'llm_lang': 'en'}],
        expected_matches=[{'id': ['2452'], 'name': 'Jenga', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_wie_is_het_reisspel",
        title="Wie is het? Reisspel - Het originele gezichten raadspel",
        description="Wie is het? Reisspel, het bekende gezichten raadspel van Hasbro. Ideaal voor onderweg! Raad wie de andere speler in gedachten heeft door slimme vragen te stellen. Geschikt voor 2 spelers en urenlang speelplezier.",
        image_texts=[
            "Het ORIGINELE gezichten raadspel\nWie is het?\nHet ORIGINELE gezichten raadspel\nB\nREISSPEL\nF\nLEAFTER\n6+\nHasbro",
        ],
        expected_extraction=[{'llm_name': 'Wie is het? Reisspel', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['4143'], 'name': 'Guess Who?', 'lang': 'en', 'exact_match': False}],
    ),
    PromptTestCase(
        name="nl_verdraaide_berichtjes",
        title="Verdraaide Berichtjes - Party Spel",
        description="Leuk partyspel 'Verdraaide Berichtjes' van de makers van What Do You Meme? Geschikt voor het hele gezin.  Urenlang speelplezier gegarandeerd!",
        image_texts=[
            "Van de makers van\nWHAT DO YOU MEME?\nWDYM\nOngelezen bericht\nVandaag 13:23\n50%\nVERDRAAIDE\nBERICHTJES\nEen partyspel voor het hele gezin...\nMEGABLEU",
        ],
        expected_extraction=[{'llm_name': 'Verdraaide Berichtjes', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['422870'], 'name': 'Twisted Texts', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_spiegel_jezelf",
        title="Spiegel Jezelf Spel",
        description="Leuk kaartspel 'Spiegel Jezelf'. Het spel is in nieuwe staat.\nverzendkosten voor de koper.",
        image_texts=[
            "Spiegel\njezelf\nspel\n...en vergr\ntrouwen",
        ],
        expected_extraction=[{'llm_name': 'Spiegel Jezelf', 'llm_lang': 'nl'}],
        expected_matches=[{'id': [''], 'name': '', 'lang': '', 'exact_match': False}],
    ),
    PromptTestCase(
        name="en_war_on_terror",
        title="War on Terror the Boardgame - Terror Bull Games",
        description="Een mooi vormgegeven satirisch, strategisch en controversiële bordspel. Het spel is compleet en de spel onderdelen zijn in goede staat. De doos is aan een zijde lichter verkleurd door de zon.",
        image_texts=[
            "2-6 PLAYERS\nAGES 14+\nDON'T\nPANIC\nWAR ON\nTERROR\nTHE BOARDGAME\nSPINNER\nAUD\nINCLUDES\nEVIL BALACLAVA",
            "ALASKA\nWEST\nCANADA\nNUNAVUT\nGREENLAND\nICELAND\nSCANDINAVIA\nHESTERN\nSTATES\nMID-WEST\nSTATES\nEASTERN\nSTATES\nMEXICO\nP\nCOLOMBIA\nVENEZUELA\nPERU\nBRAZIL\nARGENTINA\nEAST\nCANADA\nCUBA\nWAR ON\nTERROR\nTHE BOARDGAME\nFALKLANDS\nWEST\nNOWHERE\n60H\nUKRAINE\nWESTERN\nEUROPE\nEASTERN\nEUROPE\nBALKANS\nLIBYA\nALGERIA\nAXIS PEVIL\nEGYPT\nWESTERN\nRUSSIA\nIRAQ\nEMPIRE\nCARDS\nIRAN\nAFGHANISTAN\nSAUDI ARABIA\nNORTHERN\nRUSSIA\nTERRORIST\nCARDS\nMONGOLIA\nEASTERN\nRUSSIA\nPAKISTAN\nCHINA\nMALAYSIA\nINDIA\nSUDAN\nSOUTH\nAFRICA\n31\nLIBERATION POINTS\n2\nEACH\nNOWHERE\nMIDDLE OF NOWHERE\nCITY=1\nPOINT\n1.00\nEAST\nNOWHERE\nJAPAN\nINDONESIA\nNORTH\nAUSTRALIA\nSOUTH AUSTRALIA",
            "4\n8",
            "",
            "WORLD BANK OF CAPITALISM (500M\nWORLD BANK OF CAPITALISM (100M\n100M\nWORLD BANK OF CAPITALISM (50M\n50M\nWORLD BANK OF CAPITALISM 20M\n20M\nWORLD BANK OF CAPITALISM\n10M\n10M\nWORLD BANK OF CAPITALISM 5M\n5M\nA\n5M\nfer the profit of few at the cost of many",
            "TERR\n3266\nTEF T\nVID POLITICAL KIDNAP\n糖",
            "TERRORIST\nTE\nT\nTER\nESP\nRADIATIO\nRemove one Rad\nfrom the board\nFREE]\nSteal a ca\nOne free cl\nIn\nfor placemel\nC\nyour normal\nW\nIncite any terroris\nthe development in\noccupy or incite te\nRall to attack the\nAttack\nborderin\nswitch\nother\nKYOT\nTERRORIST ATTACK\nForce another\nKyoto Protoco\nBank for each\ntheir Empire.\nIncite any terrorist unit to attack\nthe development in the country they\noccupy or incite terrorist infighting\nRut to attack the following sired units\nREFERENCE CARD\nREFERENCE CARD\nREFERENCE CARD\nLIBER\n6 Em\n5\nEn\nTO WIN\nLIBERATION POINTS REQUIRED TO WIN\n6 Empires: 12\nREFERENCE CARD\nLIBERATION POINTS REQUIRED TO WIN\n6 Empires: 12\nAttack\nunits in\nterrorist\nCan be\nAtt\nA\nAtt\nAttack\nuni\nuni\nIncite\nunits\nIncite any\nter\nter\nthe de\nthe develo\nCa\nterrori\nother W\nCar\nоссиру\noth\nCan\noccupy or\noth\nતુ મા\nStrike\nRA\nk\nwithin\nTerrorist\n50m\nke Partial Strike\n5 Empires: 11\n4 Empires: 10\nREFERENCE CARD\nREFERENCE CARD\nLIBERATION POINTS REQUIRED TO WIN\nTER\nT\nTERRORIS\nREGIM TERRORIST MOVEMENT\n6 Empires: 12\n5 Empire: 11\n4 Empires: 10\n3 Empires: 9\n2 Empires: 8\n1 Empire: 7\nEach City 1 point\nunits\nIncit\nthe d\nterrori\nCan b\noccu\nother W\nRemove\nfrom th\ncosts.\nCross\nvilla\nRe\n10 4\nThis\nStrike\nfro\ndeve\nIncite\nthe de\noccup\nMove any terrorist un\nberdering the Terrori\nswitch any two to\nwithin a Terroris\nTerrorists cross sea rol\nConvert\ndevelopment,\nboard, to you\nregime change\nof the develop\n50m\nMove any terrorist unit to a country\nbordering the Terrorist Network or\nswitch any two terrorist units.\nwithin Terrorist Network.\nTerrorists cross sea routes for free.\nATURN\n1. Roll action de\n2. Take 2 cards\n3. \"Play\"\n4. Rollo dice\nACTION DIE\nBonus Card\nShuffle Deck\nSpin Axis of Ev",
            "",
            "WAR ON\nTERROR\nTHE BOARDGAME\nWAR\nTERR\nTHE BOARD\nWAR ON\nTERROR\nTHE BOARDGAME\nRULES OF ENG\nwww.waronterrorthebo\nCARD APPENDIX\nwww.waronterrortheboardgame.com",
            "TERROR\nTHE BOARDGAME\nFIGHT THE LONG WAR IN AN EVENING\nARON TERROR***\nTHE BOARDGAME\nTERRORBE",
            "EVIL BALACLAVA\nINCLUDES\nWAGE WAR ON THE MOST DANG\nWAR\nTERROR BALL GAMES",
        ],
        expected_extraction=[{'llm_name': 'War on Terror: The Boardgame', 'llm_lang': 'en'}],
        expected_matches=[{'id': ['24396'], 'name': 'War on Terror: The Boardgame', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_choo_choo",
        title="Choo-Choo - MB Spellen",
        description="Een mooi vintage spel. Compleet en gezien de leeftijd in uitstekende staat. Een actie bordspel waarbij het de bedoeling is om de juiste kleurcode op jouw bord te krijgen. Choo Choo is een spel voor 2 spelers.",
        image_texts=[
            "Alex Randolph\nMB CHOO-CHOO\nSPELLEN\n4 M.\nww\n7-14 jaar\n2 spelers\nWie maakt als eerste\nde juiste volgorde?\nSnel heen en weer schuiven,\ncombineren en rangeren.\ndaar gaat het om. Maar om\nals eerste de juiste volgorde\nte maken is lastiger dan je\ndenkt en daarom juist zo\nspannend.\nLeerzaam,\nplezierig en spannend.\nEerst wordt de volgorde vastgesteld\nProbeer nu zo vlug mogelijk de schijven\nin de juiste kleurvolgorde te krijgen.\n060\nDe volgorde is goed-pak de bel-je\nhebt gewonnen",
            "4715-4 ME\nCHOO-CHOO\nEen supersnel actie-spel\n2 spelers\nInhoud\n2 spelborden\n2 sets van 12 gekleurde schijven (drie stuks van\nelke vier kleuren per set)\n1 plastic zakje\n1 bel\n48 fiches (12 stuks van iedere (4) kleur)\n8 rubber beschermstukjes\nDoel van het spel\nZoveel mogelijk fiches verzamelen door als eerste\nde schijven in de juiste kleurvolgorde te schuiven.\nVoorbereiding\n1. Maak de gekleurde schijven los en sorteer ze\nop kleur.\n2. ledere speler neemt 12 schijven (3 stuks per\nkleur).\n3. Bevestig de rubber beschermstukjes onder de\nspelborden.\n4. ledere speler neemt een spelbord voor zich\n(fig. 1).\nBovenkant\nN.B. Rechts bovenin het spelbord is een opening\nvoor de schijven.\n5. Doe de 12 schijven als volgt in elk spelbord:\na. Op iedere schijf zit aan de bovenkant een\npuntje (fig. 2).\nPlaats alle 12 schijven stuk voor stuk in\nwillekeurige volgorde met de puntige kant\nboven, in de opening op het spelbord en\nschuif ze op het spelbord naar links.\nN.B. De schijven kunnen gemakkelijk op de\nspelborden heen en weer geschoven worden.\nOnder in het spelbord kunnen ze in de\nzijgleuven geschoven worden om zonodig de\nkleurvolgorde te kunnen veranderen.\nb. De 48 fiches worden in het plastic zakje\nbewaard.\nSchuiven\n1. Voor iedere ronde mag de volgorde van de\nschijven in de spelborden worden veranderd.\nMaak daarvoor gebruik van de zijgleuven\n(fig. 1).\n2. Voor het begin van elke ronde moeten alle 12\nschijven naar boven in het spelbord worden\ngeschoven (fig. 3).\nPuntje\nOpening om\nschijven in\nte doen\nZijgleuven\nFig. 2:\nGekleurde\nschijven\nFig. 1:\n1977 by Milton Bradley GmbH under Berne & Universal Copyright Convention. Mada in Holland.\nFig. 3: Schijven in startpositie\nvoor het begin van een ronde\nHet spel\n1. Maak uit wie spelleider van de eerste ronde is.\nDaarna is steeds de winnaar van de vorige\nronde spelleider.\n2. De bel wordt tussen de twee spelers geplaatst.\nDe spelleider belt als startsein voor de eerste\nronde.\n3. De spelers mogen de schijven op het spelbord\ndan niet meer verschuiven. (De schijven staan\nal in een bepaalde volgorde, zie punt 1 onder\nSCHUIVEN).\n4. De spelleider stelt nu de kleurvolgorde vast\ndoor één voor één de fiches uit het zakje te\nnemen (zonder te kijken) en deze op een rij\ntussen de spelers in op tafel te leggen, totdat\ner drie fiches van dezelfde kleur in de rij\nliggen. (De rij is dus nooit korter dan 3 of\nlanger dan 9 fiches.)\n5. De kleurvolgorde is nu vastgesteld. De\nspelleider belt weer en het spel begint.\n6. De spelers proberen zo vlug mogelijk hun\ngekleurde schijven in dezelfde volgorde te\nkrijgen als de rij fiches op tafel (hetzij van\nlinks naar rechts of andersom). De schijven\nblijven in het bord en mogen daar niet uitgehaald\nworden. Door gebruik te maken van de\nzijgleuven kan de juiste kleurvolgorde worden\nverkregen.\n7. Zodra een speler zijn schijven in de juiste\nvolgorde heeft, schuift hij zijn combinatie naar\nboven op zijn spelbord en pakt de bel.\n8. De speler die als eerste de bel luidt stopt het\nspel.\n9. De kleurvolgorde in het bord wordt vergeleken\nmet die van de fiches op tafel. Als het klopt\nheeft die speler gewonnen, zoniet dan gaat\nhet spel door. DE WINNAAR KRIJGT DE\nFICHES DIE OP TAFEL LIGGEN.\n10. Het spel gaat door totdat er geen fiches meer\nover zijn. De laatste ronde wordt zelfs nog\ngespeeld als er géén drie fiches van dezelfde\nkleur meer zijn.\nWinnaar\nWinnaar is degene die de meeste fiches heeft.\n4715-LNL 1177\nLAS\nINT-SUN",
            "",
            "e",
            "MB\nSPELLEN\nToonie\nww\n7-14 jaar\n2spelers\nWie maakt als eerste\nde juiste volgorde?\nSnel heen en weer schuiven.\ncombineren en rangeren\nat het om. Maar om\nste volgorde\ndenkt en diger dan je\nspannend\nLeerzaam,\n20\nplezierig en spannend.\nProbeer n zu why magas de schen\nin de juiste kleurigonde te kragen\n060\n69.00\nDe volgorde is good-pak de bel-j\nMB",
        ],
        expected_extraction=[{'llm_name': 'Choo-Choo', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['17689'], 'name': 'Choo-choo', 'lang': 'en', 'exact_match': True}],
    ),
    PromptTestCase(
        name="nl_willem_wiebel",
        title="Willem Wiebel | spel",
        description="Wie maken we hier blij mee?",
        image_texts=[
            "Wiljem Wiebel\nWillem kan het niet ge\nkrijgt hij werkelijk de\nkriebel ven det vresel\ngewiebel\nden lacht ledersen zich\nde vit end\nS\nSchmidt\nSpellen",
            "Wiljem Wiebel\nSpelmateriaal\n1 Willem Wiebel\n1 Platform\n1 Ladder uit twee delen\n4x3 Lege verfemmers\n1 Speciale dobbelsteen\n1 Handleiding\nSchmidt-Spelinfo\nSpeltype Behendigheidsspel\nAantal spelers: 2-4\nLeeftijd: 5-88\nSpelduur\n20 minuten\nHandigheid OOOOGeluk\nWillem Wiebel zit boven op zijn wankele ladder en probeert het plafond\neen nieuw kleurtje te geven. De emmers met verf die hij aan zijn voeten\nen aan de ladder gehangen heeft schommelen bedenkelijk. Zal alles\nwel goed gaan, of volt Willem mel emmers en al naar beneden? Maar\nje hoeft niet bang te zijn, het is maar een spelletje!\nDoel van het spel\nDe speler die als eerste alle emmers\nvan zijn kleur verf aan de voeten van\nWillem Wiebel weet te hangen, is win-\nnaar\nSchmidt\nSpellen",
            "",
        ],
        expected_extraction=[{'llm_name': 'Willem Wiebel', 'llm_lang': 'nl'}],
        expected_matches=[{'id': ['25769'], 'name': 'Willi Wackel', 'lang': 'en', 'exact_match': True}],
    ),
]
