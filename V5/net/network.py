import socket
import threading


class NetThread(threading.Thread):
    def __init__(self, game, on_result, on_sunk, on_gameover, role, server_ip="127.0.0.1"):
        super().__init__()
        self.game = game
        self.on_result = on_result
        self.on_sunk = on_sunk
        self.on_gameover = on_gameover
        self.role = role
        self.server_ip = server_ip

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.settimeout(0.5)  # evita bloqueos eternos en recv()
        self.running = True

    # ---------------------------------------------------------
    #  DETENER HILO Y CERRAR SOCKET
    # ---------------------------------------------------------
    def stop(self):
        self.running = False
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            self.sock.close()
        except:
            pass

    # ---------------------------------------------------------
    #  ENVÍO DE MENSAJES
    # ---------------------------------------------------------
    def send(self, msg):
        try:
            self.sock.sendall((msg + "\n").encode("utf-8"))
        except:
            self.running = False

    def send_shot(self, r, c):
        self.send(f"SHOT {r} {c}")

    def send_result(self, r, c, hit):
        self.send(f"RESULT {r} {c} {1 if hit else 0}")

    def send_sunk(self, coords):
        flat = " ".join(f"{r} {c}" for (r, c) in coords)
        self.send(f"SUNK {len(coords)} {flat}")

    def send_gameover(self):
        self.send("GAMEOVER")

    # ---------------------------------------------------------
    #  HILO PRINCIPAL DE RED
    # ---------------------------------------------------------
    def run(self):
        if self.role == "server":
            self.run_server()
        else:
            self.run_client()

    # ---------------------------------------------------------
    #  MODO SERVIDOR
    # ---------------------------------------------------------
    def run_server(self):
        self.sock.bind(("0.0.0.0", 5000))
        self.sock.listen(1)
        print("Esperando cliente...")

        # IMPORTANTE: NO usar timeout antes de accept()

        conn, addr = self.sock.accept()
        print("Cliente conectado:", addr)

        # Ahora sí ponemos timeout en la conexión activa

        conn.settimeout(0.5)
        self.sock = conn

        self.listen_loop()

    # ---------------------------------------------------------
    #  MODO CLIENTE
    # ---------------------------------------------------------
    def run_client(self):
        print(f"Conectando al servidor {self.server_ip}:5000 ...")
        self.sock.connect((self.server_ip, 5000))
        self.sock.settimeout(0.5)
        print("Conectado al servidor.")
        self.listen_loop()

    # ---------------------------------------------------------
    #  BUCLE DE RECEPCIÓN
    # ---------------------------------------------------------
    def listen_loop(self):
        buffer = ""

        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break

                buffer += data.decode("utf-8")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    self.process_message(line.strip())

            except socket.timeout:
                continue  # permite comprobar self.running periódicamente
            except:
                break

        self.running = False
        try:
            self.sock.close()
        except:
            pass

    # ---------------------------------------------------------
    #  PROCESAMIENTO DE MENSAJES
    # ---------------------------------------------------------
    def process_message(self, msg):
        parts = msg.split()

        if not parts:
            return

        cmd = parts[0]

        if cmd == "SHOT":
            r = int(parts[1])
            c = int(parts[2])

            hit, sunk = self.game.receive_enemy_shot(r, c)

            self.send_result(r, c, hit)

            if sunk:
                self.send_sunk(sunk)

            if self.game.game_over:
                self.send_gameover()

        elif cmd == "RESULT":
            r = int(parts[1])
            c = int(parts[2])
            hit = parts[3] == "1"
            self.on_result(r, c, hit)

        elif cmd == "SUNK":
            n = int(parts[1])
            coords = []
            idx = 2
            for _ in range(n):
                r = int(parts[idx])
                c = int(parts[idx + 1])
                coords.append((r, c))
                idx += 2
            self.on_sunk(coords)

        elif cmd == "GAMEOVER":
            self.on_gameover()
            self.running = False