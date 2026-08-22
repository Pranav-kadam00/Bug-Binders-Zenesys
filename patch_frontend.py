import os

app_path = r'artifacts/aqura/src/App.tsx'
with open(app_path, 'r', encoding='utf-8') as f:
    app_code = f.read()

# Add useUser and auth setup
auth_setup = """import { ErrorBoundary } from "@/components/error-boundary";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/not-found";
import "./index.css";

import { setAuthTokenGetter } from "@workspace/api-client-react";
setAuthTokenGetter(() => localStorage.getItem("aqura_token") || "");
function useUser() {
  try { return JSON.parse(localStorage.getItem("aqura_user") || "null"); } catch { return null; }
}

const queryClient = new QueryClient();"""
app_code = app_code.replace(
    'import { ErrorBoundary } from "@/components/error-boundary";\nimport { Toaster } from "@/components/ui/toaster";\nimport { TooltipProvider } from "@/components/ui/tooltip";\nimport NotFound from "@/pages/not-found";\nimport "./index.css";\n\nconst queryClient = new QueryClient();',
    auth_setup
)

# Update Shell
shell_old = """function Shell({ children }: { children: ReactNode }) {
  const [location, setLocation] = useLocation(); const [open, setOpen] = useState(false);
  const title = nav.find((n) => location.startsWith(n.href))?.label ?? (location.includes("decision-twin") ? "Decision Twin" : location.includes("comparison") ? "Vendor comparison" : "Workspace");
  return <div className="aqura-noise min-h-[100dvh] bg-background">
    <aside className={`fixed inset-y-0 left-0 z-40 flex w-[252px] flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground transition-transform lg:translate-x-0 ${open ? "translate-x-0" : "-translate-x-full"}`}>
      <div className="flex h-20 items-center border-b border-sidebar-border px-6"><Logo light /></div>
      <div className="px-4 pt-7"><p className="px-3 text-[10px] font-bold uppercase tracking-[.18em] text-sidebar-foreground/45">Workspace</p><nav className="mt-3 space-y-1">{nav.map(({ href, label, icon: Icon }) => <Link key={href} href={href} data-testid={`link-nav-${label.toLowerCase().replaceAll(" ", "-")}`} className={`group flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13px] font-medium ${location.startsWith(href) ? "bg-sidebar-accent text-sidebar-accent-foreground" : "text-sidebar-foreground/70 hover:bg-sidebar-accent/70 hover:text-sidebar-foreground"}`}><Icon size={16} strokeWidth={location.startsWith(href) ? 2.2 : 1.7} /><span>{label}</span>{href === "/approvals" && <span className="ml-auto rounded-full bg-accent px-1.5 py-0.5 text-[10px] font-bold text-accent-foreground">4</span>}</Link>)}</nav></div>
      <div className="mt-auto space-y-1 border-t border-sidebar-border p-4"><Link href="/notifications" data-testid="link-nav-notifications" className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13px] text-sidebar-foreground/70 hover:bg-sidebar-accent"><Bell size={16} /><span>Notifications</span><span className="ml-auto h-2 w-2 rounded-full bg-accent" /></Link><Link href="/settings" data-testid="link-nav-settings" className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13px] text-sidebar-foreground/70 hover:bg-sidebar-accent"><Settings2 size={16} /><span>Settings</span></Link><div className="mt-3 flex items-center gap-3 rounded-lg bg-sidebar-accent/60 px-3 py-3"><div className="grid h-8 w-8 place-items-center rounded-full bg-primary text-xs font-bold text-primary-foreground">MC</div><div className="min-w-0 flex-1"><p className="truncate text-xs font-semibold text-sidebar-foreground">Maya Chen</p><p className="truncate text-[11px] text-sidebar-foreground/50">Procurement lead</p></div><ChevronDown size={14} className="text-sidebar-foreground/45" /></div></div>
    </aside>
    {open && <button aria-label="Close menu" data-testid="button-close-menu" className="fixed inset-0 z-30 bg-foreground/20 lg:hidden" onClick={() => setOpen(false)} />}
    <div className="lg:pl-[252px]"><header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b border-border/80 bg-background/90 px-5 backdrop-blur-md lg:px-10"><div className="flex items-center gap-3"><button onClick={() => setOpen(true)} data-testid="button-open-menu" className="rounded-lg p-2 hover:bg-muted lg:hidden"><Menu size={19} /></button><div><p className="text-[11px] font-medium uppercase tracking-[.16em] text-muted-foreground">AQURA / {title}</p><div className="mt-1 h-1 w-8 rounded-full bg-primary" /></div></div><div className="flex items-center gap-2"><Link href="/notifications" data-testid="link-header-notifications" className="relative rounded-lg p-2.5 text-muted-foreground hover:bg-muted hover:text-foreground"><Bell size={18} /><span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-accent" /></Link><div className="hidden h-7 w-px bg-border sm:block" /><div className="hidden items-center gap-2 sm:flex"><div className="grid h-8 w-8 place-items-center rounded-full bg-primary/15 text-xs font-bold text-primary">MC</div><span className="text-sm font-medium">Maya Chen</span></div></div></header><main className="min-h-[calc(100dvh-5rem)]">{children}</main></div>
  </div>;
}"""

shell_new = """function Shell({ children }: { children: ReactNode }) {
  const [location, setLocation] = useLocation(); const [open, setOpen] = useState(false);
  const user = useUser();
  const role = user?.role || "employee";
  const name = user?.name || "Aarav Mehta";
  const initials = name.split(" ").map((n: string) => n[0]).join("").substring(0, 2).toUpperCase();
  const roleDisplay = role === "procurement_manager" ? "Procurement Manager" : role === "approver" ? "Approver" : role === "admin" ? "Admin" : "Employee";

  const title = nav.find((n) => location.startsWith(n.href))?.label ?? (location.includes("decision-twin") ? "Decision Twin" : location.includes("comparison") ? "Vendor comparison" : "Workspace");
  
  let visibleNav = nav;
  if (role === "employee") {
    visibleNav = nav.filter(n => ["Purchase requests", "Order tracking"].includes(n.label));
  } else if (role === "approver") {
    visibleNav = nav.filter(n => ["Purchase requests", "Approvals", "Purchase orders", "Order tracking"].includes(n.label));
  } else if (role === "procurement_manager") {
    visibleNav = nav.filter(n => n.label !== "Settings");
  }

  return <div className="aqura-noise min-h-[100dvh] bg-background">
    <aside className={`fixed inset-y-0 left-0 z-40 flex w-[252px] flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground transition-transform lg:translate-x-0 ${open ? "translate-x-0" : "-translate-x-full"}`}>
      <div className="flex h-20 items-center border-b border-sidebar-border px-6"><Logo light /></div>
      <div className="px-4 pt-7"><p className="px-3 text-[10px] font-bold uppercase tracking-[.18em] text-sidebar-foreground/45">Workspace</p><nav className="mt-3 space-y-1">{visibleNav.map(({ href, label, icon: Icon }) => <Link key={href} href={href} data-testid={`link-nav-${label.toLowerCase().replaceAll(" ", "-")}`} className={`group flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13px] font-medium ${location.startsWith(href) ? "bg-sidebar-accent text-sidebar-accent-foreground" : "text-sidebar-foreground/70 hover:bg-sidebar-accent/70 hover:text-sidebar-foreground"}`}><Icon size={16} strokeWidth={location.startsWith(href) ? 2.2 : 1.7} /><span>{label}</span>{href === "/approvals" && <span className="ml-auto rounded-full bg-accent px-1.5 py-0.5 text-[10px] font-bold text-accent-foreground">4</span>}</Link>)}</nav></div>
      <div className="mt-auto space-y-1 border-t border-sidebar-border p-4"><Link href="/notifications" data-testid="link-nav-notifications" className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13px] text-sidebar-foreground/70 hover:bg-sidebar-accent"><Bell size={16} /><span>Notifications</span><span className="ml-auto h-2 w-2 rounded-full bg-accent" /></Link><button onClick={() => { localStorage.removeItem("aqura_token"); localStorage.removeItem("aqura_user"); window.location.href = "/login"; }} className="w-full flex items-center gap-3 rounded-lg px-3 py-2.5 text-[13px] text-sidebar-foreground/70 hover:bg-sidebar-accent"><Settings2 size={16} /><span>Sign out</span></button><div className="mt-3 flex items-center gap-3 rounded-lg bg-sidebar-accent/60 px-3 py-3"><div className="grid h-8 w-8 place-items-center rounded-full bg-primary text-xs font-bold text-primary-foreground">{initials}</div><div className="min-w-0 flex-1"><p className="truncate text-xs font-semibold text-sidebar-foreground">{name}</p><p className="truncate text-[11px] text-sidebar-foreground/50">{roleDisplay}</p></div><ChevronDown size={14} className="text-sidebar-foreground/45" /></div></div>
    </aside>
    {open && <button aria-label="Close menu" data-testid="button-close-menu" className="fixed inset-0 z-30 bg-foreground/20 lg:hidden" onClick={() => setOpen(false)} />}
    <div className="lg:pl-[252px]"><header className="sticky top-0 z-20 flex h-20 items-center justify-between border-b border-border/80 bg-background/90 px-5 backdrop-blur-md lg:px-10"><div className="flex items-center gap-3"><button onClick={() => setOpen(true)} data-testid="button-open-menu" className="rounded-lg p-2 hover:bg-muted lg:hidden"><Menu size={19} /></button><div><p className="text-[11px] font-medium uppercase tracking-[.16em] text-muted-foreground">AQURA / {title}</p><div className="mt-1 h-1 w-8 rounded-full bg-primary" /></div></div><div className="flex items-center gap-2"><Link href="/notifications" data-testid="link-header-notifications" className="relative rounded-lg p-2.5 text-muted-foreground hover:bg-muted hover:text-foreground"><Bell size={18} /><span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-accent" /></Link><div className="hidden h-7 w-px bg-border sm:block" /><div className="hidden items-center gap-2 sm:flex"><div className="grid h-8 w-8 place-items-center rounded-full bg-primary/15 text-xs font-bold text-primary">{initials}</div><span className="text-sm font-medium">{name}</span></div></div></header><main className="min-h-[calc(100dvh-5rem)]">{children}</main></div>
  </div>;
}"""
app_code = app_code.replace(shell_old, shell_new)

# Update Auth
auth_old = """<form className="mt-9 space-y-5" onSubmit={(e) => { e.preventDefault(); if (mode === "login") setLocation("/dashboard"); else setSent(true); }}><div><label className="mb-2 block text-xs font-bold text-foreground">Work email</label><input required type="email" placeholder="you@company.com" data-testid="input-auth-email" className="h-12 w-full rounded-lg border border-input bg-card px-4 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/15" /></div>"""
auth_new = """<form className="mt-9 space-y-5" onSubmit={async (e) => { e.preventDefault(); if (mode === "login") { const email = (e.target as any).elements[0].value; const pass = (e.target as any).elements[1].value; const fd = new URLSearchParams(); fd.append("username", email); fd.append("password", pass); const r = await fetch("http://localhost:8000/api/v1/auth/login", { method: "POST", body: fd }); if (r.ok) { const d = await r.json(); localStorage.setItem("aqura_token", d.access_token); localStorage.setItem("aqura_user", JSON.stringify(d.user)); window.location.href = "/dashboard"; } else { alert("Invalid email or password"); } } else setSent(true); }}><div><label className="mb-2 block text-xs font-bold text-foreground">Work email</label><input required type="email" placeholder="maya@aqura.demo" data-testid="input-auth-email" className="h-12 w-full rounded-lg border border-input bg-card px-4 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/15" /></div>"""
app_code = app_code.replace(auth_old, auth_new)

# Protect detail pages buttons
# Vendor Comparison Link in RequestDetail
comp_old = """<Link href={`/vendor-comparison/${r.id}`} data-testid="link-request-comparison" className="rounded-lg bg-primary px-4 py-2 text-xs font-bold text-primary-foreground">Compare vendors <ArrowRight className="ml-1 inline" size={14}/></Link>"""
comp_new = """{(useUser()?.role === "procurement_manager" || useUser()?.role === "admin") && <Link href={`/vendor-comparison/${r.id}`} data-testid="link-request-comparison" className="rounded-lg bg-primary px-4 py-2 text-xs font-bold text-primary-foreground">Compare vendors <ArrowRight className="ml-1 inline" size={14}/></Link>}"""
app_code = app_code.replace(comp_old, comp_new)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_code)

print("Updated App.tsx")
