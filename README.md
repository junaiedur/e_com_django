# E Commerce Project

### Setup E Commerce Project

1. Create/Activate Python's Virtual Environment.
2. Install/Check Python's packages using pip.
3. Create/Check Database. We're using MySQL.
4. Run Django.
5. After finishing, deactivate Django.

---

### Virtual Environment

- Create Virtual Environment:

```sh
python -m venv venv_ecom
```

- Activate Virtual Environment from **Command Prompt**:
```sh
venv_ecom\Scripts\activate
```

- Activate Virtual Environment from **Git Bash**:
```sh
source venv_ecom\Scripts\activate
```

- Activate Virtual Environment from **PowerShell**:
```sh
.\venv_ecom\Scripts\Activate.ps1
```
> [!TIP]
> From **Windows Setings** go to **Update & Security** > **For Developers** >  **PowerShell** > Click **Apply** . 
> Without this setting, you can't activate python's virtual environment from **PowerShell**.
> ![Click Apply For PowerShell Settings](/static/powershell_script_run_permission.JPG)

- **Deactivate** Virtual Environment from **Command Prompt/PowerShell/Git Bash**:

```sh
deactivate
```

---

### Python Package

- Install all packages(from python virtual environment) for project: `pip install -r requirements.txt` </br>
- After installing new packages, delete `requirements.txt`. To add all the packages into the `requirements.txt` use:
```sh
pip freeze > requirements.txt
```

---

### Database

- Check Database. We're using MySQL Here. Database Name: `e_com`
- Create new **admin account** from **Command Prompt**: 
```sh
python manage.py createsuperuser
```
- After Creating a new super user(admin) account, migrate the database:
```sh
python manage.py migrate
```

---

### Run Django

- Run Django Server:
```sh
python manage.py runserver
```
- Stop Django Server, press `Ctrl+C` </br>
:+1: Deactivate Python Virtual Environment: `deactivate` </br>