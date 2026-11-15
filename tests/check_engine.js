const fs=require('fs');
const h=fs.readFileSync(process.argv[2],'utf8');
const eng=h.slice(h.indexOf('// MONEY-ENGINE-START'), h.indexOf('// MONEY-ENGINE-END'));
const computePaise = new Function(eng + '; return computePaise;')();
const cases=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));
let bad=0, ex=[];
for (const c of cases) {
  const m = computePaise(c);
  const got=[m.interest,m.subtotal,m.after,m.total].map(Number);
  if (got.join()!==c.exp.join()) { bad++; if (ex.length<5) ex.push(JSON.stringify({c, got})); }
}
console.log(`mismatches: ${bad} / ${cases.length}`); console.log(ex.join('\n'));
