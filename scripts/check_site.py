#!/usr/bin/env python3
"""Check the public HTML without network requests or third-party dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids=set();self.duplicates=[];self.links=[];self.h1=0;self.title=False;self.description=False;self.viewport=False
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if attrs.get('id'):
            if attrs['id'] in self.ids:self.duplicates.append(attrs['id'])
            self.ids.add(attrs['id'])
        if tag=='h1':self.h1+=1
        if tag=='title':self.title=True
        if tag=='meta':
            self.description |= attrs.get('name')=='description' and bool(attrs.get('content'))
            self.viewport |= attrs.get('name')=='viewport'
        for attr in ('href','src'):
            if attrs.get(attr):self.links.append(attrs[attr])


def check(root=ROOT):
    pages={path:Page(path.read_text(encoding='utf-8')) for path in root.glob('*.html')}
    pages.update({path:Page(path.read_text(encoding='utf-8')) for path in (root/'articles').glob('*.html')})
    errors=[]
    for path,page in pages.items():
        label=str(path.relative_to(root))
        if page.h1!=1:errors.append(f'{label}: expected one H1, found {page.h1}')
        if not all((page.title,page.description,page.viewport)):errors.append(f'{label}: missing title/description/viewport')
        if page.duplicates:errors.append(f'{label}: duplicate IDs {page.duplicates}')
        for link in page.links:
            parsed=urlsplit(link)
            if parsed.scheme or parsed.netloc:continue
            target=(root/unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/') else path.parent/unquote(parsed.path) if parsed.path else path
            target=target.resolve()
            if not target.is_relative_to(root.resolve()):errors.append(f'{label}: out-of-site link {link}')
            elif not target.exists():errors.append(f'{label}: missing target {link}')
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:errors.append(f'{label}: missing anchor {link}')
    if errors:raise ValueError('\n'.join(errors))
    return len(pages)


if __name__=='__main__':
    try:print(f'{check()} pages checked: local links, anchors, headings and metadata OK.')
    except ValueError as error:print(error,file=sys.stderr);raise SystemExit(1)
