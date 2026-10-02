import re
old=open('eg-redline.html').read(); img=re.search(r'const IMG = "([^"]*)";',old).group(1)
t=open('template.html').read().replace('__DATA__',open('data.json').read()).replace('__SUGG__',open('../sugg.json').read()).replace('__IMG__',img)
open('eg-redline.html','w').write(t)
s=re.findall(r'<script>(.*?)</script>',t,re.S); open('/tmp/x.js','w').write(s[-1])
