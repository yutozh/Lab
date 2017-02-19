# coding=utf8

from app import db


Purchase = db.Table('purchase',
                    db.Column("id", db.Integer, primary_key=True),
                    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                    db.Column("book_id", db.Integer, db.ForeignKey("book.id")),
                    db.Column("quantity", db.Integer, default=1),
                    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=False)
    # bookInfo = db.Column(db.String(128),unique=False)
    email = db.Column(db.String(128))
    books = db.relationship("Book", secondary=Purchase,
                            backref=db.backref('users', lazy='dynamic'))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(128))
    publishHouse = db.Column(db.String(128))
    author = db.Column(db.String(128))
    introduction = db.Column(db.Text)
    priceBefore = db.Column(db.Integer)
    priceOff = db.Column(db.Integer)
    priceAfter = db.Column(db.Integer)
    ISBN = db.Column(db.String(128))

    def toJson(self):
        return {
            "bookname": self.bookName,
            "priceBefore": self.priceBefore,
            "priceOff": self.priceOff,
            "priceAfter": self.priceAfter,
            "introduction": self.introduction,
            "publishHouse": self.publishHouse,
            "author": self.author,
            "ISBN": self.ISBN
        }
