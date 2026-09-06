const API = "http://127.0.0.1:5000/api";
let editingId = null;

function showLogin(){document.getElementById("loginPage").classList.remove("hidden");document.getElementById("registerPage").classList.add("hidden");}
function showRegister(){document.getElementById("loginPage").classList.add("hidden");document.getElementById("registerPage").classList.remove("hidden");}
function showDashboard(){document.getElementById("loginPage").classList.add("hidden");document.getElementById("registerPage").classList.add("hidden");document.getElementById("dashboardPage").classList.remove("hidden");loadPasswords();}

async function register(){
  const body={name:registerName.value,email:registerEmail.value,password:registerPassword.value};
  const r=await fetch(`${API}/register`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
  const d=await r.json(); registerMessage.textContent=d.message||d.error;
  if(r.ok) showLogin();
}
async function login(){
  const r=await fetch(`${API}/login`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:loginEmail.value,password:loginPassword.value})});
  const d=await r.json(); loginMessage.textContent=d.message||d.error;
  if(r.ok){localStorage.setItem("token",d.token);welcome.textContent=`Welcome, ${d.name}`;showDashboard();}
}
function logout(){localStorage.removeItem("token");showLogin();}
async function loadPasswords(){
  const token=localStorage.getItem("token"); if(!token)return;
  const q=encodeURIComponent(search.value||"");
  const r=await fetch(`${API}/passwords?q=${q}`,{headers:{Authorization:`Bearer ${token}`}});
  const d=await r.json();
  passwordList.innerHTML="";
  (d.passwords||[]).forEach(p=>{
    const el=document.createElement("div");el.className="entry";
    el.innerHTML=`<h3>${escapeHtml(p.site)}</h3><p><b>Username:</b> ${escapeHtml(p.username)}</p><p><b>Password:</b> <span id="pw-${p.id}">••••••••</span></p><p>${escapeHtml(p.notes||"")}</p><div class="entry-actions"><button onclick="togglePassword(${p.id})">Show</button><button class="secondary" onclick="editPassword(${p.id})">Edit</button><button class="secondary" onclick="deletePassword(${p.id})">Delete</button></div>`;
    el.dataset.password=p.password;el.dataset.id=p.id;passwordList.appendChild(el);
  });
}
function togglePassword(id){const el=[...document.querySelectorAll(".entry")].find(x=>x.dataset.id==id);const s=document.getElementById(`pw-${id}`);s.textContent=s.textContent==="••••••••"?el.dataset.password:"••••••••";}
function openAddForm(){editingId=null;formTitle.textContent="Add Password";site.value=username.value=vaultPassword.value=notes.value="";passwordForm.classList.remove("hidden");}
function closeForm(){passwordForm.classList.add("hidden");}
async function savePassword(){
  const token=localStorage.getItem("token");
  const body={site:site.value,username:username.value,password:vaultPassword.value,notes:notes.value};
  const url=editingId?`${API}/passwords/${editingId}`:`${API}/passwords`;
  const r=await fetch(url,{method:editingId?"PUT":"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${token}`},body:JSON.stringify(body)});
  const d=await r.json();formMessage.textContent=d.message||d.error;if(r.ok){closeForm();loadPasswords();}
}
async function editPassword(id){
  const r=await fetch(`${API}/passwords/${id}`,{headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}});
  const p=await r.json();editingId=id;formTitle.textContent="Edit Password";site.value=p.site;username.value=p.username;vaultPassword.value=p.password;notes.value=p.notes||"";passwordForm.classList.remove("hidden");
}
async function deletePassword(id){
  if(!confirm("Delete this password?"))return;
  await fetch(`${API}/passwords/${id}`,{method:"DELETE",headers:{Authorization:`Bearer ${localStorage.getItem("token")}`}});
  loadPasswords();
}
function generatePassword(){
  const chars="ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*";
  let out="";for(let i=0;i<18;i++)out+=chars[Math.floor(Math.random()*chars.length)];vaultPassword.value=out;
}
function escapeHtml(v){return String(v).replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[m]));}
if(localStorage.getItem("token"))showDashboard();else showLogin();
