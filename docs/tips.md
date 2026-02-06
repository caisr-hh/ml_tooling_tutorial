# Tips

Optional conveniences and common bumps. None of this is required to run the examples.

## Make targets

If you have make available, the repo may include convenience targets.

Type `make` to see the list of available targets and their descriptions.

Note: Many make targets assume a Linux-like shell. On Windows, prefer WSL2.

## Port forwarding over SSH

If you run services on a remote machine but want to open the UI locally, use SSH local port forwarding.
Replace `<remote-host>` with a host from your `~/.ssh/config`.

```bash
ssh -L 5000:127.0.0.1:5000 <remote-host>  # MLflow UI
ssh -L 8080:127.0.0.1:8080 <remote-host>  # Optuna dashboard
```

Both:

```bash
ssh -L 5000:127.0.0.1:5000 -L 8080:127.0.0.1:8080 <remote-host>

```bash
Detached after auth:

```bash
ssh -fN -L 5000:127.0.0.1:5000 -L 8080:127.0.0.1:8080 <remote-host>
```

## Common bumps

* "Address already in use" (ports 5000/8080):
    - Pick a different port, and keep your service command, config, and smoke test consistent.
* Corporate endpoint tools can block localhost servers (often on Windows):
    - Try different ports, or run inside WSL.
