#!/usr/bin/env bash

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# IPP - csv - doplňkové testy - 2014/2015
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Činnost: 
# - vytvoří výstupy studentovy úlohy v daném interpretu na základě sady testů
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# Popis (README):
#
# Struktura skriptu _stud_tests.sh (v kódování UTF-8):
# Každý test zahrnuje až 4 soubory (vstupní soubor, případný druhý vstupní 
# soubor, výstupní soubor, soubor logující chybové výstupy *.err vypisované na 
# standardní chybový výstup (pro ilustraci) a soubor logující návratový kód 
# skriptu *.!!!). Pro spuštění testů je nutné do stejného adresáře zkopírovat i 
# váš skript. V komentářích u jednotlivých testů jsou uvedeny dodatečné 
# informace jako očekávaný návratový kód. 
#
# Proměnné ve skriptu _stud_tests.sh pro konfiguraci testů:
#  INTERPRETER - využívaný interpret 
#  EXTENSION - přípona souboru s vaším skriptem (jméno skriptu je dáno úlohou) 
#  LOCAL_IN_PATH/LOCAL_OUT_PATH - testování různých cest ke vstupním/výstupním
#    souborům
#  
# Další soubory archivu s doplňujícími testy:
# V adresáři ref-out najdete referenční soubory pro výstup (*.out nebo *.xml), 
# referenční soubory s návratovým kódem (*.!!!) a pro ukázku i soubory s 
# logovaným výstupem ze standardního chybového výstupu (*.err). Pokud některé 
# testy nevypisují nic na standardní výstup nebo na standardní chybový výstup, 
# tak může odpovídající soubor v adresáři chybět nebo mít nulovou velikost.
# V adresáři s tímto souborem se vyskytuje i soubor csv_options 
# pro nástroj JExamXML, který doporučujeme používat na porovnávání XML souborů. 
# Další tipy a informace o porovnávání souborů XML najdete na Wiki IPP (stránka 
# https://wis.fit.vutbr.cz/FIT/st/cwk.php?title=IPP:ProjectNotes&id=9999#XML_a_jeho_porovnávání).
#
# Doporučení a poznámky k testování:
# Tento skript neobsahuje mechanismy pro automatické porovnávání výsledků vašeho 
# skriptu a výsledků referenčních (viz adresář ref-out). Pokud byste rádi 
# využili tohoto skriptu jako základ pro váš testovací rámec, tak doporučujeme 
# tento mechanismus doplnit.
# Dále doporučujeme testovat různé varianty relativních a absolutních cest 
# vstupních a výstupních souborů, k čemuž poslouží proměnné začínající 
# LOCAL_IN_PATH a LOCAL_OUT_PATH (neomezujte se pouze na zde uvedené triviální 
# varianty). 
# Výstupní soubory mohou při spouštění vašeho skriptu již existovat a pokud není 
# u zadání specifikováno jinak, tak se bez milosti přepíší!           
# Výstupní soubory nemusí existovat a pak je třeba je vytvořit!
# Pokud běh skriptu skončí s návratovou hodnotou různou od nuly, tak není 
# vytvoření souboru zadaného parametrem --output nutné, protože jeho obsah 
# stejně nelze považovat za validní.
# V testech se jako pokaždé určitě najdou nějaké chyby nebo nepřesnosti, takže 
# pokud nějakou chybu najdete, tak na ni prosím upozorněte ve fóru příslušné 
# úlohy (konstruktivní kritika bude pozitivně ohodnocena). Vyhrazujeme si také 
# právo testy měnit, opravovat a případně rozšiřovat, na což samozřejmě 
# upozorníme na fóru dané úlohy.
#
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

TASK=csv
#INTERPRETER="php -d open_basedir=\"\""
#EXTENSION=php
INTERPRETER=python3
EXTENSION=py

# cesty ke vstupním a výstupním souborům
LOCAL_IN_PATH="./" # (simple relative path)
LOCAL_IN_PATH2="" #Alternative 1 (primitive relative path)
LOCAL_IN_PATH3=`pwd`"/" #Alternative 2 (absolute path)
LOCAL_OUT_PATH="./" # (simple relative path)
LOCAL_OUT_PATH2="" #Alternative 1 (primitive relative path)
LOCAL_OUT_PATH3=`pwd`"/" #Alternative 2 (absolute path)
# cesta pro ukládání chybového výstupu studentského skriptu
LOG_PATH="./"


# test01: basic test; Expected output: test01.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test01.csv --output=${LOCAL_OUT_PATH}test01.xml 2> $LOG_PATH/test01.err
echo -n $? > test01.!!!

# test02: custom line element with dash; Expected output: test02.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -l="ra-dek" --input=${LOCAL_IN_PATH}test02.csv > ${LOCAL_OUT_PATH}test02.xml  2> ${LOG_PATH}test02.err
echo -n $? > test02.!!!

# test03: rooted output with indexed custom line element (no header); Expected output: test03.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -l=radek -r=root --input=${LOCAL_IN_PATH2}test03.csv -i -n > ${LOCAL_OUT_PATH2}test03.xml 2> ${LOG_PATH}test03.err
echo -n $? > test03.!!!

# test04: semicolon as a separator; Expected output: test04.xml; Expected return code: 32
$INTERPRETER $TASK.$EXTENSION -s=\; > ${LOCAL_OUT_PATH3}test04.xml < ${LOCAL_IN_PATH}test04.csv 2> ${LOG_PATH}test04.err
echo -n $? > test04.!!!

# test05: semicolon as a separator with error recovery; Expected output: test05.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test05.csv -s=\; -e > ${LOCAL_OUT_PATH3}test05.xml 2> ${LOG_PATH}test05.err
echo -n $? > test05.!!!

# test06: multi-option with header and indexing starting at 2; Expected output: test06.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --start=2 --input=${LOCAL_IN_PATH}test06.csv --output=${LOCAL_OUT_PATH}test06.xml -h -i -l=data 2> ${LOG_PATH}test06.err
echo -n $? > test06.!!!

# test07: quotas versus apostrophes; Expected output: test07.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test07.csv --output=${LOCAL_OUT_PATH}test07.xml  2> ${LOG_PATH}test07.err
echo -n $? > test07.!!!

# test08: apostrophes versus quotas; Expected output: test08.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test08.csv --output=${LOCAL_OUT_PATH}test08.xml  2> ${LOG_PATH}test08.err
echo -n $? > test08.!!!

# test09: tests diacritics in elements and cells; Expected output: test09.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH}test09.csv -h --output=${LOCAL_OUT_PATH}test09.xml  -r=róót 2> ${LOG_PATH}test09.err
echo -n $? > test09.!!!

# test10: multiline input with header - linefeed in a string; Expected output: test10.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -h --input=${LOCAL_IN_PATH}test10.csv --output=${LOCAL_OUT_PATH}test10.xml  2> ${LOG_PATH}test10.err
echo -n $? > test10.!!!

# test11: tests diacritics and special characters in a string; Expected output: test11.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -l=line -i --input=${LOCAL_IN_PATH}test11.csv --output=${LOCAL_OUT_PATH}test11.xml 2> ${LOG_PATH}test11.err
echo -n $? > test11.!!!

# test12: header leading to invalid element (starts with a dash); Expected output: test12.xml; Expected return code: 31
$INTERPRETER $TASK.$EXTENSION -h --input=${LOCAL_IN_PATH}test12.csv --output=${LOCAL_OUT_PATH}test12.xml 2> ${LOG_PATH}test12.err
echo -n $? > test12.!!!

# test13: TAB (	) separator, indexing starts at 5; Expected output: test13.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH2}test13.csv --start=5 -i --output=${LOCAL_OUT_PATH}test13.xml -s=TAB -l=row 2> ${LOG_PATH}test13.err
echo -n $? > test13.!!!

# test14: TAB (	) separator, the header with diacritics; Expected output: test14.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -s=TAB -h --input=${LOCAL_IN_PATH2}test14.csv --output=${LOCAL_OUT_PATH2}test14.xml 2> ${LOG_PATH}test14.err
echo -n $? > test14.!!!

# test15: invalid number of columns (the header contains just one column); Expected output: test15.xml; Expected return code: 32
$INTERPRETER $TASK.$EXTENSION --input=${LOCAL_IN_PATH2}test15.csv -r=root --output=${LOCAL_OUT_PATH3}test15.xml 2> ${LOG_PATH}test15.err
echo -n $? > test15.!!!

# test16: root element with error recovery with preservation of all columns; Expected output: test16.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION --all-columns -e -r=root --input=${LOCAL_IN_PATH3}test16.csv --output=${LOCAL_OUT_PATH}test16.xml 2> ${LOG_PATH}test16.err
echo -n $? > test16.!!!

# test17: invalid root element name (starts with a space); Expected output: test17.xml; Expected return code: 30
$INTERPRETER $TASK.$EXTENSION --error-recovery -r=" root" --input=${LOCAL_IN_PATH3}test17.csv --output=${LOCAL_OUT_PATH2}test17.xml 2> ${LOG_PATH}test17.err
echo -n $? > test17.!!!

# test18: combination of -e, -h=, --all-columns and --missing-field=; Expected output: test18.xml; Expected return code: 0
$INTERPRETER $TASK.$EXTENSION -e -h=jk --all-columns --missing-field=chybí -c=Kontakt --input=${LOCAL_IN_PATH3}test18.csv --output=${LOCAL_OUT_PATH3}test18.xml 2> ${LOG_PATH}test18.err
echo -n $? > test18.!!!
