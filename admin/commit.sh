. ./admin/defs.sh

getDiff ChangeLog > $MSG
echo "Committing with this message:"
cat $MSG
echo
# skip the tests if the appropriate flag was passed
if [[ "$1" == "$FLAG" ]];then
    echo 'OK' > test.out
else
    # send the output (stdout and stderr) to both a file for checking and
    # stdout for immediate viewing/feedback purposes
    trial $LIB 2>&1|tee test.out
    ./admin/testDocs.py 2>&1|tee doctest.out
fi
TEST_STATUS=`tail -1 test.out`
DOCTEST_STATUS=`tail -1 doctest.out`
STATUS=`echo "$TEST_STATUS $DOCTEST_STATUS"|grep 'FAIL'`
if [[ "$STATUS" == '' ]];then
    if [[ "$1" == "FLAG" ]];then
        echo "Skipping tests..."
    else
        echo "All tests passed."
    fi
    ./admin/checkBuild.sh || error
    localCommit && cleanup || error
else
    abort
fi
