
# Examples

1. Build a piechart of your activities, only to the 18.
./create_form.py JUN -f <FILE1> -f <FILE2> --printonly --to 18 --no-header | LC_CTYPE=en_us datamash -s -g 3 sum 2 | tr '\t' '|' |piechart --delimiter '|' --order legend,value --color contrast --percent > test.svg

1. Print only sum of activities:
./create_form.py JUN -f <FILE1>

1. Print only sum of activities, name starting with Thesis:
./create_form.py JUN -f <FILE1> --title "Thesis"
