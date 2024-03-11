# -*- coding: utf-8 -*-

# Import the module directly, instead of using a relative import.
# This makes the code more readable and easier to understand.
import models

# Use the imported module to create a new instance of the MyModel class.
m = models.MyModel()

# Set some attributes on the instance.
m.name = "My Model"
m.description = "This is an example model."

# Save the instance to the database.
m.save()

# Retrieve the instance from the database.
m = models.MyModel.objects.get(name="My Model")

# Print the instance's attributes.
print(f"Model name: {m.name}")
print(f"Model description: {m.description}")
