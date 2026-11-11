"""Aplicación mínima para el laboratorio CI/CD de XYZ Solutions."""

VERSION = "1.0.0"


def saludar(nombre="mundo"):
    """Devuelve un mensaje de prueba de la aplicación."""
    return f"Hola, {nombre}. XYZ Solutions está funcionando."


def health():
    """Devuelve un estado de salud legible en JSON."""
    return {"status": "ok", "app": "xyz-solutions", "version": VERSION}
