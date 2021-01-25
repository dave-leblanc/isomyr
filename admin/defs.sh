NAME=Isomyr
LIB=isomyr
EGG_NAME=$NAME
BZR='lp:~oubiwann/isomyr/trunk'
SVN='svn+https://isomyr.googlecode.com/svn/trunk'
FLAG='skip_tests'
MSG=commit-msg
export PYTHONPATH=.:./test:$PYTHONPATH

function getDiff {
    bzr diff $1 | \
        egrep '^\+' | \
        sed -e 's/^\+//g'| \
        egrep -v "^\+\+ ChangeLog"
}

function cleanup {
    echo "Cleaning up temporary files ..."
    rm -rf $MSG _trial_temp test.out doctest.out .DS_Store \
        CHECK_THIS_BEFORE_UPLOAD.txt build dist
    echo "Done."
}

function abort {
    echo "*** Aborting rest of process! ***"
    cleanup
    exit 1
}

function error {
    echo "There was an error committing/pushing; temp files preserved."
    abort
}

function localCommit {
    echo "Committing locally ..."
    bzr commit --local --file $MSG
}

function pushSucceed {
    echo "Push succeeded."
}

function pushLaunchpad {
    echo "Pushing to Launchpad now ($BZR) ..."
    bzr push $BZR && pushSucceed
    cleanup
}

function pushGoogle {
    #echo "Pushing to Google Code (Subversion) now ..."
    #bzr push $SVN
    PASS=""
}

function buildSucceed {
    echo "Build succeeded."
    echo
}
