from exts import db

"""
Class Recipe:
    id:int primary key
    title: str
    description: str (text)
    img_src: str(text)
"""

class Recipe(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    title=db.Column(db.String(), nullable=False)
    description=db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<Recipe {self.title}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title, description):
        self.title = title
        self.description = description
        db.session.commit()

#user login info
"""
class User:
    id:integer
    username:string
    email:string
    password:string
"""

class User(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(25), nullable=False, unique=True)
    email=db.Column(db.String(80), nullable=False, unique=True)
    password=db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<User {self.username} {self.id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

# charities info
"""
class Charities:
    id:integer
    name:string
    short_description:string
    link:string
    img_src=string
    address_line1=string
    city=string
    state=string
    country=string
    zip=integer
"""

class Charities(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(120), nullable=False)
    short_description=db.Column(db.String(400), nullable=False)
    link=db.Column(db.Text(), nullable=False)
    img_src=db.Column(db.Text())

    address_line1=db.Column(db.String(120), nullable=False)
    city=db.Column(db.String(40), nullable=False)
    state=db.Column(db.String(40), nullable=False)
    country=db.Column(db.String(60), nullable=False)
    zip=db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Charities {self.name} {self.id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

#user donations
"""
class Donation:
    id:integer
    username:string
    charity_id:integer
    amount:double
    date:date
    motivation:string
"""

class Donation(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(25), db.ForeignKey('user.username'), nullable=False)
    charity_id=db.Column(db.Integer(), db.ForeignKey('charities.id'), nullable=False)
    amount=db.Column(db.Float(), nullable=False)
    date=db.Column(db.Date(), nullable=False)
    motivation=db.Column(db.Text())

    def __repr__(self):
        return f"<Donation {self.user_id} {self.amount} {self.charity_id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()