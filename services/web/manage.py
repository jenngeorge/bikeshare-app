import unittest
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import Station, StationHistory

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
	db.drop_all()
	db.create_all()
	db.session.commit()

@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(Station(id='24', station_name='Best Station', available_docks=10,
                                   total_docks=35, latitude=40.741895, longitude=-73.989308,
                                   status_value='In Service', status_key=1,
                                   available_bikes=24, st_address_1='995 Pacific St',
                                   st_address_2='', city='', postal_code='11215',
                                   location='', altitude='', test_station=False,
                                   last_communication_time='2018-07-12 06:51:58 PM'))
    db.session.commit()

if __name__ == '__main__':
    cli()
