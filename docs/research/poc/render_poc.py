"""Proof of concept: Markdown -> sanitised HTML with server-side math and trusted markup swapped in after sanitising."""
import html, re, secrets
import markdown
import nh3
from markdown.extensions.wikilinks import WikiLinkExtension
from math_poc import tex_to_mathml

MATH = re.compile(r'\\{1,2}\((.+?)\\{1,2}\)|\\{1,2}\[(.+?)\\{1,2}\]', re.S)  # MMD uses \\( \\) and \\[ \\]

def render(src, allowed_tags, allowed_attrs):
    nonce = secrets.token_hex(6)
    formulas = []

    def stash(m):  # math is hidden from Markdown and the sanitiser behind inert text tokens
        formulas.append({'tex': (m.group(1) or m.group(2)).strip(), 'display': m.group(2) is not None})
        return f'SPAKRMATH{nonce}X{len(formulas) - 1}X'

    src = MATH.sub(stash, src)
    body = markdown.markdown(src, extensions=['tables', 'footnotes', 'def_list', 'abbr', 'attr_list', 'toc', 'sane_lists',
        WikiLinkExtension(base_url='/wiki/', end_url='', build_url=lambda label, base, end: base + re.sub(r'\W+', '-', label.lower()).strip('-'))])
    clean = nh3.Cleaner(tags=allowed_tags, attributes=allowed_attrs, url_schemes={'http', 'https', 'mailto'},
                        link_rel='noopener noreferrer nofollow', strip_comments=True).clean(body)
    if formulas:
        for i, f in enumerate(formulas):
            ml = tex_to_mathml(f['tex'], f['display']) or f'<code class="math-error">{html.escape(f["tex"])}</code>'
            clean = clean.replace(f'SPAKRMATH{nonce}X{i}X', ml)
    return clean

if __name__ == '__main__':
    tags = {'p', 'em', 'strong', 'a', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'h1', 'h2', 'h3', 'sup', 'sub', 'abbr',
            'dl', 'dt', 'dd', 'code', 'pre', 'blockquote', 'div', 'span', 'hr', 'br', 'section', 'ol'}
    attrs = {'a': {'href', 'title'}, 'abbr': {'title'}, 'th': {'align'}, 'td': {'align'}, '*': {'id', 'class'}}
    print(render(open('sample.md').read(), tags, attrs))
