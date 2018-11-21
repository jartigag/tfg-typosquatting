git filter-branch -f --env-filter \
    'if [ $GIT_COMMIT = 653d2451d7053793993539e96172c99e2e7ceade ]
     then
         export GIT_AUTHOR_DATE="Wed Nov 21 10:00:00 2018 +0200"
         export GIT_COMMITTER_DATE="Wed Nov 21 10:00:00 2018 +0200"
     fi'
