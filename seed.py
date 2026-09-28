"""
Script utilitário para popular a API com dados iniciais de demonstração.
Certifique-se de que a API esteja em execução (ex: python main.py).
"""
import httpx

BASE_URL = "http://127.0.0.1:8000"


def popular():
    print("Conectando à API em", BASE_URL)
    with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
        try:
            res = client.get("/")
            if res.status_code != 200:
                print("Erro: API não respondeu corretamente no endpoint raiz.")
                return
        except Exception as e:
            print("Não foi possível conectar ao servidor. Inicie a API com 'python main.py' primeiro.")
            return

        print("Cadastrando eventos...")
        eventos = [
            {
                "titulo": "Workshop de Python e FastAPI",
                "descricao": "Desenvolvimento prático de microsserviços modernos com Python.",
                "data": "2026-10-15",
                "horario": "14:00",
                "local": "Laboratório de Informática 01",
                "capacidade": 2,
                "categoria": "Workshop"
            },
            {
                "titulo": "Seminário de Inteligência Artificial e LLMs",
                "descricao": "Explorando as fronteiras de modelos de linguagem e agentes autônomos.",
                "data": "2026-10-20",
                "horario": "10:00",
                "local": "Auditório Nobre",
                "capacidade": 80,
                "categoria": "Seminário"
            },
            {
                "titulo": "Minicurso de Git e GitHub para Engenharia",
                "descricao": "Boas práticas de controle de versão e trabalho colaborativo.",
                "data": "2026-10-22",
                "horario": "16:00",
                "local": "Sala 302",
                "capacidade": 25,
                "categoria": "Minicurso"
            }
        ]

        ids_eventos = []
        for ev in eventos:
            r = client.post("/eventos", json=ev)
            if r.status_code == 201:
                evento_criado = r.json()
                ids_eventos.append(evento_criado["id"])
                print(f" -> Evento criado: [ID {evento_criado['id']}] {evento_criado['titulo']}")

        print("\nCadastrando participantes...")
        participantes = [
            {
                "nome": "Ana Beatriz Souza",
                "email": "ana.souza@universidade.edu.br",
                "curso": "Engenharia de Software"
            },
            {
                "nome": "Carlos Eduardo Lima",
                "email": "carlos.lima@universidade.edu.br",
                "curso": "Ciência da Computação"
            },
            {
                "nome": "Mariana Ferreira",
                "email": "mariana.ferreira@universidade.edu.br",
                "curso": "Sistemas de Informação"
            }
        ]

        ids_participantes = []
        for part in participantes:
            r = client.post("/participantes", json=part)
            if r.status_code == 201:
                part_criado = r.json()
                ids_participantes.append(part_criado["id"])
                print(f" -> Participante cadastrado: [ID {part_criado['id']}] {part_criado['nome']}")

        print("\nRealizando inscrições...")
        if ids_eventos and len(ids_participantes) >= 2:
            ev_id = ids_eventos[0]
            # Inscrever participante 1 no evento 1
            r1 = client.post(f"/eventos/{ev_id}/inscricoes/{ids_participantes[0]}")
            print(f" -> Inscrição Participante {ids_participantes[0]} no Evento {ev_id}: {r1.status_code}")

            # Inscrever participante 2 no evento 1 (atingindo capacidade limite = 2)
            r2 = client.post(f"/eventos/{ev_id}/inscricoes/{ids_participantes[1]}")
            print(f" -> Inscrição Participante {ids_participantes[1]} no Evento {ev_id}: {r2.status_code}")

        print("\nDemonstração populada com sucesso! Acesse http://127.0.0.1:8000/docs para explorar.")


if __name__ == "__main__":
    popular()
