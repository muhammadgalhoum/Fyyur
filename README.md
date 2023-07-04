# Fyyur

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and booking of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

## Tech Stack (Dependencies)

### Backend Dependencies

Our tech stack will include the following:

* **virtualenv** as a tool to create isolated Python environments.
* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations

You can download and install the dependencies mentioned above using `pip` as:

```bash
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

## Development Setup

```text
git clone https://github.com/muhammadgalhoum/Fyyur 
```

* **Create an empty repository in your Github account online. To change the remote repository path in your local repository, use the commands below:**

```git
git remote -v 
git remote remove origin 
git remote add origin <https://github.com/<USERNAME>/<REPO_NAME>.git>
git branch -M master
```

Once you have finished editing your code, you can push the local repository to your Github account using the following commands.

```git
git add . --all   
git commit -m "your comment"
git push -u origin master
```

* **Initialize and activate a virtualenv using:**

```python
python -m virtualenv env
.\env\Scripts\activate
```

* **Install the dependencies:**

```bash
pip install -r requirements.txt
```

* **Run the development server:**

```bash
set FLASK_APP=app.py
set  FLASK_ENV=development # enables debug mode
set  FLASK_DEBUG=true
flask run
```

* **Verify on the Browser**

Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
