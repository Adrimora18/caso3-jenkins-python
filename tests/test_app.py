"""Pruebas unitarias ejecutadas automáticamente con pytest."""

from app import VERSION, health, saludar


def test_saludar_nombre():
    assert "Ana" in saludar("Ana")


def test_saludar_por_defecto():
    assert "mundo" in saludar()


def test_health_estado():
    assert health()["status"] == "ok"


def test_health_version():
    assert health()["version"] == VERSION
