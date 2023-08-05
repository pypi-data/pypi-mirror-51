#! /usr/bin/bash
export OWLFILE=sct2_sRefset_OWLExpressionFull_INT_20190731.txt
export DESCFILE=sct2_Description_Snapshot-en_INT_20190731.txt
export OUTFILE=owl20190731.owl
export CIDFILE=concepts.owl
# touch $OWLFILE
# touch $OUTFILE
gawk -F'\t' '{if ($3 == 1) print $6}' $OWLFILE | sort | uniq > $CIDFILE
gawk -F'\t' '{if ($3 == 1) print $7}' $OWLFILE | grep "^Prefix" > $OUTFILE
gawk -F'\t' '{if ($3 == 1) print $7}' $OWLFILE | grep "^Ontology" | sed "s/)\r//" >> $OUTFILE
gawk -F'\t' '{if ($3 == 1) print $7}' $OWLFILE | grep "^Equivalent" >> $OUTFILE
gawk -F'\t' '{if ($3 == 1) print $7}' $OWLFILE | grep "^Sub" >> $OUTFILE
gawk -F'\t' '{if ($3 == 1) print $7}' $OWLFILE | grep "^Reflex" >> $OUTFILE
gawk -F'\t' '{if ($3 == 1) print $7}' $OWLFILE | grep "^Transitive" >> $OUTFILE

# AnnotationAssertion(rdfs:label :Triangle "Driehoek"@nl)

gawk -F'\t' '{if ($3 == 1) print $5 "\t" $6 "\t" $7 "\t" $8 "\t" $9}' $DESCFILE | grep -f $CIDFILE | sed 's/\"/\\\"/g' | gawk -F'\t' '{if($3 == 900000000000003001) print "AnnotationAssertion(rdfs:label :" $1 " \"" $4 "\"@"  $2 ")"}' >> $OUTFILE

# Print closing bracket
echo ")" >> $OUTFILE
o a brief