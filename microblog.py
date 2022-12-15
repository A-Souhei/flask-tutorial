from app import app, db
from app.models import User, Post

from app import cli # for custom cli (Important)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post} # Important to return the db, User and Post objects
    # run: flask shell
    # run: db.create_all()
    # run: User.query.all()
    # run: User.query.filter_by(username='john').first()
    # run: u = User(username = 'john', email = 'john@some.mail'
    # run: db.session.add(u)
    # run: db.session.commit()



