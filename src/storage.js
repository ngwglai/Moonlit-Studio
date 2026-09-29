(function(global){
'use strict';
class ProjectStore{
 constructor(){this.db=null;this.queue=Promise.resolve();}
 async open(){if(!global.indexedDB)throw Error('浏览器不支持项目自动保存，请使用 Chrome / Edge');this.db=await new Promise((res,rej)=>{const r=indexedDB.open('moonlit-studio-v1',1);r.onupgradeneeded=()=>{r.result.createObjectStore('projects',{keyPath:'id'});const b=r.result.createObjectStore('backups',{keyPath:'id'});b.createIndex('projectId','projectId');};r.onsuccess=()=>res(r.result);r.onerror=()=>rej(r.error);r.onblocked=()=>rej(Error('请关闭其他编辑器窗口后重试'));});return this;}
 async list(){return this.request('projects','readonly',s=>s.getAll()).then(a=>a.sort((a,b)=>b.updatedAt-a.updatedAt));}
 request(name,mode,action){return new Promise((res,rej)=>{if(!this.db){rej(Error('自动保存不可用'));return;}const tx=this.db.transaction(name,mode);const req=action(tx.objectStore(name));let value;req.onsuccess=()=>{value=req.result;};tx.oncomplete=()=>res(value);tx.onerror=()=>rej(tx.error||req.error);tx.onabort=()=>rej(tx.error||Error('保存中断'));});}
 save(p){const data=GalCore.clone(p);data.updatedAt=Date.now();const run=()=>this.request('projects','readwrite',s=>s.put(data));const result=this.queue.then(run,run);this.queue=result.catch(()=>{});return result;}
 async remove(id){await this.request('projects','readwrite',s=>s.delete(id));const backups=await this.backups(id);for(const b of backups)await this.request('backups','readwrite',s=>s.delete(b.id));}
 async backup(p){const record={id:GalCore.uid('backup'),projectId:p.id,time:Date.now(),project:GalCore.clone(p)};await this.request('backups','readwrite',s=>s.put(record));const list=await this.backups(p.id);for(const x of list.slice(8))await this.request('backups','readwrite',s=>s.delete(x.id));return record;}
 async backups(id){const all=await this.request('backups','readonly',s=>s.index('projectId').getAll(id));return all.sort((a,b)=>b.time-a.time);}
}
global.ProjectStore=ProjectStore;
})(window);
