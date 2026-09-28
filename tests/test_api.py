import pytest
from fastapi.testclient import TestClient
from main import app
from database import db

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_dados():
    """Limpa o banco de dados em memória antes de cada teste."""
    db.reset()
    yield
    db.reset()


# ==============================================================================
# TESTES DE EVENTOS
# ==============================================================================

def test_cadastrar_evento_sucesso():
    payload = {
        "titulo": "Semana de Inteligência Artificial",
        "descricao": "Palestras e minicursos sobre as novas tendências de IA.",
        "data": "2026-11-10",
        "horario": "10:00",
        "local": "Auditório Central",
        "capacidade": 50,
        "categoria": "Seminário"
    }
    response = client.post("/eventos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["titulo"] == payload["titulo"]
    assert data["capacidade"] == 50
    assert data["vagas_disponiveis"] == 50
    assert data["total_inscritos"] == 0


def test_cadastrar_evento_dados_invalidos():
    # Título vazio
    res1 = client.post("/eventos", json={
        "titulo": "   ",
        "descricao": "Desc",
        "data": "2026-11-10",
        "horario": "10:00",
        "local": "Auditório",
        "capacidade": 10,
        "categoria": "Palestra"
    })
    assert res1.status_code == 422

    # Capacidade zero ou negativa
    res2 = client.post("/eventos", json={
        "titulo": "Evento Teste",
        "descricao": "Desc",
        "data": "2026-11-10",
        "horario": "10:00",
        "local": "Auditório",
        "capacidade": 0,
        "categoria": "Palestra"
    })
    assert res2.status_code == 422

    # Data inválida (ex: 30 de fevereiro)
    res3 = client.post("/eventos", json={
        "titulo": "Evento Teste",
        "descricao": "Desc",
        "data": "2026-02-30",
        "horario": "10:00",
        "local": "Auditório",
        "capacidade": 10,
        "categoria": "Palestra"
    })
    assert res3.status_code == 422

    # Horário inválido
    res4 = client.post("/eventos", json={
        "titulo": "Evento Teste",
        "descricao": "Desc",
        "data": "2026-11-10",
        "horario": "25:99",
        "local": "Auditório",
        "capacidade": 10,
        "categoria": "Palestra"
    })
    assert res4.status_code == 422


def test_listar_eventos():
    client.post("/eventos", json={
        "titulo": "Workshop de Git",
        "descricao": "Aprenda Git e GitHub na prática.",
        "data": "2026-10-05",
        "horario": "14:00",
        "local": "Laboratório 3",
        "capacidade": 20,
        "categoria": "Workshop"
    })
    client.post("/eventos", json={
        "titulo": "Palestra de Microsserviços",
        "descricao": "Arquitetura distribuída.",
        "data": "2026-10-06",
        "horario": "19:00",
        "local": "Auditório A",
        "capacidade": 100,
        "categoria": "Palestra"
    })

    response = client.get("/eventos")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Filtro por categoria
    resp_filtro = client.get("/eventos?categoria=Workshop")
    assert resp_filtro.status_code == 200
    assert len(resp_filtro.json()) == 1
    assert resp_filtro.json()[0]["categoria"] == "Workshop"


def test_consultar_evento_por_id():
    post_res = client.post("/eventos", json={
        "titulo": "Palestra Inovação",
        "descricao": "Inovação tecnológica.",
        "data": "2026-10-15",
        "horario": "09:00",
        "local": "Auditório",
        "capacidade": 30,
        "categoria": "Palestra"
    })
    evento_id = post_res.json()["id"]

    res_ok = client.get(f"/eventos/{evento_id}")
    assert res_ok.status_code == 200
    assert res_ok.json()["id"] == evento_id

    res_404 = client.get("/eventos/9999")
    assert res_404.status_code == 404
    assert res_404.json()["detail"] == "Evento não encontrado."


def test_atualizar_evento():
    post_res = client.post("/eventos", json={
        "titulo": "Título Antigo",
        "descricao": "Desc Antiga",
        "data": "2026-10-15",
        "horario": "09:00",
        "local": "Sala 1",
        "capacidade": 10,
        "categoria": "Palestra"
    })
    evento_id = post_res.json()["id"]

    put_res = client.put(f"/eventos/{evento_id}", json={
        "titulo": "Título Atualizado",
        "capacidade": 15
    })
    assert put_res.status_code == 200
    assert put_res.json()["titulo"] == "Título Atualizado"
    assert put_res.json()["capacidade"] == 15


def test_excluir_evento():
    post_res = client.post("/eventos", json={
        "titulo": "Para Excluir",
        "descricao": "Desc",
        "data": "2026-10-15",
        "horario": "09:00",
        "local": "Sala 1",
        "capacidade": 10,
        "categoria": "Palestra"
    })
    evento_id = post_res.json()["id"]

    del_res = client.delete(f"/eventos/{evento_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/eventos/{evento_id}")
    assert get_res.status_code == 404


# ==============================================================================
# TESTES DE PARTICIPANTES
# ==============================================================================

def test_cadastrar_participante_sucesso():
    payload = {
        "nome": "Carlos Silva",
        "email": "carlos.silva@universidade.edu.br",
        "curso": "Engenharia de Software"
    }
    response = client.post("/participantes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["nome"] == payload["nome"]
    assert data["email"] == payload["email"]


def test_cadastrar_participante_erros():
    # E-mail inválido
    res1 = client.post("/participantes", json={
        "nome": "Maria",
        "email": "email-invalido",
        "curso": "Ciência da Computação"
    })
    assert res1.status_code == 422

    # Nome vazio
    res2 = client.post("/participantes", json={
        "nome": "   ",
        "email": "maria@universidade.edu.br",
        "curso": "Ciência da Computação"
    })
    assert res2.status_code == 422

    # E-mail duplicado
    client.post("/participantes", json={
        "nome": "Ana",
        "email": "ana@universidade.edu.br",
        "curso": "Design"
    })
    res3 = client.post("/participantes", json={
        "nome": "Outra Ana",
        "email": "ana@universidade.edu.br",
        "curso": "Administração"
    })
    assert res3.status_code == 400
    assert "Já existe um participante cadastrado com este e-mail" in res3.json()["detail"]


def test_listar_e_consultar_participante():
    p1 = client.post("/participantes", json={
        "nome": "Participante 1",
        "email": "p1@teste.com",
        "curso": "Engenharia"
    }).json()

    res_list = client.get("/participantes")
    assert res_list.status_code == 200
    assert len(res_list.json()) == 1

    res_get = client.get(f"/participantes/{p1['id']}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == p1["id"]

    res_404 = client.get("/participantes/9999")
    assert res_404.status_code == 404
    assert res_404.json()["detail"] == "Participante não encontrado."


def test_atualizar_e_excluir_participante():
    p = client.post("/participantes", json={
        "nome": "Original",
        "email": "orig@teste.com",
        "curso": "Física"
    }).json()

    # Atualizar
    put_res = client.put(f"/participantes/{p['id']}", json={"nome": "Modificado"})
    assert put_res.status_code == 200
    assert put_res.json()["nome"] == "Modificado"

    # Excluir
    del_res = client.delete(f"/participantes/{p['id']}")
    assert del_res.status_code == 204

    assert client.get(f"/participantes/{p['id']}").status_code == 404


# ==============================================================================
# TESTES DE INSCRIÇÕES E REGRAS DE NEGÓCIO
# ==============================================================================

def test_fluxo_inscricao_e_regras_de_negocio():
    # Cadastra evento com capacidade para 1 pessoa
    evento = client.post("/eventos", json={
        "titulo": "Minicurso Rápido",
        "descricao": "Vagas limitadas a 1 pessoa.",
        "data": "2026-10-30",
        "horario": "08:00",
        "local": "Lab 1",
        "capacidade": 1,
        "categoria": "Minicurso"
    }).json()
    evento_id = evento["id"]

    # Cadastra dois participantes
    p1 = client.post("/participantes", json={
        "nome": "Alice",
        "email": "alice@teste.com",
        "curso": "Engenharia de Software"
    }).json()

    p2 = client.post("/participantes", json={
        "nome": "Bob",
        "email": "bob@teste.com",
        "curso": "Sistemas de Informação"
    }).json()

    # 1. Regra: Se evento não existe
    res_evento_inexistente = client.post(f"/eventos/9999/inscricoes/{p1['id']}")
    assert res_evento_inexistente.status_code == 404
    assert res_evento_inexistente.json()["detail"] == "Evento não encontrado."

    # 2. Regra: Se participante não existe
    res_participante_inexistente = client.post(f"/eventos/{evento_id}/inscricoes/9999")
    assert res_participante_inexistente.status_code == 404
    assert res_participante_inexistente.json()["detail"] == "Participante não encontrado."

    # 3. Inscrição do primeiro participante (Sucesso)
    res_inscricao = client.post(f"/eventos/{evento_id}/inscricoes/{p1['id']}")
    assert res_inscricao.status_code == 201
    assert res_inscricao.json()["evento_id"] == evento_id
    assert res_inscricao.json()["participante_id"] == p1["id"]

    # Verifica se as vagas diminuíram
    evento_atualizado = client.get(f"/eventos/{evento_id}").json()
    assert evento_atualizado["vagas_disponiveis"] == 0
    assert evento_atualizado["total_inscritos"] == 1

    # 4. Regra: Participante já inscrito
    res_duplicado = client.post(f"/eventos/{evento_id}/inscricoes/{p1['id']}")
    assert res_duplicado.status_code == 400
    assert res_duplicado.json()["detail"] == "Participante já está inscrito neste evento."

    # 5. Regra: Evento sem vagas disponíveis (Bob tenta se inscrever mas capacidade era 1)
    res_sem_vagas = client.post(f"/eventos/{evento_id}/inscricoes/{p2['id']}")
    assert res_sem_vagas.status_code == 400
    assert res_sem_vagas.json()["detail"] == "Não existem vagas disponíveis para este evento."

    # 6. Consultar participantes inscritos no evento
    res_listar_inscritos = client.get(f"/eventos/{evento_id}/inscricoes")
    assert res_listar_inscritos.status_code == 200
    inscritos = res_listar_inscritos.json()
    assert len(inscritos) == 1
    assert inscritos[0]["participante"]["nome"] == "Alice"

    # 7. Cancelar inscrição de Alice
    res_cancelar = client.delete(f"/eventos/{evento_id}/inscricoes/{p1['id']}")
    assert res_cancelar.status_code == 204

    # Agora deve ter vaga disponível novamente e Bob consegue se inscrever
    res_bob_inscricao = client.post(f"/eventos/{evento_id}/inscricoes/{p2['id']}")
    assert res_bob_inscricao.status_code == 201

    # Nova consulta de inscritos mostra Bob
    inscritos_apos = client.get(f"/eventos/{evento_id}/inscricoes").json()
    assert len(inscritos_apos) == 1
    assert inscritos_apos[0]["participante"]["nome"] == "Bob"
