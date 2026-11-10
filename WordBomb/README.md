# Word Bomb — SE239 Week 6 + Week 8

This is the **networking milestone prototype**, not the complete game. It demonstrates a TCP client/server exchange, simultaneous clients, unique usernames, and a basic lobby status command.

## Run in VS Code

1. Open this folder in VS Code. Python 3 is required; no extra packages.
2. Open a terminal and run `python3 server.py` (on Windows, use `python server.py`).
3. Open **three more terminals**, and run `python3 client.py` in each.
4. Enter a different username in each client: `sara`, `alanoud`, `deema`.
5. Leave all three clients connected. Type `LIST` in one client to see the connected usernames. Type `QUIT` to disconnect.

For different laptops on the same network, change `HOST` in `client.py` from `127.0.0.1` to the server laptop's LAN IP. Ensure the network permits device-to-device connections and TCP port 5050 is allowed.

## Evidence to capture

- **Week 6:** Server running and one client exchanging `JOIN|sara` / `WELCOME|sara`.
- **Week 8:** Server plus three clients connected at the same time; each receives `WELCOME|username`. Show `LIST` output if helpful.
- **GitHub:** Shared repository URL and commits by each team member.

Submit the actual screenshots/demo and GitHub link to Moodle. One teammate submits, listing all names:

- Sarah Almoqhim — 202502039
- Alanoud Alnasser — 202501269
- Sarah Alhezaimi — 202501568
- Deema Aldawood — 202501812

The server intentionally does **not** yet implement matchmaking or the complete word game; those belong to later milestones.
