from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.Model):
    """Board game."""

    __tablename__ = "games"
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100))


def connect_to_db(app, db_uri="postgresql:///games"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""

    ladies = Game(name="Ladies and Gentlemen", description="Team based boardgame where you play to earn money to buy outfits.")
    splendor = Game(name="Splendor", description="Card based where you try to accumulate gems before others")
    uno = Game(name="Uno", description="Card game where you match your hand to cards before everyone else.")

    db.session.add_all([ladies, splendor, uno])
    db.session.commit()

if __name__ == '__main__':
    from server import app

    connect_to_db(app)
    print "Connected to DB."
