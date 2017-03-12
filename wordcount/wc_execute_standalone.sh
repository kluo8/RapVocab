#!/usr/bin/env bash

# Execute wordcount for artist texts in standalone mode using Apache Spark
# Requires following env variables: 
#	- Spark bin directory added to PATH
#	- SPARK var pointing to spark folder location

export PYTHONPATH=${SPARK}/python

OUTPUT="output"

# Clean output directory
if [ -d "$OUTPUT" ]; then
  rm -rf $OUTPUT
fi
mkdir $OUTPUT

chmod 775 wordcount.py

./wordcount.py

echo "Diversity (Regular) Results:"
cat diversity_regular.txt