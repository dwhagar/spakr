"""Pure-Python math for the proof of concept: latex2mathml (MIT) behind guards. No Node.

latex2mathml does not report errors, so the output is checked and a formula is rejected (shown as TeX source by the
caller) when it contains an unknown command, a raw ampersand token or a link.
"""
import re
import latex2mathml.converter

MAX_TEX = 2000
BAD_OUTPUT = re.compile(r'<mi>\\|<mi>&</mi>|href=|javascript', re.I)
ALIGNED = re.compile(r'\\(begin|end)\{(aligned|align\*?)\}')


def tex_to_mathml(tex: str, display: bool = False):
    """Return MathML, or None when the formula must be shown as TeX source."""
    if len(tex) > MAX_TEX:
        return None
    tex = ALIGNED.sub(lambda m: r'\begin{array}{rl}' if m.group(1) == 'begin' else r'\end{array}', tex)
    try:
        out = latex2mathml.converter.convert(tex, display='block' if display else 'inline')
    except Exception:  # RecursionError, KeyError and friends on unsupported input
        return None
    return None if BAD_OUTPUT.search(out) else out
