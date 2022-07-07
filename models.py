def create_classes(db):
    class Patient(db.Model):
        __tablename__ = 'sitepatients'

        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(30))
        last_name = db.Column(db.String(30))
        covidcl = db.Column(db.Integer)
        age = db.Column(db.Date)
        gender = db.Column(db.Integer)
        pregnant = db.Column(db.Integer)
        pneumonia = db.Column(db.Integer)
        diabetes = db.Column(db.Integer)
        copd = db.Column(db.Integer)
        asthma = db.Column(db.Integer)
        immunosup = db.Column(db.Integer)
        hypertension = db.Column(db.Integer)
        another_complication = db.Column(db.Integer)
        cardiovascular = db.Column(db.Integer)
        obesity = db.Column(db.Integer)
        renal_chronic = db.Column(db.Integer)
        tobacco = db.Column(db.Integer)
        closed_contanct = db.Column(db.Integer)
        def __repr__(self):
            return '<Patient %r>' % (self.name)
    return {'Patient':Patient}