import psutil

class ProgramBlocker:
    def __init__(self):
        self.blocked_apps = []  # Lista para almacenar las aplicaciones bloqueadas

    def enforce_blocking(self):
        """Aplica el bloqueo a las aplicaciones especificadas en blocked_apps."""
        for app in self.blocked_apps:
            for process in psutil.process_iter(attrs=['pid', 'name']):
                if app.lower() in process.info['name'].lower():
                    try:
                        # Terminamos el proceso para bloquearlo
                        process.terminate()
                        print(f"Bloqueando la aplicación: {process.info['name']}")
                    except psutil.NoSuchProcess:
                        pass  # Si el proceso ya no existe, ignoramos

    def release_blocking(self):
        """Libera el bloqueo de las aplicaciones, si es necesario."""
        # En esta implementación, el desbloqueo se puede manejar de varias maneras,
        # dependiendo de cómo desees administrar el desbloqueo.
        # Por ejemplo, podrías reiniciar los procesos bloqueados o simplemente
        # permitir que el usuario los inicie manualmente.
        print("Liberando el bloqueo de aplicaciones...")
        for app in self.blocked_apps:
            print(f"Considera reiniciar {app} si está disponible.")

    def set_blocked_apps(self, apps):
        """Establece la lista de aplicaciones bloqueadas."""
        self.blocked_apps = apps

    def get_blocked_apps(self):
        """Devuelve la lista de aplicaciones bloqueadas."""
        return self.blocked_apps
