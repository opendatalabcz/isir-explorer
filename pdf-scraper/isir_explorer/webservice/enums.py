#Enums from WS ISIR docs v2.5

# These enums are mainly for ISIR->DB conversion, if you need to print a different string based on ID, use custom enum.

#druhRoleVRizeni
DRUH_ROLE_V_RIZENI = {
    "DLUŽNÍK": 1,
    "SPRÁVCE": 2,
    "VĚŘITEL": 3,
    "VĚŘIT-NAVR": 4,
}
DRUH_ROLE_V_RIZENI_INV = {v: k for k, v in DRUH_ROLE_V_RIZENI.items()}

#druhSpravce
DRUH_SPRAVCE = {
    "INS SPRÁV": 1,
    "ZVL SPRÁV": 2,
    "ZÁST INS S": 3,
    "PREDB.SPR.": 4,
    "VYR SPRÁV": 5,
    "ODDĚL SPR": 6,
    "SPRÁVCE": 98,
    "ZÁST SPR": 99,
}

#druhOsoby
DRUH_OSOBY = {
    "F": 1,
    "O": 2,
    "P": 3,
    "SPRÁV_INS": 4,
    "PODNIKATEL": 5,
    "POLICIE": 6,
    "SPRÁVCE_KP": 7,
    "EXEKUTOR": 8,
    "DAN_PORAD": 9,
    "OST_OVM": 10,
    "PAT_ZAST": 11,
    "S": 12,
    "SPR_ORGAN": 13,
    "U": 14,
    "Z": 15,
    "ZNAL_TLUM": 16,
    "ADVOKÁT": 17,
}

DRUH_OSOBY_INV = {v: k for k, v in DRUH_OSOBY.items()}

#druhPravniForma
DRUH_PRAVNI_FORMA = {
    "k. s.": 1,
    "o.p.s.": 2,
    "s.p.": 3,
    "s.p. likv": 4,
    "s.r.o.": 5,
    "spol s r.o": 5,
    "v.o.s.": 6,
    "a.s.": 7,
    "evrop. sp.": 8,
    "družstvo": 9,
    "S.V.J.": 99,
}

#druhStavRizeni
DRUH_STAV_RIZENI = {
    "NEVYRIZENA": 1,
    "MORATORIUM": 2,
    "ÚPADEK": 3,
    "KONKURS": 4,
    "ODDLUŽENÍ": 5,
    "REORGANIZ": 6,
    "VYRIZENA": 7,
    "PRAVOMOCNA": 8,
    "ODSKRTNUTA": 9,
    "ZRUŠENO VS": 10,
    "K-PO ZRUŠ.": 11,
    "OBZIVLA": 12,
    "MYLNÝ ZÁP.": 13,
    "NEVYR-POST": 14,
}

SOUDY = {
    "MSPHAAB": 1,
    "KSJIMBM": 2,
    "KSJICCB": 3,
    "KSVYCHK": 4,
    "KSVYCHKP1": 5,
    "KSSEMOS": 6,
    "KSSEMOSP1": 7,
    "KSZPCPM": 8,
    "KSSTCAB": 9,
    "KSSCEUL": 10,
    "KSSECULP1": 11,
    "CCA": 100,
}

SOUDY_INV_SHORT = {
    1: "MSPH",
    2: "KSBR",
    3: "KSCB",
    4: "KSHK",
    5: "KSPA",
    6: "KSOS",
    7: "KSOL",
    8: "KSPL",
    9: "KSPH",
    10: "KSUL",
    11: "KSLB",
}

SOUDY_INV_FULL = {
    1: "Městský soud v Praze",
    2: "Krajský soud v Brně",
    3: "Krajský soud v Českých Budějovicích",
    4: "Krajský soud v Hradci Králové",
    5: "Krajský soud v Hradci Králové - pobočka v Pardubicích",
    6: "Krajský soud v Ostravě",
    7: "Krajský soud v Ostravě - pobočka v Olomouci",
    8: "Krajský soud v Plzni",
    9: "Krajský soud v Praze",
    10: "Krajský soud v Ústí nad Labem",
    11: "Krajský soud v Ústí nad Labem - pobočka v Liberci",
}


class Udalosti:
    ZMENA_ADRESY_OSOBY = 2
    ZMENA_OSOBY = 1
    ZMENA_STAVU_VECI = 372
    ZMENA_VECI = 3
    ZASL_ZMENA_OSOBY = 625
