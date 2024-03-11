#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import the models module from the django_app application
from django_app.models import MyModel

# Use the MyModel class from the models module
m = MyModel(name="My Model", description="This is an example model")
m.save()

# Print the object's name and id
print(f"Model name: {m.name}, ID: {m.id}")

