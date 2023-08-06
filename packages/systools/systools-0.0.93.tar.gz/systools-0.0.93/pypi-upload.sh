# pip install m2r
m2r README.md
git rm -r --cached . ; git add . ; git commit -m "minor updates" ; git push -u origin master
python setup.py sdist upload
