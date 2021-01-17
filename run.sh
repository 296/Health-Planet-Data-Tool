#### FILL YOUR INFORMATION ####
LOGIN_ID=
CLIENT_ID=
CLIENT_SECRET=
CHECK_EXISTS_VENV=true
FROM_DATE=minimum
TO_DATE=today
OUT_FILE=out.json
#### END ####

script_dir=`$(cd $(dirname $0)); pwd`
echo $script_dir

if [ $CHECK_EXISTS_VENV = "true" ]; then
    if [ ! -e $script_dir/venv ]; then
        python3 -m venv $script_dir/venv
        source $script_dir/venv/bin/activate
        pip install -r requirements.txt
        deactivate
    fi
    source $script_dir/venv/bin/activate
fi

python3 $script_dir/run.py \
    -i $LOGIN_ID \
    -c $CLIENT_ID \
    -s $CLIENT_SECRET \
    -f $FROM_DATE \
    -t $TO_DATE \
    -o $OUT_FILE

if [ $CHECK_EXISTS_VENV = "true" ]; then
    deactivate
fi
