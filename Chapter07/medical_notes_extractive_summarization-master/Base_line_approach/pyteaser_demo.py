from pyteaser import SummarizeUrl
url = 'http://mtsamples.com/site/pages/sample.asp?Type=6-Cardiovascular%20/%20Pulmonary&Sample=901-Angina'
summaries = SummarizeUrl(url)
for i in range(len(summaries)):
    print summaries[i]
