import subprocess
import os

current_path = os.getcwd()
print("Current working directory:", f"{current_path}/data/images/images.qrc")

def run_pyrcc5():
    try:
        # Run the pyrcc5 command
        print(f'pyrcc5 {current_path}/data/images/images.qrc -o {current_path}/data/py/images_rc.py')
        subprocess.run(f'pyrcc5 {current_path}/data/images/images.qrc -o {current_path}/data/py/images_rc.py', check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")

if __name__ == "__main__":
    run_pyrcc5()
