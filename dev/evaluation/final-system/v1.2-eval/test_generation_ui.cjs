const assert=require('node:assert/strict');
const {generateWithOneRepair}=require('./web/generation.js');
(async()=>{
 let s={session:{approval:null}},calls=[],messages=[];
 await generateWithOneRepair(async action=>{calls.push(action);s={session:{approval:{},generation_progress:{status:'raci_failed',raci_attempts:1}}};if(calls.length===2)s={session:{approval:{},documents:{}}};return true;},()=>s,m=>messages.push(m));
 assert.deepEqual(calls,['approve_generate','generate']);assert.equal(messages.length,1);
 s={session:{approval:{}}};calls=[];
 await generateWithOneRepair(async a=>{calls.push(a);s={session:{approval:{},documents:{}}};return true;},()=>s,()=>{});assert.equal(calls.length,1);
 s={session:{approval:{}}};calls=[];
 await generateWithOneRepair(async a=>{calls.push(a);s={session:{approval:{},generation_progress:{status:'raci_failed',raci_attempts:calls.length}}};return true;},()=>s,()=>{});assert.equal(calls.length,2);
 await generateWithOneRepair(async()=>{throw Error('Third attempt must not run');},()=>s,()=>{});
 s={session:{approval:null}};calls=[];
 await generateWithOneRepair(async a=>{calls.push(a);return false;},()=>s,()=>{});assert.equal(calls.length,1);
 console.log('4 generation UI scenarios passed; no API calls.');
})().catch(e=>{console.error(e);process.exitCode=1;});
