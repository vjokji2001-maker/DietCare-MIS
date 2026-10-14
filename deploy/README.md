# Hosting under /diet/

Vite assets and BrowserRouter use `/diet/`. The entry URL `/diet?token=...`
also works; the app reads the authentication query before clearing it.
Plain `python3 -m http.server` does not provide subpath mounting or SPA fallback.
Use the included server for entry URLs and nested-route refreshes.

Windows PowerShell, from the project directory:

```powershell
npm run build
scp -r ./dist root@192.168.1.194:/root/
scp ./deploy/serve.py root@192.168.1.194:/root/dietcare-serve.py
scp ./deploy/dietcare.service root@192.168.1.194:/root/dietcare.service
ssh root@192.168.1.194
```

On the Linux server with systemd:

```bash
systemctl stop dietcare
cp /root/dietcare.service /etc/systemd/system/dietcare.service
systemctl daemon-reload
systemctl enable --now dietcare
systemctl status dietcare --no-pager
curl -I http://127.0.0.1:8081/diet
curl -I http://127.0.0.1:8081/diet/patients
```

If port 8081 is occupied by a manually started Python server, stop that
process before starting the service. Check failures with
`journalctl -u dietcare -n 30 --no-pager`.

Future frontend updates only need a new build and dist upload.
For development, use the `/diet/` URL shown by `npm run dev`.
