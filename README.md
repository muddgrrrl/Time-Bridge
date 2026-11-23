<p align="center">
  <img src="readme-banner.png" width="920" alt="Time Bridge. One instant across time zones · 14:30  Chicago · Same instant in three cities.">
</p>

# Time Bridge

Convert a timestamp to several time zones in one command. Ambiguous times during a fall clock change require an explicit choice, and nonexistent spring-forward times produce an error.

## At a glance

| Task | How |
| --- | --- |
| **Convert across time zones** | Pass a timestamp and one or more target IANA zones. |
| **Interpret a local time** | Use `--from` when the input has no offset. |
| **Resolve a repeated hour** | Use `--fold 0` or `--fold 1` when clocks fall back. |

## Quick start

```sh
python3 time_bridge.py 2026-11-23T14:30 Europe/London Asia/Tokyo --from America/Chicago
python3 time_bridge.py 2026-11-01T01:30 UTC --from America/Chicago --fold 1
```

Requires Python 3.9+ and an installed IANA time-zone database, standard on macOS and most Linux systems. A timestamp with no offset or source zone is interpreted as UTC. [MIT](LICENSE)
