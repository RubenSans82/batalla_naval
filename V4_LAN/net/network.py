import socket
import threading

HOST_SERVER = "0.0.0.0"
HOST_CLIENT = "192.168.100.201"
PORT = 5000


class NetThread(threading.Thread):
    def __init__(self, game, on_result, on_sunk, on_gameover, role):
        super().__init__(daemon=True)
        self.game = game
        self.on_result = on_result
        self.on_sunk = on_sunk
        self.on_gameover = on_gameover
        self.role = role
        self.sock = None

    def run(self):
        # -------------------------
        # Conexión
        # -------------------------
        if self.role == "server":
            s = socket.socket()
            s.bind((HOST_SERVER, PORT))
            s.listen(1)
            print("Esperando cliente...")
            conn, addr = s.accept()
            print("Cliente conectado:", addr)
            self.sock = conn
        else:
            s = socket.socket()
            print("Conectando al servidor...")
            s.connect((HOST_CLIENT, PORT))
            print("Conectado.")
            self.sock = s

        f = self.sock.makefile("rwb", buffering=0)

        # -------------------------
        # Bucle de recepción
        # -------------------------
        while True:
            line = f.readline()
            if not line:
                break

            parts = line.decode().strip().split()

            # -------------------------
            # SHOT r c
            # -------------------------
            if parts[0] == "SHOT":
                r = int(parts[1])
                c = int(parts[2])

                hit, sunk_ship = self.game.receive_enemy_shot(r, c)

                # RESULT
                msg = f"RESULT {r} {c} {'HIT' if hit else 'MISS'}\n".encode()
                self.sock.sendall(msg)

                # SUNK con todas las coordenadas
                if sunk_ship:
                    flat = []
                    for rr, cc in sunk_ship:
                        flat.append(str(rr))
                        flat.append(str(cc))
                    msg = "SUNK " + str(len(sunk_ship)) + " " + " ".join(flat) + "\n"
                    self.sock.sendall(msg.encode())

                # GAMEOVER
                if self.game.game_over:
                    self.sock.sendall(b"GAMEOVER\n")

            # -------------------------
            # RESULT r c HIT/MISS
            # -------------------------
            elif parts[0] == "RESULT":
                r = int(parts[1])
                c = int(parts[2])
                hit = (parts[3] == "HIT")
                self.on_result(r, c, hit)

            # -------------------------
            # SUNK n r1 c1 r2 c2 ...
            # -------------------------
            elif parts[0] == "SUNK":
                n = int(parts[1])
                coords = []
                idx = 2
                for _ in range(n):
                    rr = int(parts[idx])
                    cc = int(parts[idx+1])
                    coords.append((rr, cc))
                    idx += 2
                self.on_sunk(coords)

            # -------------------------
            # GAMEOVER
            # -------------------------
            elif parts[0] == "GAMEOVER":
                self.on_gameover()

    # -------------------------
    # Enviar SHOT
    # -------------------------
    def send_shot(self, r, c):
        msg = f"SHOT {r} {c}\n".encode()
        self.sock.sendall(msg)