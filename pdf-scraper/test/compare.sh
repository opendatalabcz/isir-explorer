#!/bin/bash
TEST_PATH="`dirname \"$0\"`"
cd "$TEST_PATH"

# Pdf soubory
FILES=$TEST_PATH/../data/all/*
REF_DIR=$TEST_PATH/../data/ref/

# Project path
cd ..
. venv/bin/activate

for f in $FILES
do
  baseName=$( basename $f )
  echo "Soubor $baseName"
  
  noExt="${baseName%.*}"
  refFile="${noExt}.json"
  refPath="$REF_DIR/$refFile"

  if [ "$1" == "--init" ]; then
    isir-scraper "$refPath" "$f"
  else
    output="$TEST_PATH/tmp.json"
    isir-scraper -o "$output" "$f"
    diff "$output" "$refPath" >/dev/null
    if [ $? -ne 0 ]; then
      echo -e "\e[91m===chyba===\e[39m";
      diff "$output" "$refPath"
    else
      echo -e "\e[92m===ok===\e[39m";
    fi
  fi
done


rm "$TEST_PATH/tmp.json" 2>/dev/null