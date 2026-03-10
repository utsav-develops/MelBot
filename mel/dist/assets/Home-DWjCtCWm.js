import{r as a,u as h,j as e}from"./index-ZxvrT6N3.js";import{l as g,i as y,B as b}from"./webllm-yNbeZAUm.js";function w(){const[o,s]=a.useState(!1),[n,t]=a.useState(!1),[l,c]=a.useState(""),[x,r]=a.useState(null);a.useEffect(()=>{d()},[]);async function d(){if(y()){s(!0);return}t(!0),r(null);try{await g(i=>c(i)),s(!0)}catch(i){r("Failed to load Mel. Make sure you are using Chrome."),console.error(i)}finally{t(!1)}}return{isReady:o,isLoading:n,progress:l,error:x}}const u=["stretching my neurons...","remembering how to be chill...","loading personality... almost there...","warming up the vibes...","untangling some thoughts...","brewing intelligence, no cap...","waking up from a fat nap..."];function N(){const o=h(),{isReady:s,isLoading:n,progress:t,error:l}=w(),[c,x]=a.useState(0),[r,d]=a.useState(0),[i,p]=a.useState(!1);return a.useEffect(()=>{if(!n)return;const m=setInterval(()=>{x(f=>(f+1)%u.length)},2500);return()=>clearInterval(m)},[n]),a.useEffect(()=>{if(!t)return;const m=t.match(/(\d+(\.\d+)?)%/);m&&d(Math.min(Math.round(parseFloat(m[1])),99))},[t]),a.useEffect(()=>{s&&(d(100),setTimeout(()=>p(!0),600),setTimeout(()=>o("/chat"),1200))},[s,o]),e.jsxs("main",{style:{opacity:i?0:1,transition:"opacity 0.6s ease",fontFamily:"'IBM Plex Mono', monospace"},className:"relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-gray-950 px-8",children:[e.jsx("div",{className:"pointer-events-none absolute inset-0",style:{backgroundImage:`
            linear-gradient(rgba(52,211,153,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(52,211,153,0.03) 1px, transparent 1px)
          `,backgroundSize:"40px 40px"}}),e.jsx("div",{className:"pointer-events-none absolute",style:{width:400,height:400,borderRadius:"50%",background:"radial-gradient(circle, rgba(52,211,153,0.06) 0%, transparent 70%)"}}),e.jsx("div",{style:{animation:"floatBot 3s ease-in-out infinite"},children:e.jsx(b,{size:"lg",isThinking:n})}),e.jsx("h1",{className:"mt-8 text-5xl font-bold tracking-widest text-white",style:{letterSpacing:"0.3em",animation:"fadeUp 0.6s ease both"},children:"MEL"}),e.jsx("div",{className:"mt-2 h-5 text-center",style:{animation:"fadeUp 0.6s 0.1s ease both",opacity:0},children:l?e.jsx("p",{className:"text-xs text-red-400",children:l}):s?e.jsx("p",{className:"text-xs tracking-widest text-emerald-400",children:"READY"}):e.jsx("p",{className:"text-xs tracking-wider text-gray-500",style:{animation:"quipFade 0.4s ease both"},children:u[c]},c)}),e.jsxs("div",{className:"mt-10 w-full max-w-xs",style:{animation:"fadeUp 0.6s 0.2s ease both",opacity:0},children:[e.jsx("div",{className:"relative h-px w-full overflow-hidden bg-gray-800",children:e.jsx("div",{className:"absolute top-0 left-0 h-full bg-emerald-400",style:{width:`${r}%`,transition:"width 0.4s ease",boxShadow:"0 0 8px rgba(52,211,153,0.8)"}})}),e.jsxs("div",{className:"mt-3 flex items-center justify-between",children:[e.jsx("p",{className:"max-w-[220px] truncate text-xs text-gray-600",title:t,children:t?t.length>35?t.slice(0,35)+"...":t:"initializing..."}),e.jsxs("p",{className:"ml-4 text-xs text-emerald-400 tabular-nums",children:[r,"%"]})]})]}),n&&r<10&&e.jsxs("p",{className:"mt-8 max-w-xs text-center text-xs leading-relaxed text-gray-700",style:{animation:"fadeUp 0.6s 0.4s ease both",opacity:0},children:["First load downloads the model (~1GB).",e.jsx("br",{}),"After that — instant."]}),e.jsx("style",{children:`
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;700&display=swap');

        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(16px); }
          to   { opacity: 1; transform: translateY(0); }
        }

        @keyframes floatBot {
          0%, 100% { transform: translateY(0px); }
          50%       { transform: translateY(-8px); }
        }

        @keyframes quipFade {
          from { opacity: 0; transform: translateY(4px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `})]})}export{N as default};
