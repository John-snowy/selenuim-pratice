# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 23:06:39 2022

@author: me
"""

import requests

API_KEY = "LisY5n8WGSiXuhiBAfDiCY2e"
SECRET_KEY = "zBdVxMblkMR1OjDzTXW4uPssrxt8gZqj"
zBdVxMblkMR1OjDzTXW4uPssrxt8gZqj

def main():
        
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + get_access_token()
    
    payload='image=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAARgAAABXCAMAAADoKaqzAAAAb1BMVEXwyMiAjQWYu8exztGfvNScltHC3NLQwLucq86xqrTU4Za2xKjUuZe4qmbiwK%2BOlB2cmzWqo07GsX6DkB6Vo5uOnGmKmFCOkWuDjh6eoEmKkxuUmTKqxbeGlR6etYSLnlKbtrqDkh6XsKCVoimfrDtdNYYJAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAHNUlEQVR4nO2ciZajKBSGpZJKXHDtnpmetWuW93%2FGERC5FwibaEzN%2FOd0OiYq8uXen0WsovgvqWnkiyFCCPvHXmLOeOHKcnFPV9PUto9nJMtLhAST1yfTCFnAkDQyKUjuTPGH7SmRRPaIUWSiFJ9KHMrJyCwWYwFDipREkoqPm5OB4alkixiSSibBY%2B73E%2BaSUG2LGEkmUtGpJJDsCuZySWoray70UaK%2FJGmxmP0jJktTeSyZmcprgNnmvCdVFi6fkEymREp03vMqBxeLv7z88CfP5RtkXpxKzgbpf38xlOK8b1wZCt9JuRLJ5ryucwsmZyaTQSk9u0%2BOpKiqoiJVGplzp9JGVTOZQpGJ1YFk3mcdVhiPGFKWNjIe89rfYyouucWoHEmmqkhJ5mwyEul6BR08dX1Kh6TSWrBgciiYmQupKiORrle013FXBIUDpjhyfmsOGJZDlWExMxjF5klgQLEzGOYxFibdRPcom7mLtBgkA8zxcGCJ78JjDDDTQIZ9SmcWI16wdDDP5SI9hs9urXCmkZCduLBwKaxkrlzrNT4hmVCrtIK5y6liyqiQYdqlbMLbaoFHF6PyVDBYsLm%2B3%2BnYMyptt09hZCVTund8SippUh08%2BvMvM5V%2BLypMkowlYJDymG%2BGuLvfu7bfm4ocOwaMkXiFttYK0U08Gf2VGQtpwSf5G2sCyGRQzW7hWe7irVJg6joxdiYiJB2XN0t9Zv8lmcnUPjKKRSoYSiAY0SwxZU0rAsnkUBSYtFTqJYm2EM3SuhmkrgsgSCCZ7eILbpxgQK%2Bk4vs5ku6B1oAhPaAyaww5mps26cfWOYQgkMx2sZUlddOERUw1g6nZS2wpE3mgADAdQtkP40Rt4UNykykiwbDoiSYDwfQjVQEUMCoYbECHVgueCC5LV9wzESIXr0V5TDQYkEqsQp3a9B4KmA5FR6fVt1GwxcRLEBi5eM19qjAw9HHHRCcRAQYEDMXbwLij8ojPgwSBaXxglB6C6cQvOdpbDwVGXLa26ZCKNZF2o7YtzhblL4xK04SkkhkxtG31JBYSSEwwyiHtaDQSyk%2FdzfDlAkCwLhDYXHOJYDJeATC3Wf4D9FoOEV126JC2wZD6ln8ZDOY3dSDLOshFZNYCJaY9YmNaAYZRiSCjojeol8GktRxmt00jofb3wG%2FRSVtYCANFCNHIhGhmMoORTILJoKY1LGjQD9kPlkGQRkJtOiPmcvkdhhriwmWQCRUwj1AwWl8spM%2BOuXQFNdEoEhM6wtMq%2FWGgcJMJUoOam1AuVC%2F6y9eydE%2BG4QDnIUB7LdoUOwzGObz2UTHIhAk1N8GJhMO1pV9Y0DjJ4BCTtjT1yL0VmBaWYjcxWOkIMikK5dJNKC0mUYf%2BqwOMPgxaA4WjkRaieEMwGhcDCPB00190MikK5NJpjQurYll%2Bnd%2F98PAYI%2FVAoLDKLN0ahW9k%2BHkjNcr9DCBBoYLJ7MmF4hmBXnARdRoetB6YS7uEgty7m6ZlpkCB6SeOf5wUkTAyneWzZe9E3RZ5dtNyQrhoWcoYtjZP%2BGLZLg%2BGBhigjMw4MvCzbHOinoalML2CvnP9iKqtCU%2BVLI4x2nbXfm6dSGw2%2BceeofKCMb3iJzaYgK5jZhNy6oXLChhPtcgTTUlkePjiXvBRQnUUsf6NYjc2wxd%2BvXAAgbdcvdzCFQ4gAyZxtAFWvqW7vj6aBmZaGqhvBH%2FqOMjkotdU%2B%2F8xmVUq%2BNhkJjj192xg4lKJWqtoyWvlMeI3tTXe4WQs528HVQI448cmFlDvZelbIbhmsOyhaV0qa4Mtc41z0YGslHxk3KJTOyKT%2F%2FOvq%2BcQj2ChMxjfNKfodcnf3uDiPgpW1PzgEZkIdbQd%2F%2BZY%2Fvm4bgNzwxcaUPYAuGAzNgY14CtFEHcQnWSSVNfdxwdaFpWk2834CX2YmK8Ii8WDgx50U7UqE0ukuMhskbzbtxGMm0y8osjofdtM99jr4lrXW7nwIdLTyKwhknEF66OZ%2BFjx0dHzyIQ%2BoR0%2BG50VzDPISANXyxH9lxkkxgRwAWswo6RKPIIME%2BXt2jqQyQ6mQI%2Fi8zWYW%2F1GKjMZU6gb6Fwj%2F%2FZW8CcaZjBxt72kFJjSP%2BSJUwqZGHnAvHE6t8jbXqvWaGFUMpNxiaplKG%2Bpz6u4Ekk%2BHRR520tJghFMDiSjtMszPBvBgPXvB0cM0BnBQOPN7jGhkj6Z%2B6SFAPNiHgMkfTLzScXrplaJ6QiPcS6wOtuDt%2BFg7psfr3spMKsCU2nTqK1pbFzO%2Fmx%2FmPnuAKZweozxJ7POqUAujxKzsa9UdPTvtJHdCSRuvGqmIjd86zAjwTh0PjBMN20Eu75NBeNd82vofFAKFjQYjHqXDCZaZwQz94useRSgXGAsf67w%2BWL9Rcgiqj0Sjf%2BnjBgeL9B74xpqRuWzgrkJjwkVnFQRRD4nGK4IMByKIlNmGqxjMEnDwT0U3c%2FduWN%2FfjD%2FAkgNQ8yszwHJAAAAAElFTkSuQmCC'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    

def get_access_token():
    """
    ?????? AK???SK ?????????????????????Access Token???
    :return: access_token?????????None(????????????)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    main()
