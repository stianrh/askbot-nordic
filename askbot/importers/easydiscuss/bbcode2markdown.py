from __future__ import unicode_literals

import re

def convert(bbcode):
    markdown = bbcode
    markdown = re.sub(r'\[b\](.+?)\[/b\]', lambda x: r'**%s**' % x.group(1).strip(), markdown)
    markdown = re.sub(r'\[i\](.+?)\[/i\]', lambda x: r'*%s*' % x.group(1).strip(), markdown)
    markdown = re.sub(r'\[u\](.+?)\[/u\]', lambda x: r'<u>%s</u>' % x.group(1).strip(), markdown)
    markdown = re.sub(r'\[s\](.+?)\[/s\]', lambda x: r'<del>%s</del>' % x.group(1).strip(), markdown)
    markdown = re.sub(r'\[url\](.+?)\[/url\]', lambda x: r'[%s]' % x.group(1).strip(), markdown)
    markdown = re.sub(r'\[url=?(.*?)\](.+?)\[/url\]', r'[\g<2>](\g<1>)', markdown, flags=re.DOTALL)
    markdown = re.sub(r'\[img\](.+?)\[/img\]', r'!(\g<1>)[\g<1>]\n', markdown)

    markdown = re.sub(r'\[quote.*?\](.+?)\[/quote\]', r'> \g<1>\n', markdown)
    bb_codes = re.findall(r'\[quote.*?\].*?\[/quote\]', markdown, flags=re.DOTALL)
    for bb_code in bb_codes:
        cleaned = re.sub(r'\[quote.*?\](.+?)\[/quote\]', r'\g<1>', bb_code, flags=re.DOTALL)
        lines = cleaned.split('\n')
        lines = ['>    %s' % line.strip() for line in lines]
        markdown = markdown.replace(bb_code, '\n'.join(lines))

    markdown = re.sub(r'\[code.*?\](.+?)\[/code\]', r'    \g<1>\n', markdown)

    bb_codes = re.findall(r'\[code.*?\].*?\[/code\]', markdown, flags=re.DOTALL)
    for bb_code in bb_codes:
        cleaned = re.sub(r'\[code.*?\](.+?)\[/code\]', r'\g<1>', bb_code, flags=re.DOTALL)
        lines = cleaned.split('\n')
        lines = ['    %s' % line.rstrip() for line in lines]
        markdown = markdown.replace(bb_code, '\n'.join(lines))

    bb_lists = re.findall(r'\[list\].*?\[/list\]', markdown, flags=re.DOTALL)
    for bb_list in bb_lists:
        items = re.findall(r'\[\*\](.*)[\n\s]+?', bb_list)
        items = ['- %s' % item for item in items]
        markdown = markdown.replace(bb_list, '\n'.join(items))

    # tables not implemented

    return markdown

def test():
    bbcode = '''
[b]bolded text[/b]
[i]italicized text[/i]
[u]underlined text[/u]
[s]strikethrough text[/s]
[url]http://example.org[/url]
[url=http://example.com]Example[/url]
[img]http://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Go-home.svg/100px-Go-home.svg.png[/img]

[quote]quoted text[/quote]

[quote]
quoted text
[/quote]

[quote="author"]quoted text[/quote]

[code]monospaced text[/code]

[code type="something"]monospaced text[/code]

[code]
monospaced text
over several lines
[/code]

[list] [*]Entry 1 [/list]

[list]
[*]Entry 1
[*]Entry 2
[/list]
    '''
    markdown = convert(bbcode)
    print markdown
