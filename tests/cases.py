# tests/cases.py
from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class PromptTestCase:
    name: str
    title: str
    description: str
    image_texts: List[str]
    expected: List[Dict[str, str]]  # [{"name": "...", "lang": "nl"|"en"|"unknown"}]


TEST_CASES: List[PromptTestCase] = [
    PromptTestCase(
        name="nl_party_co_multiple",
        title="Party & Co + 1000 extra vragen",
        description="Niet veel gebruikt",
        image_texts=[
            "TM\nPARTY\nCO\nDiset\nOMDAT EEN SPEL MET VRIENDEN ALTIJD EEN FEEST IS\nTM\nPARTY\n& CO\n1000\nNIEUWE VRAGEN\nDiset\nAANVULLINGSSET MET 200 NIEUWE KAARTEN"
        ],
        expected=[{"name": "Party & Co", "lang": "nl"}, {"name": "Party & Co: 1000 Nieuwe Vragen", "lang": "nl"}],
    ),
    PromptTestCase(
        name="en_bandida",
        title="Bandida",
        description="Leuk kaartspel Bandida, in zo goed als nieuwe staat. Geschikt voor 1-4 spelers. Probeer samen te voorkomen dat Bandida ontsnapt! Een spannend en snel spel voor het hele gezin.",
        image_texts=[
            "BANDIDA\nWANTED⭑",
            "6-99\n1-4\n15'\nCoop\nGame Author: Martin Nedergaard Andersen\nGraphics & Illustration: Odile Sageat\nEN Bandida is trying to escape AGAIN. Team\nup to either stop her or help her escape!\nES Bandida está tratando de escapar\notra vez. ¡Únete al equipo para\ndetenerla o para ayudarla a evadirse!\nFR Bandida tente ENCORE de s'évader.\nUnissez vos forces pour l'arrêter\nou pour l'aider à s'échapper!\nDE Bandida versucht SCHON WIEDER\nauszubrechen. Haltet sie gemeinsam\nauf oder helft ihr zu fliehen!\n-\nIT Bandida sta DI NUOVO tentando\ndi evadere. Unite le forze per\nfermarla o per aiutarla a fuggire!\nNL Bandida probeert OPNIEUW te ontsnap-\npen. Werk samen om haar te stoppen\nof help haar samen ontsnappen!\n70 Cards\n1 Super card\nVideo rules\nwww.helvetiq.com"
        ],
        expected=[{"name": "Bandida", "lang": "en"}],
    ),
    PromptTestCase(
        name="nl_oud_en_nieuw_spel",
        title="Het Oud & Nieuw Spel - Dilemma's, Vragen, Uitbeelden",
        description="Leuk spel voor Oud & Nieuw! Bevat 20 dilemma's, 20 vragen en 20 uitbeeldingen. Perfect om de avond mee te vullen met vrienden en familie.",
        image_texts=[
            "HET OUD\n& NIEUW\nSPEL\n20X DILEMMA'S\n20X VRAGEN\n20X UITBEELDEN\nJEUX POUR SAINT SYLVESTRE\n20X DILEMMES, 20X QUESTIONS,\n20X MIMES"
        ],
        expected=[{"name": "Het Oud & Nieuw Spel", "lang": "nl"}],
    ),
    PromptTestCase(
        name="en_ticket_to_ride_europa",
        title="Ticket to Ride: Europa 1912",
        description="Ticket to Ride: Europa 1912 uitbreiding.  Voeg nieuwe varianten en routes toe aan je Ticket to Ride Europa spel.  Geschikt voor meerdere spelers. In goede staat.",
        image_texts=[
            "EUROPA 2\n1912\n4.183\nExpansion\nExtension\nA\nLisäosa\nZUG UM ZUG\nTICKET TO RIDE\nLES AVENTURIERS DU RAIL\nExpansion\nAVENTUREROS AL TREN!\nMENOLIPPU\nDAYS OF\nWONDER\nEUROPA",
            "EUROPA\n1912\nhe fumpu 1912 expamion brings new Warehouses and\nDepots to the exploration of your favorite European\ncities and introduces a whole n t of Destination Tickets!\nContains 5 Players Washouses, 25 in Depots,\n11 Destra\nTicket to Ride Europe with 5 new\nThis dut\nTickets t\nfor the Ticket to Ride family of board, A\nto play with the new Waries & Depois rule the new fickets induded are for\nuse only with it so ide up\nvec Europo 1912, apprener à utiliser les Entrepits et Depots dismisse\nplateau de jeu pour acquérir de nouvelles cartes et remporter la victoire\nDe nouvelles cartes Destination vous attendent également dans cette extension\nContents 25 been 101 cartes destination per even dead wige (\nCe produit est une EXTENSION s jeux de la série Les Aventuriery du at est poble de j\nfees riges des Entrepits et épôts aves tout explaire de la série. La nasc\nDestination set tables qu'avec Les Aventales d\nErweiterung Faropa 1912 bringt orue lagerhallen, Depots and Zielkarten ins Spiel\nSo steht der Erkandung Ihrer europaischen Lieblingsstädte nichts mehrt West\nDieses Spiel ist eine\nund Depots\nfor die Spiele der leg um fag\nspielen. Die in dieser trweiterung enthaltenes new\nke und k\nkaren sind hie\nAlso includes rules in\n\"\n24968\n11771\nLFCACA149\nMade\nin Germany\nCE\nDAYS OF\nWONDER"
        ],
        expected=[{"name": "ticket_to_ride_europa", "lang": "en"}],
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
        expected=[{"name": "Ticket to Ride: London", "lang": "nl"}],
    ),
    PromptTestCase(
        name="en_ticket_to_ride_multiple",
        title="Ticket to Ride: India + Zwitserland",
        description="Ticket to Ride: India en Zwitserland uitbreiding. Reis door India en Zwitserland in dit spannende bordspel. Geschikt voor meerdere spelers.",
        image_texts=[
            "Alan R. Moon\nTICKET TO RIDE\nINDIA\nBy Jan Vincent\nExtension\nZUG ZUG\nTICKET TO RIDE\nLES AVENTURIERS RAIL\n¡AVENTUREROS TREN!,\nMENOLIPPU\nDAYS OF\nWONDER\nराजहंस\n611\nAlan R. Moon\n+SWITZERLAND\n644",
            "Al R. Men\nAlan R. Mon\nTICKET TO RIDE\n+ SWITZERLAND\nET TO RIDE\nINDIA\nDAYS OF\nWONDER\nMARZALA\nMADRAS\nERODE\nDAYS OF\nWONDER\nINDIAN EXPRESS\nराजहंस\n+SWITZERLAND\nLAND"
        ],
        expected=[{"name": "Ticket to Ride: India", "lang": "en"}, {"name": "Ticket to Ride: Switzerland", "lang": "en"}],
    ),
    PromptTestCase(
        name="nl_ticket_to_ride_nederland",
        title="Ticket to Ride: Nederland - Bordspel",
        description="Ticket to Ride: Nederland is een spannend bordspel waarin spelers spoorwegroutes bouwen door Nederland. Verzamel wagons, claim routes en verbind steden om de meeste punten te scoren. Geschikt voor meerdere spelers en een leuke uitdaging voor de hele familie!",
        image_texts=[
            "Alan R. Moon\nTICKET TO RIDE\n&NEDERLAND\nExtensi\nZUG\nZUG\nTICKET TO RIDE\nLES AVENTURIERS RAIL\nSTAVENTUREROS TREN!.\nMENOLIPPU\nDAYS OF\nWONDER",
            "Alan R. Moon\nAlan R. Moon\nTICKET TO RIDE\nHAO\nNEDERLAND\nTO RIDE\nNEDERLAND\nDeutschlan\nNEDERLAND"
        ],
        expected=[{"name": "Ticket to Ride: Nederland", "lang": "nl"}],
    ),
    PromptTestCase(
        name="nl_monopoly_bathmen",
        title="Gezelschapspel hasbro monopoly bathmen editie nieuw in doos",
        description="Gezelschapspel hasbro monopoly bathmen editie nieuw in doos\nKerst / sint tip\nVaste prijs 30 euro\nVzk en risico koper",
        image_texts=[
            "JUMBO\nHet beroemde vastgoedspel voor snelle onderhandelaars +\nBATHHEINE\nMONOPOLY\nBATHMEN\nJUMBO\nJUMBO",       
            "Herende vatranete onderhandelaar+\nMONOPOLY\nBATHMEN\nMet gepaste trots presenteren w\nMONOPOLY Bathment\nDeze unieke editie is een\nverzamelaarsobject voor iedereen\ndie Bathmen een warm hart\ntoedraagt\nLeef nu als vastgoedmagreat in Bathven\nLoop over het bord van de Brink via de\nSchoolstraat naar die Smidsweg Word eigenaar\n90\nB\nvan de Vegerinkskamp. Doe je boodschappen bij\nBB\nJumbo Johan Mersink aan de Larenseweg Koop huizen in elke straat\nbouw hotels op alle hotspots en laat het geld maar binnenstromen\nKoop, onderhandel en investeer zo veel je wit, maar blijf wel opletten: er is maar één winner\nSpeel dit fantastische spel met je familie, vrienden en bekenden en word dé vastgoedmagnaat ven Bathmen\nVeel speelpleziert\nJumbo Johan Mensink en team\n(met dank aan Camills en Enc Kein Nagelvoort)\nFotografe Cal HIVE\nHHOLD\nSpreng, speeien 80sencebean\n10 Kanton 10 kan met Algemeen Fond\n1 p MONOPOLY geld, 32 huler, 12 ho\n2dobbe\nMONOPOLY\nres THOSE DOM\nSTART"
        ],
        expected=[{"name": "Monopoly: Bathmen", "lang": "nl"}],
    ),
    PromptTestCase(
        name="nl_monopoly_colmschate",
        title="Monopoly Colmschate",
        description="Als nieuw\n\nOphalen in Schalkhaar",
        image_texts=[
            "◆ Het beroemde vastgoedspel voor snelle onderhandelaars◆\nMONOPOLY\nCOLMSCHATE\nDalhuisen keurslager\nK\n8+8\n400\nELOVEDDIN\n460\nSTATIONSWEG\nSTART\nJE KRIJGT\nM200 SALARIS\nRCRA\n№400\nBETAAL 100\nOB\nWinkelcentrum\nColmschate"  
        ],
        expected=[{"name": "Monopoly: Colmschate", "lang": "nl"}],
    ),
    PromptTestCase(
        name="nl_party_co",
        title="Party & co Original",
        description="Niet veel gebruikt",
        image_texts=[
            "14+\n45\n3-20\nHERZIENE\nEDITIE\nPARTY\n-& co\nORIGINAL\nMEER DAN EEN SPEL,\nHET IS ECHT EEN FEEST!"
        ],
        expected=[{"name": "Party & Co: Original", "lang": "nl"}],
    ),
    PromptTestCase(
        name="",
        title="",
        description="",
        image_texts=[

        ],
        expected=[{"name": "", "lang": ""}],
    ),
    PromptTestCase(
        name="",
        title="",
        description="",
        image_texts=[

        ],
        expected=[{"name": "", "lang": ""}],
    ),
    PromptTestCase(
        name="",
        title="",
        description="",
        image_texts=[

        ],
        expected=[{"name": "", "lang": ""}],
    )
]
