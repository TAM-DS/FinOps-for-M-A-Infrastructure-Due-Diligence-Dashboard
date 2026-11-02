import {useEffect,useState} from 'react'
import {BarChart,Bar,XAxis,YAxis,CartesianGrid,Tooltip,ResponsiveContainer,AreaChart,Area,Legend} from 'recharts'
import {ShieldCheck,TriangleAlert,Landmark,RotateCcw,ArrowUpRight} from 'lucide-react'

const money=v=>Number(v).toLocaleString('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0})
const short=v=>{const n=Number(v);return (n<0?'-$':'$')+(Math.abs(n)/1000000).toFixed(2)+'M'}
const tooltip={contentStyle:{background:'#132338',color:'#f3f7ff',border:'1px solid #3c5268',borderRadius:8},formatter:(v)=>money(v)}
function Panel({title,children}){return <section className="panel"><h2>{title}</h2>{children}</section>}
function Slider({title,value,setValue,max=100,step=5}){return <label className="slider"><span>{title} <b>{value}%</b></span><input type="range" min="0" max={max} step={step} value={value} onChange={e=>setValue(+e.target.value)}/></label>}
export default function App(){
 const [capture,setCapture]=useState(100),[rate,setRate]=useState(10),[overrun,setOverrun]=useState(0)
 const [data,setData]=useState(null),[error,setError]=useState(''),[loading,setLoading]=useState(true)
 useEffect(()=>{
  const ctrl=new AbortController()
  setLoading(true)
  fetch('/api/overview?capture_pct='+capture+'&discount_pct='+rate+'&implementation_overrun_pct='+overrun,{signal:ctrl.signal})
   .then(r=>{if(!r.ok)throw new Error('Evidence verification failed');return r.json()})
   .then(json=>{setData(json);setError('');setLoading(false)})
   .catch(err=>{if(err.name!=='AbortError'){setError('Could not load verified data. Start the local FastAPI server.');setLoading(false)}})
  return ()=>ctrl.abort()
 },[capture,rate,overrun])
 const e=data?.evidence,s=data?.scenario
 const providers=(e?.provider_mix||[]).map(p=>({name:p.name,exposed:+p.gross_waste,other:+p.other_spend}))
 const categories=(e?.waste_by_category||[]).map(p=>({name:p.name,amount:+p.amount}))
 const cashflows=(s?.cashflows||[]).filter(x=>x.year>0).map(x=>({year:'Y'+x.year,discounted:+x.discounted}))
 return <div className="shell">
  <aside className="sidebar">
   <div className="brand"><Landmark size={28}/><div><strong>INFRA / DEAL ROOM</strong><small>TRANSACTION ADVISORY</small></div></div>
   <nav><a href="#overview">01 / Executive overview</a><a href="#exposure">02 / Cloud exposure</a><a href="#scenario">03 / Deal economics</a><a href="#controls">04 / Decision controls</a></nav>
   <div className="disclosure"><ShieldCheck size={18}/> Actual consulting engagement. Public figures are synthetic replacements, not client results.</div>
  </aside>
  <main id="overview">
   <header className="topbar"><span>FINANCIAL DUE DILIGENCE / EXECUTIVE INTELLIGENCE</span><span className="status">READ-ONLY MODEL</span></header>
   <div className="content">
    <div className="hero"><p className="eyebrow">INVESTMENT COMMITTEE / DECISION SUPPORT</p><h1>Infrastructure <em>Deal Room.</em></h1><p>What is the cloud exposure, what can actually be captured, and what is the modeled value after execution costs?</p><span className="tag">REAL ENGAGEMENT · SYNTHETIC FINANCIAL RECONSTRUCTION</span></div>
    {error&&<div className="error" role="alert">{error}</div>}
    {!data&&loading&&<p role="status">Validating the synthetic cost evidence…</p>}
    {data&&<>
     <div className="section-title"><h2>The financial picture</h2><span><ShieldCheck size={15}/> Reconciled Python evidence {loading?'· Updating…':''}</span></div>
     <div className="metrics">
      <div><span>Annual cloud run rate</span><strong>{short(e.annual_spend)}</strong><small>Synthetic source evidence</small></div>
      <div><span>Gross waste exposure</span><strong>{short(e.gross_waste)}</strong><small>{e.waste_pct}% of synthetic spend</small></div>
      <div><span>Actionable savings backlog</span><strong>{short(e.actionable_savings)}</strong><small>Modeled, not realized</small></div>
      <div className="featured"><span>Five-year scenario NPV</span><strong>{short(s.five_year_npv)}</strong><small>Assumptions adjustable below</small></div>
     </div>
     <div className="grid" id="exposure">
      <Panel title="Multi-cloud spend vs exposure"><p className="subtext">The exposed portion is included in total spend—not added to it.</p><div className="chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={providers} layout="vertical" margin={{right:20,left:0}}><CartesianGrid stroke="#283c52" strokeDasharray="3 4"/><XAxis type="number" tickFormatter={short} stroke="#91a6bf"/><YAxis type="category" dataKey="name" stroke="#c8d6e5" width={48}/><Tooltip {...tooltip}/><Legend/><Bar dataKey="other" name="Other spend" stackId="a" fill="#4c7194"/><Bar dataKey="exposed" name="Gross waste exposure" stackId="a" fill="#d9ab68"/></BarChart></ResponsiveContainer></div></Panel>
      <Panel title="Waste concentration by category"><p className="subtext">Modeled exposure; not automatically collectible savings.</p><div className="chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={categories} layout="vertical" margin={{right:20,left:5}}><CartesianGrid stroke="#283c52" strokeDasharray="3 4"/><XAxis type="number" tickFormatter={short} stroke="#91a6bf"/><YAxis type="category" dataKey="name" stroke="#c8d6e5" width={100}/><Tooltip {...tooltip}/><Bar dataKey="amount" name="Gross exposure" fill="#67d2c1" radius={[0,5,5,0]}/></BarChart></ResponsiveContainer></div></Panel>
     </div>
     <div className="grid scenario" id="scenario">
      <Panel title="Challenge the deal economics"><p className="subtext">Change assumptions; the backend recomputes the financial scenario without changing source evidence.</p>
       <Slider title="Savings realization" value={capture} setValue={setCapture}/>
       <Slider title="Discount rate" value={rate} setValue={setRate} max={30} step={1}/>
       <Slider title="Implementation cost overrun" value={overrun} setValue={setOverrun}/>
       <button type="button" onClick={()=>{setCapture(100);setRate(10);setOverrun(0)}}><RotateCcw size={15}/> Reset baseline</button>
       <div className="result"><small>MODELED FIVE-YEAR NPV</small><strong>{short(s.five_year_npv)}</strong><p>Not an acquisition valuation or real client outcome.</p></div>
      </Panel>
      <Panel title="Discounted annual benefits"><p className="subtext">Year 1 captures staged implementation; years 2–5 assume full modeled run-rate, adjusted by capture.</p><div className="chart big"><ResponsiveContainer width="100%" height="100%"><AreaChart data={cashflows} margin={{right:16,left:5}}><CartesianGrid stroke="#283c52" strokeDasharray="3 4"/><XAxis dataKey="year" stroke="#91a6bf"/><YAxis tickFormatter={short} stroke="#91a6bf"/><Tooltip {...tooltip}/><Area type="monotone" dataKey="discounted" name="Discounted benefit" stroke="#6bdbca" strokeWidth={3} fill="#6bdbca" fillOpacity={0.16}/></AreaChart></ResponsiveContainer></div><div className="financial-notes"><span>Modeled investment <b>{money(s.implementation_cost)}</b></span><span>Year-1 benefit <b>{money(s.year_one_savings)}</b></span></div></Panel>
     </div>
     <section id="controls"><div className="section-title"><h2>Executive decision controls</h2><span><ShieldCheck size={15}/> Human authority</span></div><div className="control-grid">{data.decision_controls.map(x=><article key={x.title}><TriangleAlert size={20}/><h3>{x.title}</h3><p>{x.detail}</p></article>)}</div>
      <div className="provenance"><ArrowUpRight size={19}/><p><b>Real engagement. Synthetic financial reconstruction.</b> The published {short(e.unbooked_gap)} difference between gross exposure and the modeled remediation backlog is intentionally excluded from savings. No actual client figures, realized savings, or valuation outcomes are presented.</p></div>
     </section>
     <footer>REPRODUCIBLE EVIDENCE · MODELING BOUNDARIES · EXECUTIVE JUDGMENT</footer>
    </>}
   </div>
  </main>
 </div>
}
