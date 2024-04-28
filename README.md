# Project Installation Guide

This guide will walk you through the process of cloning a Django project from GitHub, setting up a virtual environment, installing dependencies, and running the project on your local machine. The instructions are provided for both Windows and macOS.

## Prerequisites

Before you begin, make sure you have the following installed:
- Python (3.8 or higher)
- pip (Python package manager)
- Git

## Step 1: Cloning the Repository

First, clone the repository from GitHub to your local machine. Open your terminal (Command Prompt for Windows, Terminal for macOS) and run the following command:

- اضغطت علي الكود وخد الرابط كوبي وحطه في ال visual studio نسخ واكتب قبله git clone
![alt text](<Screen Shot 2024-04-29 at 2.11.00 AM.png>)

```bash
git clone https://github.com/your-username/your-project-name.git
```

Replace `https://github.com/your-username/your-project-name.git` with the URL of your GitHub repository.

## Step 2: Setting Up a Virtual Environment

Navigate to the project directory:
- شغل المشروع من ال visual studio وافتح ال terminal

```bash
cd your-project-name
```

### For Windows

Create a virtual environment by running:

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
.\venv\Scripts\activate
```

### For macOS

Create a virtual environment by running:

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

## Step 3: Installing Dependencies

With the virtual environment activated, install the project dependencies by running:

```bash
pip install -r requirements.txt
```

This command installs all the packages listed in the `requirements.txt` file, which is typically included in the root of your Django project repository.

## Step 4: Running the Django Server

Before running the server, you may need to apply migrations and create a superuser to access the admin panel (optional but recommended).

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a superuser account.

Finally, start the Django development server:

```bash
python manage.py runserver
```

This command starts a local web server running on `http://127.0.0.1:8000/`.

You can now open a web browser and visit `http://127.0.0.1:8000/` to see the project running locally.