import nh3, bleach, time  # pip install nh3 bleach markdown; run from this directory
vec = {
 'script': '<script>alert(1)</script>x',
 'img-onerror': '<img src=x onerror=alert(1)>',
 'js-href': '<a href="javascript:alert(1)">a</a>',
 'js-href-ws': '<a href="  jav&#x09;ascript:alert(1)">a</a>',
 'data-href': '<a href="data:text/html;base64,PHNjcmlwdD4=">a</a>',
 'svg-onload': '<svg onload=alert(1)><circle/></svg>',
 'style-attr': '<span style="background:url(javascript:alert(1))">s</span>',
 'style-tag': '<style>@import "x";</style>t',
 'iframe': '<iframe src="//evil"></iframe>',
 'form': '<form action=//evil><input name=x></form>',
 'math-xlink': '<math><mi xlink:href="javascript:alert(1)">x</mi></math>',
 'mathml-mglyph': '<math><mglyph><style><!--</style><img title="--&gt;&lt;img src=1 onerror=alert(1)&gt;">',
 'noscript-mxss': '<noscript><p title="</noscript><img src=x onerror=alert(1)>">',
 'comment': '<!--[if IE]><script>x</script><![endif]-->c',
 'nested-bad': '<scr<script>ipt>alert(1)</scr</script>ipt>',
 'target-blank': '<a href="https://example.com" target="_blank">ext</a>',
 'meta-refresh': '<meta http-equiv="refresh" content="0;url=//evil">',
 'base': '<base href="//evil">',
 'link': '<link rel=stylesheet href=//evil>',
 'class': '<span class="x" id="y" data-a="1">c</span>',
 'allowed-sup': 'H<sub>2</sub>O and E=mc<sup>2</sup> <u>u</u> <abbr title="t">A</abbr>',
 'img-src-js': '<img src="javascript:alert(1)">',
 'a-no-rel': '<a href="//evil.example/x">proto-relative</a>',
}
tags={'sup','sub','u','abbr','a','img','table','thead','tbody','tr','td','th','p','em','strong','ul','ol','li','code','pre','blockquote','h1','h2','h3','span','div','br','hr','dl','dt','dd'}
attrs={'a':{'href','title'},'abbr':{'title'},'img':{'src','alt','title'},'td':{'align'},'th':{'align'},'*':{'id','class'}}
cl=nh3.Cleaner(tags=tags,attributes=attrs,url_schemes={'http','https','mailto'},link_rel='noopener noreferrer nofollow',strip_comments=True,clean_content_tags={'script','style'})
for k,v in vec.items():
    a=cl.clean(v)
    b=bleach.clean(v,tags=tags,attributes=attrs,protocols=['http','https','mailto'],strip=True,strip_comments=True)
    print(f"{k:14} nh3: {a!r:70}\n{'':14} bleach: {b!r}")
big=open('sample.md').read()*30
import markdown
h=markdown.markdown(big)
t=time.perf_counter();[cl.clean(h) for _ in range(50)];n=(time.perf_counter()-t)/50*1000
t=time.perf_counter();[bleach.clean(h,tags=tags,attributes=attrs,strip=True) for _ in range(50)];b=(time.perf_counter()-t)/50*1000
print(f'html bytes {len(h)}: nh3 {n:.2f} ms, bleach {b:.2f} ms')
