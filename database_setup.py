#!/usr/bin/env python2
#
# Create database with tables for Item Catalog project

import os
import sys
import random
import string
from flask import jsonify
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

Base = declarative_base()
secret_key = 'HFF765DJBFD876SDC654FJD74RFOIS76'


class User(Base):
    """user table to store users logged in to the system"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    picture = Column(String)
    email = Column(String, index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }


class Category(Base):
    """Main categories in the catalog."""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    categoryItems = relationship("CategoryItem", back_populates="category")

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'Item': [categoryItem.serialize
                     for categoryItem in self.categoryItems]
        }


class CategoryItem(Base):
    """Category items in the catalog."""
    __tablename__ = 'category_item'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(1000))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates="categoryItems")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):
        return {
            'cat_id': self.category_id,
            'description': self.description,
            'id': self.id,
            'title': self.title
        }


engine = create_engine("postgresql://catalog:catalog@localhost:5432/catalog")
Base.metadata.create_all(engine)
