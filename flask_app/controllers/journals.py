from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import journal,user # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create Journals Controller
@app.post('/journal/entry')
def journal_entry_process():
    if 'user_id' not in session: return redirect('/')
    if not journal.Journal.journal_validations(request.form): return redirect('/journal/entry')
    journal.Journal.create_journal(request.form)
    return redirect(f'/journal/{session['user_id']}')

# Read Journals Controller

@app.route('/journal/entry')
def journal_entry_page():
    if 'user_id' not in session: return redirect('/')
    prompt = journal.Journal.get_all_prompts_for_journal()
    return render_template('journal_entry.html', prompt = prompt)

@app.route('/journal/<int:id>')
def journal_page(id):
    if 'user_id' not in session: return redirect('/')
    users_journals = journal.Journal.get_users_journal_entries(id)
    return render_template('journal.html', journals = users_journals)


@app.route('/view/entry/<int:id>')
def view_entry(id):
    if 'user_id' not in session: return redirect('/')
    this_entry = journal.Journal.get_journal_by_id(id)
    return render_template('view_entry.html', entry = this_entry)




# Update Journals Controller

@app.get('/edit/entry/<int:id>')
def edit_entry_page(id):
    if 'user_id' not in session: return redirect('/')
    this_entry = journal.Journal.get_journal_by_id(id)
    return render_template('edit_entry.html', entry = this_entry)

@app.post('/edit/entry/<int:id>')
def edit_entry_process(id):
    if 'user_id' not in session: return redirect('/')
    if not journal.Journal.journal_validations(request.form): return redirect(f'/edit/entry/{id}')
    print(request.form)
    journal.Journal.edit_entry(request.form)
    return redirect(f'/journal/{session["user_id"]}')





# Delete Journals Controller
@app.route('/journals/delete/<int:id>')
def delete_entry(id):
    if 'user_id' not in session: return redirect('/')
    journal.Journal.delete_entry(id)
    return redirect(f'/journal/{session['user_id']}')

# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.