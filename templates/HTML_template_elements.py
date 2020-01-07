"""
Templates and functions for making the results HTML file.

SpiceBucks
"""

HEADER = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Arb Time</title>
</head>
<body>
<img src="templates/police.jpg" alt="Don't">'''

FOOTER = '''</body>
</html>'''

def make_div(result):
    ret = "<h1>" + result["Name"] + "</h1> <h2> " + result["Arbitrage Opportunity"] + "</h2> "
    ret += '<h3> <a href="' + result["Link"] + '"> ' + result["Link"] + '</a> </h3> <br />'
    for r in result["Instructions"]:
        ret += "<span> " + r + "<br /> </span> "
    return ret

def make_html(res_list):
    ret = HEADER
    for r in res_list:
        ret += make_div(r)
    ret += FOOTER
    return ret
