"""Tiny serializer for WordPress core block markup (static blocks), matching core's save() output.

Used by tools/build_patterns.py. Attribute JSON is escaped the way WordPress does it ('--' -> \\u002d\\u002d etc.)."""
import json

IMG = "<?php echo esc_url( get_theme_file_uri( 'assets/images/{f}' ) ); ?>"


def _attrs(a):
    if not a:
        return ''
    s = json.dumps(a, separators=(',', ':'), ensure_ascii=False)
    # Same escaping as WordPress serializeAttributes() / serialize_block_attributes().
    s = s.replace('--', '\\u002d\\u002d').replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    return ' ' + s


def _cls(*parts):
    return ' '.join(p for p in parts if p)


def _color_classes(a):
    out = []
    if a.get('textColor'):
        out.append(f"has-{a['textColor']}-color")
    if a.get('backgroundColor'):
        out.append(f"has-{a['backgroundColor']}-background-color")
    if a.get('textColor'):
        out.append('has-text-color')
    if a.get('backgroundColor'):
        out.append('has-background')
    return out


def wrap(name, attrs, open_tag, inner, close_tag):
    return f'<!-- wp:{name}{_attrs(attrs)} -->\n{open_tag}{inner}{close_tag}\n<!-- /wp:{name} -->'


def join(*blocks):
    return '\n\n'.join(b for b in blocks if b)


def group(*children, cls='', align='', tag='div', layout='constrained', anchor='', bg='', text='', grid=None):
    a = {}
    if tag != 'div':
        a['tagName'] = tag
    if anchor:
        a['anchor'] = anchor
    if align:
        a['align'] = align
    if cls:
        a['className'] = cls
    if bg:
        a['backgroundColor'] = bg
    if text:
        a['textColor'] = text
    if grid:
        a['layout'] = {'type': 'grid', 'minimumColumnWidth': grid}
    elif layout == 'constrained':
        a['layout'] = {'type': 'constrained'}
    elif layout == 'flex':
        a['layout'] = {'type': 'flex', 'flexWrap': 'wrap'}
    # 'flow' => no layout attr
    classes = _cls('wp-block-group', f'align{align}' if align else '', cls, *_color_classes(a))
    idattr = f' id="{anchor}"' if anchor else ''
    return wrap('group', a, f'<{tag}{idattr} class="{classes}">', join(*children), f'</{tag}>')


def heading(text, level=2, cls='', anchor=''):
    a = {}
    if level != 2:
        a['level'] = level
    if anchor:
        a['anchor'] = anchor
    if cls:
        a['className'] = cls
    idattr = f' id="{anchor}"' if anchor else ''
    return wrap('heading', a, f'<h{level} class="{_cls("wp-block-heading", cls)}"{idattr}>', text, f'</h{level}>')


def para(text, cls=''):
    a = {'className': cls} if cls else {}
    open_tag = f'<p class="{cls}">' if cls else '<p>'
    return wrap('paragraph', a, open_tag, text, '</p>')


def eyebrow(text):
    return para(text, 'sb-eyebrow')


def lead(text):
    return para(text, 'sb-lead')


def ul(items, cls=''):
    a = {'className': cls} if cls else {}
    lis = '\n\n'.join(f'<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->' for i in items)
    return wrap('list', a, f'<ul class="{_cls("wp-block-list", cls)}">', lis, '</ul>')


def buttons(*btns, cls=''):
    """btns: (label, url) or (label, url, 'outline')."""
    inner = []
    for b in btns:
        label, url = b[0], b[1]
        outline = len(b) > 2 and b[2] == 'outline'
        a = {'className': 'is-style-outline'} if outline else {}
        inner.append(wrap('button', a, f'<div class="{_cls("wp-block-button", "is-style-outline" if outline else "")}">',
                          f'<a class="wp-block-button__link wp-element-button" href="{url}">{label}</a>', '</div>'))
    a = {'className': cls} if cls else {}
    return wrap('buttons', a, f'<div class="{_cls("wp-block-buttons", cls)}">', join(*inner), '</div>')


def image(file, alt, cls=''):
    a = {'sizeSlug': 'full', 'linkDestination': 'none'}
    if cls:
        a['className'] = cls
    src = IMG.format(f=file)
    return wrap('image', a, f'<figure class="{_cls("wp-block-image size-full", cls)}">', f'<img src="{src}" alt="{alt}"/>', '</figure>')


def columns(*cols, cls='', align='wide', center=False):
    a = {}
    if center:
        a['verticalAlignment'] = 'center'
    if align:
        a['align'] = align
    if cls:
        a['className'] = cls
    classes = _cls('wp-block-columns', 'are-vertically-aligned-center' if center else '', f'align{align}' if align else '', cls)
    return wrap('columns', a, f'<div class="{classes}">', join(*cols), '</div>')


def column(*children, width='', cls='', center=False):
    a = {}
    if center:
        a['verticalAlignment'] = 'center'
    if width:
        a['width'] = width
    if cls:
        a['className'] = cls
    classes = _cls('wp-block-column', 'is-vertically-aligned-center' if center else '', cls)
    style = f' style="flex-basis:{width}"' if width else ''
    return wrap('column', a, f'<div class="{classes}"{style}>', join(*children), '</div>')


def details(q, a_html):
    body = join(*[para(p) for p in (a_html if isinstance(a_html, list) else [a_html])])
    return wrap('details', {}, '<details class="wp-block-details">', f'<summary>{q}</summary>{body}', '</details>')


def table(head, rows, cls='sb-table'):
    th = ''.join(f'<th>{h}</th>' for h in head)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return wrap('table', {'className': cls}, f'<figure class="{_cls("wp-block-table", cls)}">',
                f'<table class="has-fixed-layout"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>', '</figure>')


def shortcode(sc):
    return f'<!-- wp:shortcode -->\n{sc}\n<!-- /wp:shortcode -->'


def query_posts(n=3):
    return ('<!-- wp:query {"queryId":2,"query":{"perPage":%d,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","inherit":false},"align":"wide","className":"sb-posts sb-posts--home"} -->\n'
            '<div class="wp-block-query alignwide sb-posts sb-posts--home"><!-- wp:post-template {"layout":{"type":"grid","columnCount":3}} -->\n'
            '<!-- wp:group {"className":"sb-post-card","layout":{"type":"constrained"}} -->\n'
            '<div class="wp-block-group sb-post-card"><!-- wp:post-featured-image {"isLink":true,"aspectRatio":"16/9"} /-->\n\n<!-- wp:post-terms {"term":"category","className":"sb-post-card__cat"} /-->\n\n'
            '<!-- wp:post-title {"level":3,"isLink":true} /-->\n\n<!-- wp:post-excerpt {"excerptLength":22} /-->\n\n'
            '<!-- wp:post-date {"className":"sb-post-card__date"} /--></div>\n<!-- /wp:group -->\n<!-- /wp:post-template --></div>\n<!-- /wp:query -->') % n
