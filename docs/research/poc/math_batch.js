// Reads a JSON array of {tex, display} on stdin, writes a JSON array of MathML strings on stdout.
// Needs temml (MIT): npm i temml, or vendor temml.cjs and require it by path.
const temml = require(process.env.TEMML_PATH || 'temml');
let input = '';
process.stdin.on('data', (d) => (input += d));
process.stdin.on('end', () => {
  const out = JSON.parse(input).map(({ tex, display }) => {
    try {
      return temml.renderToString(tex, { displayMode: !!display, throwOnError: true, trust: false, maxExpand: 1000, maxSize: 20 });
    } catch (e) {
      if (process.env.DEBUG) console.error(String(e));
      return null; // caller falls back to escaped source
    }
  });
  process.stdout.write(JSON.stringify(out));
});
