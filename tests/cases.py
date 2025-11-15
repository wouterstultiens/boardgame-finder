# tests/cases.py
from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class BGGMatch():
    id: str
    title: str
    lang: str
    exact_match: bool

@dataclass(frozen=True)
class PromptTestCase:
    name: str
    title: str
    description: str
    image_texts: List[str]
    expected_extraction: List[Dict[str, str]]
    expected_matches: Dict[str, BGGMatch]

TEST_CASES: List[PromptTestCase] = [
    PromptTestCase(
        name="nl_party_co_multiple",
        title="Party & Co + 1000 extra vragen",
        description="Niet veel gebruikt",
        image_texts=[
            "TM\nPARTY\nCO\nDiset\nOMDAT EEN SPEL MET VRIENDEN ALTIJD EEN FEEST IS\nTM\nPARTY\n& CO\n1000\nNIEUWE VRAGEN\nDiset\nAANVULLINGSSET MET 200 NIEUWE KAARTEN"
        ],
        expected_extraction=[
            {"name": "Party & Co", "lang": "nl"},
            {"name": "Party & Co: 1000 Nieuwe Vragen", "lang": "nl"}
        ],
        expected_matches=[
            {"id": "13972", "name": "Party & Co", "lang": "en", "exact_match": True}, 
            {"id": "31395", "name": "Party & Co: Expansion", "lang": "en", "exact_match": True}
        ]
    ),
    PromptTestCase(
        name="en_bandida",
        title="Bandida",
        description="Leuk kaartspel Bandida, in zo goed als nieuwe staat. Geschikt voor 1-4 spelers. Probeer samen te voorkomen dat Bandida ontsnapt! Een spannend en snel spel voor het hele gezin.",
        image_texts=[
            "BANDIDA\nWANTED⭑",
            "6-99\n1-4\n15'\nCoop\nGame Author: Martin Nedergaard Andersen\nGraphics & Illustration: Odile Sageat\nEN Bandida is trying to escape AGAIN. Team\nup to either stop her or help her escape!\nES Bandida está tratando de escapar\notra vez. ¡Únete al equipo para\ndetenerla o para ayudarla a evadirse!\nFR Bandida tente ENCORE de s'évader.\nUnissez vos forces pour l'arrêter\nou pour l'aider à s'échapper!\nDE Bandida versucht SCHON WIEDER\nauszubrechen. Haltet sie gemeinsam\nauf oder helft ihr zu fliehen!\n-\nIT Bandida sta DI NUOVO tentando\ndi evadere. Unite le forze per\nfermarla o per aiutarla a fuggire!\nNL Bandida probeert OPNIEUW te ontsnap-\npen. Werk samen om haar te stoppen\nof help haar samen ontsnappen!\n70 Cards\n1 Super card\nVideo rules\nwww.helvetiq.com"
        ],
        expected_extraction=[{"name": "Bandida", "lang": "en"}],
        expected_matches=[{"id": "299571", "name": "Bandida", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="nl_oud_en_nieuw_spel",
        title="Het Oud & Nieuw Spel - Dilemma's, Vragen, Uitbeelden",
        description="Leuk spel voor Oud & Nieuw! Bevat 20 dilemma's, 20 vragen en 20 uitbeeldingen. Perfect om de avond mee te vullen met vrienden en familie.",
        image_texts=[
            "HET OUD\n& NIEUW\nSPEL\n20X DILEMMA'S\n20X VRAGEN\n20X UITBEELDEN\nJEUX POUR SAINT SYLVESTRE\n20X DILEMMES, 20X QUESTIONS,\n20X MIMES"
        ],
        expected_extraction=[{"name": "Het Oud & Nieuw Spel", "lang": "nl"}],
        expected_matches=[{"id": "", "name": "", "lang": "", "exact_match": False}] # Not on expected_matches
    ),
    PromptTestCase(
        name="en_ticket_to_ride_europa",
        title="Ticket to Ride: Europa 1912",
        description="Ticket to Ride: Europa 1912 uitbreiding.  Voeg nieuwe varianten en routes toe aan je Ticket to Ride Europa spel.  Geschikt voor meerdere spelers. In goede staat.",
        image_texts=[
            "EUROPA 2\n1912\n4.183\nExpansion\nExtension\nA\nLisäosa\nZUG UM ZUG\nTICKET TO RIDE\nLES AVENTURIERS DU RAIL\nExpansion\nAVENTUREROS AL TREN!\nMENOLIPPU\nDAYS OF\nWONDER\nEUROPA",
            "EUROPA\n1912\nhe fumpu 1912 expamion brings new Warehouses and\nDepots to the exploration of your favorite European\ncities and introduces a whole n t of Destination Tickets!\nContains 5 Players Washouses, 25 in Depots,\n11 Destra\nTicket to Ride Europe with 5 new\nThis dut\nTickets t\nfor the Ticket to Ride family of board, A\nto play with the new Waries & Depois rule the new fickets induded are for\nuse only with it so ide up\nvec Europo 1912, apprener à utiliser les Entrepits et Depots dismisse\nplateau de jeu pour acquérir de nouvelles cartes et remporter la victoire\nDe nouvelles cartes Destination vous attendent également dans cette extension\nContents 25 been 101 cartes destination per even dead wige (\nCe produit est une EXTENSION s jeux de la série Les Aventuriery du at est poble de j\nfees riges des Entrepits et épôts aves tout explaire de la série. La nasc\nDestination set tables qu'avec Les Aventales d\nErweiterung Faropa 1912 bringt orue lagerhallen, Depots and Zielkarten ins Spiel\nSo steht der Erkandung Ihrer europaischen Lieblingsstädte nichts mehrt West\nDieses Spiel ist eine\nund Depots\nfor die Spiele der leg um fag\nspielen. Die in dieser trweiterung enthaltenes new\nke und k\nkaren sind hie\nAlso includes rules in\n\"\n24968\n11771\nLFCACA149\nMade\nin Germany\nCE\nDAYS OF\nWONDER"
        ],
        expected_extraction=[{"name": "Ticket to Ride: Europa 1912", "lang": "en"}],
        expected_matches=[{"id": "53383", "name": "Ticket to Ride: Europa 1912", "lang": "en", "exact_match": True}]
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
        expected_extraction=[{"name": "Ticket to Ride: London", "lang": "nl"}],
        expected_matches=[{"id": "276894", "name": "Ticket to Ride: London", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="en_ticket_to_ride_india_switzerland",
        title="Ticket to Ride: India + Zwitserland",
        description="Ticket to Ride: India en Zwitserland uitbreiding. Reis door India en Zwitserland in dit spannende bordspel. Geschikt voor meerdere spelers.",
        image_texts=[
            "Alan R. Moon\nTICKET TO RIDE\nINDIA\nBy Jan Vincent\nExtension\nZUG ZUG\nTICKET TO RIDE\nLES AVENTURIERS RAIL\n¡AVENTUREROS TREN!,\nMENOLIPPU\nDAYS OF\nWONDER\nराजहंस\n611\nAlan R. Moon\n+SWITZERLAND\n644",
            "Al R. Men\nAlan R. Mon\nTICKET TO RIDE\n+ SWITZERLAND\nET TO RIDE\nINDIA\nDAYS OF\nWONDER\nMARZALA\nMADRAS\nERODE\nDAYS OF\nWONDER\nINDIAN EXPRESS\nराजहंस\n+SWITZERLAND\nLAND"
        ],
        expected_extraction=[{"name": "Ticket to Ride: India + Switzerland", "lang": "en"}],
        expected_matches=[{"id": "106645", "name": "Ticket to Ride Map Collection 2: India & Switzerland", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="nl_ticket_to_ride_nederland",
        title="Ticket to Ride: Nederland - Bordspel",
        description="Ticket to Ride: Nederland is een spannend bordspel waarin spelers spoorwegroutes bouwen door Nederland. Verzamel wagons, claim routes en verbind steden om de meeste punten te scoren. Geschikt voor meerdere spelers en een leuke uitdaging voor de hele familie!",
        image_texts=[
            "Alan R. Moon\nTICKET TO RIDE\n&NEDERLAND\nExtensi\nZUG\nZUG\nTICKET TO RIDE\nLES AVENTURIERS RAIL\nSTAVENTUREROS TREN!.\nMENOLIPPU\nDAYS OF\nWONDER",
            "Alan R. Moon\nAlan R. Moon\nTICKET TO RIDE\nHAO\nNEDERLAND\nTO RIDE\nNEDERLAND\nDeutschlan\nNEDERLAND"
        ],
        expected_extraction=[{"name": "Ticket to Ride: Nederland", "lang": "nl"}],
        expected_matches=[{"id": "147938", "name": "Ticket to Ride Map Collection 4: Nederland ", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="nl_monopoly_bathmen",
        title="Gezelschapspel hasbro monopoly bathmen editie nieuw in doos",
        description="Gezelschapspel hasbro monopoly bathmen editie nieuw in doos\nKerst / sint tip\nVaste prijs 30 euro\nVzk en risico koper",
        image_texts=[
            "JUMBO\nHet beroemde vastgoedspel voor snelle onderhandelaars +\nBATHHEINE\nMONOPOLY\nBATHMEN\nJUMBO\nJUMBO",       
            "Herende vatranete onderhandelaar+\nMONOPOLY\nBATHMEN\nMet gepaste trots presenteren w\nMONOPOLY Bathment\nDeze unieke editie is een\nverzamelaarsobject voor iedereen\ndie Bathmen een warm hart\ntoedraagt\nLeef nu als vastgoedmagreat in Bathven\nLoop over het bord van de Brink via de\nSchoolstraat naar die Smidsweg Word eigenaar\n90\nB\nvan de Vegerinkskamp. Doe je boodschappen bij\nBB\nJumbo Johan Mersink aan de Larenseweg Koop huizen in elke straat\nbouw hotels op alle hotspots en laat het geld maar binnenstromen\nKoop, onderhandel en investeer zo veel je wit, maar blijf wel opletten: er is maar één winner\nSpeel dit fantastische spel met je familie, vrienden en bekenden en word dé vastgoedmagnaat ven Bathmen\nVeel speelpleziert\nJumbo Johan Mensink en team\n(met dank aan Camills en Enc Kein Nagelvoort)\nFotografe Cal HIVE\nHHOLD\nSpreng, speeien 80sencebean\n10 Kanton 10 kan met Algemeen Fond\n1 p MONOPOLY geld, 32 huler, 12 ho\n2dobbe\nMONOPOLY\nres THOSE DOM\nSTART"
        ],
        expected_extraction=[{"name": "Monopoly: Bathmen", "lang": "nl"}],
        expected_matches=[{"id": "1406", "name": "Monopoly", "lang": "en", "exact_match": False}] # Almost all Dutch editions not on expected_matches
    ),
    PromptTestCase(
        name="nl_monopoly_colmschate",
        title="Monopoly Colmschate",
        description="Als nieuw\n\nOphalen in Schalkhaar",
        image_texts=[
            "◆ Het beroemde vastgoedspel voor snelle onderhandelaars◆\nMONOPOLY\nCOLMSCHATE\nDalhuisen keurslager\nK\n8+8\n400\nELOVEDDIN\n460\nSTATIONSWEG\nSTART\nJE KRIJGT\nM200 SALARIS\nRCRA\n№400\nBETAAL 100\nOB\nWinkelcentrum\nColmschate"  
        ],
        expected_extraction=[{"name": "Monopoly: Colmschate", "lang": "nl"}],
        expected_matches=[{"id": "1406", "name": "Monopoly", "lang": "en", "exact_match": False}] # Almost all Dutch editions not on expected_matches
    ),
    PromptTestCase(
        name="nl_party_co",
        title="Party & co Original",
        description="Niet veel gebruikt",
        image_texts=[
            "14+\n45\n3-20\nHERZIENE\nEDITIE\nPARTY\n-& co\nORIGINAL\nMEER DAN EEN SPEL,\nHET IS ECHT EEN FEEST!"
        ],
        expected_extraction=[{"name": "Party & Co: Original", "lang": "nl"}],
        expected_matches=[{"id": "13972", "name": "Party & Co: Original", "lang": "en", "exact_match": True}]
    ),
    PromptTestCase(
        name="nl_billy_bever",
        title="bert bever ravensburger",
        description="Bert Bever heeft in de rivier boomstammen opgestapeld die hij zorgvuldig bewaakt. Maar de beverkinderen proberen steeds weer de stammen te pikken. Eén voor één schuiven ze uit de stapel- heel voorzichtig, zodat er niets wiebelt! Anders merkt Bert de brutale diefstal en gaat hij als een razende tekeer.\n\nMaar pas op! In sommige stammen zijn houtwormen verstopt. Wat een pech! Want alleen die stammen tellen, die als symbool jaarringen of een ster hebben. Nu wordt snel nagekeken wat er op de magische toverfolie staat. De spanning stijgt! Wie zal als eerste zes waardevolle stammen buit maken? Hilarisch speelplezier voor de hele familie van Ravensburger.\n\nInhoud:\n\n1 beverdam(beek met twee oevers), 42 boomstammen en 42 boomschijven in 3 kleuren, 1 bever, 1 houten stokje, spelregels.",
        image_texts=[
            ""
        ],
        expected_extraction=[{"name": "Bert Bever", "lang": "nl"}],
        expected_matches=[{"id": "50458", "name": "Billy Biber", "lang": "en", "exact_match": True}]
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
        expected_extraction=[{"name": "Camel Up", "lang": "nl"}],
        expected_matches=[{"id": "153938", "name": "Camel Up", "lang": "nl", "exact_match": True}]
    ),
    PromptTestCase(
        name="nl_carcassonne_reiseditie",
        title="Carcassonne reiseditie - ongebruikt - 999 Games",
        description="Aangebodene de reis editie van het bekende spel Carcassonne. Met kleinere speelstukken in een doosje van ca 20 x 20 cm. Nog nooit gespeeld. De speelstukken moeten nog uit het karton worden gedrukt. Compleet.\n\nLichte gebruikssporen van schuiven in de kast en kleine beschadiging op achterzijde doos",
        image_texts=[
            "Carcassonne Reiseditie\n999\nGAMES",
            "30\n20\n10",
            "Tegeloverzicht\n2x\nIN\nD\n4x\n3x K\n3x 1\nIN\nM\n2x N\n3x o\n3x Q\nSpeelmateriaal\n7 landh wander 1 stankaat mes doskese achterkam)\nrown defensa steden wegen, weiden en kleeders\n40 hoog in ken\nInder lige kan al taller\nunner her of\nweden ingrert Fen horige per\nkleur wordt als trharen gut\nDe spelregels en verbal\nHet doel van het spel\nA\nAlan\nHig\nyiner",
            ""
        ],
        expected_extraction=[{"name": "Carcassonne Reiseditie", "lang": "nl"}],
        expected_matches=[{"id": "822", "name": "Carcassonne", "lang": "en", "exact_match": False}] # Dutch edition not on expected_matches
    ),
    PromptTestCase(
        name="nl_kalaha",
        title="Kalaha - een vintage spel van Papita",
        description="Een mooi oud spel Kalaha van het merk Papita. Het spel is compleet, want alle (van piepschuim gemaakte) balletjes zijn aanwezig. Goed voor uren speelplezier.",
        image_texts=[
            "•\n.\npapita\nin the Noen kes\nme le pla\nDeskspiel erike\nKALAHA\nkpel at rika r\nThen het handig\n1965 ty tedenandse petentatinek tv Amsterdam under Berne and Universal Copyright Conventions",
            ""
        ],
        expected_extraction=[{"name": "Kalaha", "lang": "nl"}], # It is Dutch text on the cover, but hard to read
        expected_matches=[{"id": "", "name": "", "lang": "", "exact_match": False}] # No Kalaha on expected_matches
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
        expected_extraction=[{"name": "Monopoly: Arnhem", "lang": "nl"}],
        expected_matches=[{"id": "1406", "name": "Monopoly", "lang": "en", "exact_match": False}] # Almost all Dutch editions not on expected_matches
    ),
    PromptTestCase(
        name="nl_monopoly_wereld",
        title="Monopoly Wereld Editie - Nieuw!",
        description="Gloednieuwe Monopoly Wereld Editie. Reis de wereld rond en koop bekende steden! Compleet en in perfecte staat. Geschikt voor de hele familie. Met de 'Snel Dobbelsteen' voor een sneller spel!",
        image_texts=[

        ],
        expected_extraction=[{"name": "Monopoly: Wereldeditie", "lang": "nl"}],
        expected_matches=[{"id": "295051", "name": "Monopoly World", "lang": "en", "exact_match": True}]
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
        expected_extraction=[{"name": "Rummy-O: Deluxe", "lang": ""}],
        expected_matches=[{"id": "811", "name": "Rummikub", "lang": "en", "exact_match": False}] # Rummikub == Rummy-O in English, Deluxe edition not on expected_matches
    )
]
