python $1

file_name=$1

if [ $file_name == "Fluffy.py" ]; then
    cp $file_name "./example/"
fi
