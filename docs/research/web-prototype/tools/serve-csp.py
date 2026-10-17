import http.server, sys, os
ROOT=sys.argv[1]; PORT=int(sys.argv[2]); EXTRA=os.environ.get("CSP_EXTRA","")
CSP="default-src 'none'; script-src 'self'; style-src 'self' "+EXTRA+"; img-src 'self'; media-src 'self'; font-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def end_headers(s):
        s.send_header("Content-Security-Policy",CSP); s.send_header("Cache-Control","no-store"); super().end_headers()
    def log_message(s,*a): pass
http.server.ThreadingHTTPServer(("127.0.0.1",PORT),H).serve_forever()
