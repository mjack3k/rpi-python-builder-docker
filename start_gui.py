import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import subprocess
import os
import paramiko
import shutil

PYTHON_VER = "3.13.1"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class FormField(tk.Frame):
    def __init__(self, parent, label_text):
        super().__init__(parent)
        self.label = tk.Label(self, text=label_text)
        self.label.pack(side=tk.LEFT, padx=5, pady=5)
        self.entry = tk.Entry(self)
        self.entry.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.X, expand=True)
    
    def get_value(self):
        return self.entry.get()

class StatusCheck(tk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.text_label = tk.Label(self, text=text, anchor=tk.W)
        self.text_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5, anchor=tk.W)
        self.status_label = tk.Label(self, text="✗", anchor=tk.E)
        self.status_label.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5, pady=5)
    
    def set(self, status):
        self.status_label.config(text="✓" if status else "❌")

class ProgressModal(tk.Toplevel):
    def __init__(self, parent, title="Progress"):
        super().__init__(parent)
        self.title(title)
        self.label = tk.Label(self, text="Processing...")
        self.label.pack(pady=10)
        self.progress = ttk.Progressbar(self, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=10)
        self.progress.start()

    def update_status(self, message):
        self.label.config(text=message)

    def stop(self):
        self.progress.stop()
        self.destroy()

class PythonBuilderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.init_gui()
        self.title("Python Builder for RPI")
        self.after(1000, self.check_everything)

    def init_gui(self):
        # Top title
        self.title_label = tk.Label(self, text="Python Builder", font=("Helvetica", 24, "bold"))
        self.title_label.pack(side=tk.TOP, fill=tk.X, expand=False)

        # Main content - two frames next to each other
        self.left_side = tk.Frame(self)
        self.left_side.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)
        self.right_side = tk.Frame(self)
        self.right_side.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # LEFT SIDE
        self.howto_frame = tk.Frame(self.left_side)
        self.howto_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        self.howto_title = tk.Label(self.howto_frame, text="How to use", font=('Helvetica', 14))
        self.howto_title.pack(side=tk.TOP, fill=tk.X, expand=True)

        steps = [
            '1. *On windows: Enable WSL2',
            '2. Install docker',
            '3. Download this repo',
            '4. Click "Build"',
            '5. Enter your RPI details',
            '6. Click "Install"'
        ]

        for step in steps:
            step_label = tk.Label(self.howto_frame, text=step, anchor=tk.W)
            step_label.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=True)

        # RIGHT SIDE
        self.work_frame = tk.Frame(self.right_side)
        self.work_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Target RPI
        self.target_rpi_frame = tk.Frame(self.work_frame)
        self.target_rpi_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.form_title = tk.Label(self.target_rpi_frame, text="Target Raspberry Pi", font=("Helvetica", 16, "bold"))
        self.form_title.pack(pady=10)
        
        self.username_field = FormField(self.target_rpi_frame, "Username:")
        self.username_field.pack(anchor='w', fill=tk.X, expand=True)
        
        self.host_field = FormField(self.target_rpi_frame, "Host:")
        self.host_field.pack(anchor='w', fill=tk.X, expand=True)

        # Action
        self.action_frame = tk.Frame(self.work_frame)
        self.action_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.button_build_docker = tk.Button(self.action_frame, text="Build Docker", command=self.on_build_docker_click)
        self.button_build_docker.pack(fill=tk.BOTH, expand=True)
        self.button_build = tk.Button(self.action_frame, text="Build Python", command=self.on_build_click)
        self.button_build.pack(fill=tk.BOTH, expand=True)

        

        self.button_install = tk.Button(self.action_frame, text="Install Python", command=self.on_install_click)
        self.button_install.pack(fill=tk.BOTH, expand=True)
        
        # checks
        self.check_frame = tk.Frame(self.right_side, highlightthickness=1, highlightcolor='black')
        self.check_frame.pack(pady=10, anchor='w', fill=tk.X, expand=True)
        
        self.checks_title = tk.Label(self.check_frame, text="Status", font=("Helvetica", 16, "bold"))
        self.checks_title.pack(side=tk.TOP, expand=True, fill=tk.X)

        self.docker_check = StatusCheck(self.check_frame, text="Docker Available:")
        self.docker_check.pack(fill=tk.X, expand=True, anchor=tk.W)
        
        self.image_check = StatusCheck(self.check_frame, text="Docker Image Available:")
        self.image_check.pack(fill=tk.X, expand=True, anchor=tk.W)
        
        self.python_check = StatusCheck(self.check_frame, text="Python Produced:")
        self.python_check.pack(fill=tk.X, expand=True, anchor=tk.W)
        
    
    def on_build_docker_click(self):
        cmd = ['bash', f'{os.path.join(ROOT_DIR, "build_docker.sh")}']
        self.run_long_process("Building docker image", command=cmd)
    
    def on_build_click(self):
        cmd = ['bash', f'{os.path.join(ROOT_DIR, "run_docker.sh")}']
        self.run_long_process("Building python", command=cmd)

    def on_install_click(self):
        self.compress_and_copy()

    def check_everything(self):
        self.docker_check.set(self.check_docker())
        self.image_check.set(self.check_image())
        self.python_check.set(self.check_python())
        self.after(5000, self.check_everything)
    
    def check_docker(self):
        cmd = ['docker', '-v']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout:
            if 'Docker version' in result.stdout.decode('utf-8'):
                return True
        return False
    
    def check_image(self):
        docker_image_name = 'rpi-python-builder'
        result = subprocess.run(['docker', 'images', '-q', docker_image_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout:
            return True
        return False

    def check_python(self):
        if os.path.exists(os.path.join(ROOT_DIR, 'out', f'PYTHON_{PYTHON_VER}')):
            return True
        return False
    
    def run_long_process(self, message, command):
        modal = ProgressModal(self, title=message)
        self.after(100, self.execute_process, modal, command)
    
    def execute_process(self, modal, command):
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            modal.update_status("Completed" if result.returncode == 0 else "Failed")
        except Exception as e:
            modal.update_status(f"Error: {str(e)}")
        finally:
            self.after(2000, modal.stop)

    def compress_and_copy(self):
        source_dir = os.path.join(ROOT_DIR, 'out', f'PYTHON_{PYTHON_VER}')
        compressed_file = os.path.join(ROOT_DIR, 'out', f'PYTHON_{PYTHON_VER}.tar.gz')

        # Compress the directory
        shutil.make_archive(compressed_file.replace('.tar.gz', ''), 'gztar', source_dir)

        # Read username and host from entry fields
        username = self.username_field.get_value()
        host = self.host_field.get_value()

        # Prompt for the password
        password = simpledialog.askstring("Password", "Enter your password:", show='*')


        # Define the remote path
        remote_path = f'/home/{username}/PYTHON_{PYTHON_VER}.tar.gz'

        # Copy the compressed file via SCP using Paramiko
        try:
            # Create an SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connect to the host
            ssh.connect(host, username=username, password=password)
            password = ''
            # Use SCP to copy the file
            sftp = ssh.open_sftp()
            sftp.put(compressed_file, remote_path)
            sftp.close()
            
            # Close the SSH connection
            ssh.close()
            
            print(f"File {compressed_file} successfully copied to {remote_path}")
        except Exception as e:
            print(f"Failed to copy file: {str(e)}")

if __name__ == "__main__":
    app = PythonBuilderApp()
    app.mainloop()