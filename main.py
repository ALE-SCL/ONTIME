import os
import subprocess
import sys

def main():
    """Lanzador automático para la app de Streamlit de ON TIME."""
    print("Iniciando ON TIME (Interfaz Web Local)...")
    
    # Ruta al script de Streamlit
    app_path = os.path.join(os.path.dirname(__file__), "app_web.py")
    
    # Comando para lanzar streamlit
    try:
        # Usamos subprocess para llamar a streamlit run app_web.py
        # Esto asegura que se use el ejecutable de streamlit del entorno actual
        subprocess.run(["streamlit", "run", app_path], check=True)
    except KeyboardInterrupt:
        print("\nCerrando aplicación...")
    except Exception as e:
        print(f"\nError al iniciar Streamlit: {e}")
        print("\nIntenta ejecutar manualmente: streamlit run app_web.py")

if __name__ == "__main__":
    main()
