import luminati as lm

session=lm.session('{username}','{password}')

r=session.get('https://api.myip.com')#returns usual request object

print(r.json())

#Every time uses different proxy

#Also chrome header is set by default to make your ban chances minimal

#but you still can parse from specific country if you want

session.get('https://api.myip.com',cc="ru")

#or set your own header

session.get('https://api.myip.com',headers={"User-Agent":"Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)"})

#or timeout

session.get('https://api.myip.com',timeout=10)

#TODO
Change UserAgent every time just like it happens with countries of origin